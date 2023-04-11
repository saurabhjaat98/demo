###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Apr 2023    #
###############################################################################
from typing import Dict

from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.provider import models as provider_models
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.service.user import UserService
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPUnauthorizedException
from ccp_server.util.logger import log


user_service: UserService = UserService()


class ClusterService(Provider):

    collection = Constants.MongoCollection.CLUSTER

    @log
    async def create_cluster(self, project_id: str, cluster_template_id: str, cluster: schemas.Cluster) -> str:
        """This method is used to create a cluster template in cloud and mongo."""

        """Check for cluster name if already exist"""
        await self.db.check_document_by_name(self.collection, cluster.name, raise_exception=True)

        """ Cloud project ID """
        project_db_response = await self.db.get_document_by_uuid(Constants.MongoCollection.PROJECT, uid=project_id,
                                                                 raise_exception=True)

        """ Cloud Cluster Template ID"""
        cluster_template_db_response = await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.CLUSTER_TEMPLATE,
            uid=cluster_template_id, project_id=project_id, raise_exception=True)

        cluster_model: provider_models.Cluster = provider_models.Cluster(
            name=cluster.name,
            cluster_template_id=cluster_template_db_response['reference_id'],
            availability_zone=cluster.availability_zone,
            keypair_id=cluster.keypair,
            master_count=cluster.master_count,
            master_flavor_id=Constants.Cluster.FLAVOR,
            node_count=cluster.node_count,
            flavor_id=Constants.Cluster.FLAVOR,
            project_id=project_db_response['reference_id']
        )

        """Save the cluster in the OpenStack"""
        cloud_response = await self.connect.cluster.create_cluster(
            project_id=project_id, cluster=cluster_model)

        """Save the cluster in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=cluster.name,
                                              project_id=project_id)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    async def list_clusters_by_project(self, pageable: Pageable = None, project_id: str = None):
        """ Fetch all the clusters in cloud and mongo.
        :param pageable: Pageable object
        :param project_id: project id.
        :return: List of clusters.

        """

        projects = await user_service.get_logged_in_user_projects()

        if project_id not in [project.get('uuid') for project in projects]:
            raise CCPUnauthorizedException(
                "User unauthorized to view requested clusters")

        return await self.db.get_document_list_by_ids(
            collection_name=self.collection,
            pageable=pageable,
            project_id=project_id
        )

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_clusters(self, pageable: Pageable = None, use_db: StrictBool = True):
        """
        This method is used to list all the clusters in mongo and cloud.
        :param pageable: Pageable object
        :param use_db: If true it will fetch the result from Mongo, else from cloud
        :return: List of clusters.
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                exclude_project=True
            )
        else:
            cloud_response = await self.connect.cluster.list_all_clusters()
            return cloud_response, len(cloud_response)

    @log
    async def get_cluster(self, project_id: str, cluster_id: str) -> Dict:
        """
        :param: cluster_id -> str
        :return: Dict
        """
        projects = await user_service.get_logged_in_user_projects()

        if project_id not in [project.get('uuid') for project in projects]:
            raise CCPUnauthorizedException(
                "User unauthorized to view requested cluster")

        return await self.db.get_document_by_ids(collection_name=self.collection,
                                                 uid=cluster_id,
                                                 project_id=project_id,
                                                 raise_exception=True)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN, Constants.CCPRole.PROJECT_ADMIN)
    async def delete_cluster(self, project_id: str, cluster_id) -> None:
        """This method is used to delete the cluster from mongo and cloud.
        :param cluster_id: id of the cluster
        :param project_id: id of the project
        :return: None
        """

        projects = await user_service.get_logged_in_user_projects()

        if project_id not in [project.get('uuid') for project in projects]:
            raise CCPUnauthorizedException(
                "User unauthorized to delete the requested cluster")

        cluster = await self.db.get_document_by_ids(collection_name=self.collection,
                                                    uid=cluster_id,
                                                    project_id=project_id,
                                                    raise_exception=True)
        await self.connect.cluster.delete_cluster(cluster['reference_id'])

        await self.db.soft_delete_document_by_uuid(self.collection, cluster_id)
