###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
# Modified by Pankaj Khanwani <pankaj@coredge.io>, March 2023                 #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from typing import Dict

from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.logger import log


class FloatingIPService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.FLOATING_IP

    @log
    async def create_floating_ip(self, project_id: str, network_id: str) -> str:
        """This method is used to create a floating IP in cloud and mongo."""
        db_response = await self.db.get_document_by_ids(Constants.MongoCollection.NETWORK,
                                                        uid=network_id,
                                                        project_id=project_id,
                                                        raise_exception=True
                                                        )
        """Check for network has subnet or not"""
        subnet_db_res = await self.db.get_document_list_by_ids(
            collection_name=Constants.MongoCollection.SUBNET,
            project_id=project_id,
            filter_dict={"network_id": network_id})
        if not subnet_db_res:
            raise CCPBadRequestException(
                f"Network {network_id} doesn't have subnet")

        """Save the floating IP in the OpenStack"""
        cloud_response = await self.connect.floating_ip.create_floating_ip(network_id=db_response['reference_id'])

        """Save the floating_ip in the mongo db"""

        db_model = MongoAPI.populate_db_model(cloud_response,
                                              project_id=project_id, network_id=network_id)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_floating_ips(self, pageable: Pageable = None, use_db: StrictBool = True):
        """ Fetch all the floating IPs
        :return: List[Dict] List of all the floating IPs in the database
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                exclude_project=True)
        else:
            mapper_res = await self.connect.floating_ip.list_all_floating_ips()
            return mapper_res, len(mapper_res)

        # TODO : Add filter specific for logged in user

    @log
    async def list_floating_ips(self, project_id: str, pageable: Pageable = None):
        """ List all floating ips for a project
        :param project_id: project_id
        :param pageable: pageable object
        :return: list of floating ips
        """
        return await self.db.get_document_list_by_ids(
            collection_name=self.collection,
            project_id=project_id,
            pageable=pageable)

    @log
    async def get_floating_ip(self, project_id: str, network_id: str, floating_ip_id: str) -> Dict:
        """
        :param: floating_ip_id -> str
        :return: Dict
        """
        return await self.db.get_document_by_ids(collection_name=self.collection,
                                                 uid=floating_ip_id,
                                                 project_id=project_id,
                                                 filter_dict={'network_id': network_id})

    @log
    async def delete_floating_ip(self, project_id: str, network_id: str, floating_ip_id) -> None:
        """This method is used to delete the floating IP from mongo.
        :param floating_ip_id: id of the floating IP
        :param project_id: id of the project
        :param network_id: id of the network
        :return: None
        """

        """DB response"""
        db_response = await self.db.get_document_by_ids(collection_name=self.collection,
                                                        uid=floating_ip_id,
                                                        project_id=project_id,
                                                        filter_dict={
                                                            'network_id': network_id},
                                                        raise_exception=True)
        """ Delete the floating IP from Cloud """
        await self.connect.floating_ip.delete_floating_ip(db_response['reference_id'])
        await self.db.soft_delete_document_by_uuid(self.collection, floating_ip_id)
