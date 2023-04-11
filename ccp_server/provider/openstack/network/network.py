###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class Network(services.Network):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.NETWORK

    @log
    async def create_network(self, network: models.Network) -> models.Network:
        try:
            cloud_response = self.conn.connect().create_network(**network.__dict__)
            return await mapper(data=cloud_response, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Network'), e.status_code, e.details)

    @log
    async def list_all_networks(self):
        cloud_response = self.conn.connect().list_networks()
        return await mapper(data=cloud_response, resource_name=self.collection)

    @log
    async def delete_network(self, network_id: str):
        try:
            if not self.conn.connect().delete_network(network_id):
                raise CCPOpenStackException("Failed To Delete Network")
        except Exception as e:
            raise CCPOpenStackException(f' {e.message or e}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
