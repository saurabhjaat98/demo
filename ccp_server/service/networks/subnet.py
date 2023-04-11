###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
# Modified by Pankaj Khanwani <pankaj@coredge.io>, March 2023                 #
###############################################################################
from typing import Dict
from typing import List
from typing import Tuple

from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class SubnetService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.SUBNET

    @log
    async def create_subnet(self, project_id, network_id, subnet: schemas.Subnet) -> str:
        """This method is used to create a subnet in cloud and mongo."""

        """Network DB response"""
        db_response = await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.NETWORK,
            uid=network_id,
            project_id=project_id,
            raise_exception=True)

        """Check for subnet if already exist with same name"""
        await self.db.check_document_by_name(
            collection_name=self.collection,
            name=subnet.name,
            project_id=project_id,
            filter_dict={"network_id": network_id},
            raise_exception=True)

        db_subnet_name = subnet.name
        subnet.name = Utils.generate_unique_str()

        """Save the subnet in the OpenStack"""
        cloud_response = await self.connect.subnet.create_subnet(network_id=db_response['reference_id'], subnet=subnet)

        """Save the subnet in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=db_subnet_name,
                                              project_id=project_id,
                                              network_id=network_id)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    async def list_subnets_by_network_id(self, pageable: Pageable = None, project_id: str = None,
                                         network_id: str = None, use_db: StrictBool = True) -> \
            Tuple[List[Dict], int]:
        """ Fetch all the subnets from database or cloud
        :return: List[Dict] List of all the subnets in the database
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                project_id=project_id,
                filter_dict={"network_id": network_id}
            )
        else:
            network_meta = await self.db.get_document_by_ids(Constants.MongoCollection.NETWORK, uid=network_id)
            mapper_res = await self.connect.subnet.list_subnets_by_network_id(network_meta["reference_id"])
            return mapper_res, len(mapper_res)

        # TODO : Add filter specific for logged in user

    @log
    async def get_subnet(self, project_id: str, network_id: str, subnet_id: str) -> Dict:
        """
        :param: subnet_id -> str
        :param: project_id -> str
        :param: network_id -> str
        :return: Dict
        """
        return await self.db.get_document_by_ids(
            collection_name=self.collection,
            uid=subnet_id,
            project_id=project_id,
            filter_dict={"network_id": network_id})

    @log
    async def delete_subnet(self, project_id: str, network_id: str, subnet_id) -> None:
        """This method is used to delete the subnet from mongo.
        :param subnet_id: id of the subnet
        :param project_id: id of the project
        :param network_id: id of the network
        :return: None
        """

        """DB response for deleting the subnet"""
        db_response = await self.db.get_document_by_ids(
            collection_name=self.collection,
            uid=subnet_id,
            project_id=project_id,
            filter_dict={"network_id": network_id},
            raise_exception=True)

        """Delete the subnet from cloud"""
        await self.connect.subnet.delete_subnet(db_response['reference_id'])
        await self.db.soft_delete_document_by_uuid(self.collection, subnet_id)
