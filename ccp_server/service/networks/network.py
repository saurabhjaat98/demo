###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from typing import Dict

from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.provider import models as provider_models
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class NetworkService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.NETWORK

    @log
    async def create_network(self, project_id: str, network: schemas.Network) -> str:
        """This method is used to create a Network in cloud and mongo."""
        # TODO: Add availability zone support

        """Check for network if already exist"""
        # TODO: Create decorator to check if the name already exist or not
        # @name_exists
        await self.db.check_document_by_name(
            collection_name=self.collection,
            name=network.name,
            project_id=project_id,
            raise_exception=True)

        db_network_name = network.name
        network.name = Utils.generate_unique_str()

        network_model: provider_models.Network = provider_models.Network(
            **network.__dict__)

        """Save the network in the OpenStack"""
        cloud_response = await self.connect.network.create_network(network_model)

        """Save the network in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=db_network_name,
                                              project_id=project_id, tags=network.tags)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    async def list_networks_by_project_id(self, pageable: Pageable = None, project_id: str = None):
        """
        This method is used to list all the networks in mongo.
        :param pageable: Pageable object
        :return: List of networks.
        :param project_id: project id.
        """
        # TODO : Add filter specific for logged in user

        return await self.db.get_document_list_by_ids(
            collection_name=self.collection,
            pageable=pageable,
            project_id=project_id
        )

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_networks(self, pageable: Pageable = None, use_db: StrictBool = True):
        """
        This method is used to list all the networks in mongo and cloud.
        :param pageable: Pageable object
        :param use_db: If true it will fetch the result from Mongo, else from cloud
        :return: List of networks.
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                exclude_project=True
            )
        else:
            cloud_response = await self.connect.network.list_all_networks()
            return cloud_response, len(cloud_response)

    @log
    async def get_network(self, project_id: str, network_id: str) -> Dict:
        """
        :param: network_id -> str
        :param: project_id -> str
        :return: Dict
        """
        return await self.db.get_document_by_ids(collection_name=self.collection,
                                                 uid=network_id,
                                                 project_id=project_id,
                                                 raise_exception=True)

    @log
    async def update_network(self, project_id, network_id, request):
        """
        Update  network
        :param project_id: Project ID
        :param network_id: id of the network
        :param request: ObjectUpdate request body.
        :return: None
        """
        """ check if network exsit in db and part of this project"""
        await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.NETWORK,
            uid=network_id,
            project_id=project_id,
            raise_exception=True)

        await self.db.update_document_by_uuid(Constants.MongoCollection.NETWORK,
                                              uid=network_id,
                                              data_dict=request.dict(include={'name', 'description', 'tags'}))

    @log
    async def delete_network(self, project_id: str, network_id: str) -> None:
        """This method is used to delete the network from mongo.
        :param network_id: id of the network
        :param project_id: id of the project
        :return: None
        """

        """DB response"""
        network_db_res = await self.db.get_document_by_ids(collection_name=self.collection,
                                                           uid=network_id,
                                                           project_id=project_id,
                                                           raise_exception=True)
        await self.connect.network.delete_network(network_db_res['reference_id'])
        await self.db.soft_delete_document_by_uuid(self.collection, network_id)
