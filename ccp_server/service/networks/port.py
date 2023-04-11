###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
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


class PortService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.PORT

    @log
    async def create_port(self, project_id: str, network_id: str, port: schemas.Port) -> str:
        """This method is used to create a port in cloud and mongo."""
        """DB Response"""
        db_response = await self.db.get_document_by_ids(collection_name=Constants.MongoCollection.NETWORK,
                                                        uid=network_id,
                                                        project_id=project_id,
                                                        raise_exception=True
                                                        )
        """Check for duplicate name"""
        await self.db.check_document_by_name(
            collection_name=self.collection,
            name=port.name,
            project_id=project_id,
            filter_dict={"network_id": network_id},
            raise_exception=True)
        db_port_name = port.name
        port.name = Utils.generate_unique_str()

        """Save the port in the OpenStack"""
        cloud_response = await self.connect.port.create_port(network_id=db_response['reference_id'], port=port)

        """Save the port in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=db_port_name,
                                              project_id=project_id, network_id=network_id)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    async def list_ports_by_network_id(self, project_id: str, network_id: str,
                                       pageable: Pageable = None, use_db: StrictBool = True
                                       ) -> Tuple[List[Dict], int]:
        """ Fetch all the ports from database or cloud
        :return: List[Dict] List of ports
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                project_id=project_id,
                filter_dict={"network_id": network_id})
        else:
            network_meta = await self.db.get_document_by_ids(Constants.MongoCollection.NETWORK, uid=network_id)
            mapper_res = await self.connect.port.list_ports_by_network_id(network_meta['reference_id'])
            return mapper_res, len(mapper_res)

    @log
    async def get_port(self, project_id: str, network_id: str, port_id: str) -> Dict:
        """
        :param: port_id -> str
        :param: project_id -> str
        :param: network_id -> str
        :return: Dict
        """
        return await self.db.get_document_by_ids(collection_name=self.collection,
                                                 uid=port_id,
                                                 project_id=project_id,
                                                 filter_dict={
                                                     "network_id": network_id},
                                                 raise_exception=True)

    @log
    async def delete_port(self, project_id: str, network_id: str, port_id: str) -> None:
        """This method is used to delete the port from mongo.
        :param port_id: id of the port
        :param project_id: id of the project
        :param network_id: id of the network
        :return: None
        """

        """DB Response"""
        port_db_res = await self.db.get_document_by_ids(collection_name=self.collection,
                                                        uid=port_id,
                                                        project_id=project_id,
                                                        filter_dict={
                                                            "network_id": network_id},
                                                        raise_exception=True)
        await self.connect.port.delete_port(port_db_res['reference_id'])

        await self.db.soft_delete_document_by_uuid(self.collection, port_id)
