###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class KeyPair:
    """
    KeyPair class to provide common methods for all cloud providers
    """

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.KEYPAIR

    @log
    async def create_keypair(self, name, request):
        """
        Create a new keypair with the given name and public key
        :param name: Name of the keypair
        :param request: Public key of the keypair
        """
        try:
            cloud_res = self.conn.connect().create_keypair(
                name=name, public_key=request.public_key)
            return await mapper(data=cloud_res, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Keypair'), e.status_code, e.details)

    @log
    async def delete_keypair(self, name: str) -> bool:
        """
        Delete a keypair
        :param name: Name of the keypair
        :returns: True if delete succeeded, False otherwise.
        """
        return self.conn.connect().delete_keypair(name=name)

    @log
    async def list_keypairs(self, filters=None) -> list:
        """
        List all keypairs
        :returns: List of keypairs
        """
        cloud_res = self.conn.connect().list_keypairs(filters=filters)
        return await mapper(data=cloud_res, resource_name=self.collection)

    @log
    async def get_keypair(self, name: str):
        pass
