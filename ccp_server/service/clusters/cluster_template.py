###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
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
from ccp_server.util.utils import Utils


user_service: UserService = UserService()


class ClusterTemplateService(Provider):

    collection = Constants.MongoCollection.CLUSTER_TEMPLATE

    @log
    async def create_cluster_template(self, project_id: str, cluster_template: schemas.ClusterTemplate) -> str:
        """This method is used to create a cluster template in cloud and mongo."""

        """Check for template name if already exist"""
        await self.db.check_document_by_name(self.collection, cluster_template.name, raise_exception=True)

        """ Cloud project ID """
        db_response = await self.db.get_document_by_uuid(Constants.MongoCollection.PROJECT, uid=project_id,
                                                         raise_exception=True)

        cluster_template_model: provider_models.ClusterTemplate = provider_models.ClusterTemplate(
            name=Utils.generate_unique_str(),
            image_id=Constants.Cluster.IMAGE,
            keypair_id=cluster_template.keypair_id,
            coe=cluster_template.coe,
            public=cluster_template.public,
            hidden=cluster_template.hidden,
            registry_enabled=cluster_template.registry_enabled,
            tls_disabled=cluster_template.tls_disabled,
            flavor_id=Constants.Cluster.FLAVOR,
            master_flavor_id=Constants.Cluster.FLAVOR,
            volume_driver=cluster_template.volume_driver,
            docker_storage_driver=cluster_template.docker_storage_driver,
            docker_volume_size=Constants.Cluster.DOCKER_VOLUME_SIZE,
            network_driver=cluster_template.network_driver,
            http_proxy=cluster_template.http_proxy,
            https_proxy=cluster_template.https_proxy,
            no_proxy=cluster_template.no_proxy,
            external_network_id=cluster_template.external_network_id,
            fixed_network=cluster_template.fixed_subnet,
            fixed_subnet=cluster_template.fixed_subnet,
            dns_nameserver=cluster_template.dns_nameserver,
            master_lb_enabled=cluster_template.master_lb_enabled,
            floating_ip_enabled=cluster_template.floating_ip_enabled,
            labels=cluster_template.labels,
            project_id=db_response['reference_id']
        )

        """Save the cluster template in the OpenStack"""
        cloud_response = await self.connect.cluster_template.create_cluster_template(
            project_id=project_id, cluster_template=cluster_template_model)

        """Save the cluster template in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=cluster_template.name,
                                              project_id=project_id)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    async def list_cluster_templates_by_project(self, pageable: Pageable = None, project_id: str = None):
        """ Fetch all the cluster templates in cloud and mongo.
        :param pageable: Pageable object
        :param project_id: project id.
        :return: List of cluster templates.

        """

        projects = await user_service.get_logged_in_user_projects()

        if project_id not in [project.get('uuid') for project in projects]:
            raise CCPUnauthorizedException(
                "User unauthorized to view requested templates")

        return await self.db.get_document_list_by_ids(
            collection_name=self.collection,
            pageable=pageable,
            project_id=project_id
        )

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_cluster_templates(self, pageable: Pageable = None, use_db: StrictBool = True):
        """
        This method is used to list all the cluster templates in mongo and cloud.
        :param pageable: Pageable object
        :param use_db: If true it will fetch the result from Mongo, else from cloud
        :return: List of cluster templates.
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                exclude_project=True
            )
        else:
            cloud_response = await self.connect.cluster_template.list_all_cluster_templates()
            return cloud_response, len(cloud_response)

    @log
    async def get_cluster_template(self, project_id: str, cluster_template_id: str) -> Dict:
        """
        :param: cluster_template_id -> str
        :return: Dict
        """
        projects = await user_service.get_logged_in_user_projects()

        if project_id not in [project.get('uuid') for project in projects]:
            raise CCPUnauthorizedException(
                "User unauthorized to view requested template")

        return await self.db.get_document_by_ids(collection_name=self.collection,
                                                 uid=cluster_template_id,
                                                 project_id=project_id,
                                                 raise_exception=True)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN, Constants.CCPRole.PROJECT_ADMIN)
    async def delete_cluster_template(self, project_id: str, cluster_template_id) -> None:
        """This method is used to delete the cluster template from mongo.
        :param cluster_template_id: id of the cluster template
        :param project_id: id of the project
        :return: None
        """

        projects = await user_service.get_logged_in_user_projects()

        if project_id not in [project.get('uuid') for project in projects]:
            raise CCPUnauthorizedException(
                "User unauthorized to delete the requested template")

        cluster_template = await self.db.get_document_by_ids(collection_name=self.collection,
                                                             uid=cluster_template_id,
                                                             project_id=project_id,
                                                             raise_exception=True)
        await self.connect.cluster_template.delete_cluster_template(cluster_template['reference_id'])

        await self.db.soft_delete_document_by_uuid(self.collection, cluster_template_id)
