###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023
#  Modified by Vicky Upadhyay <vicky@coredge.io>, Feb 2023                    #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class Volume(services.Volume):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.VOLUME

    @log
    async def create_volume(self, volume: models.Volume) -> models.Volume:
        """This method is used to create a volume
        :param volume: Request body.
        :return: The created volume ``Volume`` object."""
        try:
            cloud_res = self.conn.connect().create_volume(**volume.__dict__)
            return await mapper(data=cloud_res, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Volume'), e.status_code, e.details)

    @log
    async def delete_volume(self, volume_id: str) -> None:
        """This method is used to delete a volume.
        :param volume_id: Volume ID.
        :return: True if deletion was successful, else False."""
        return self.conn.connect().delete_volume(volume_id)

    @log
    async def list_all_volumes(self):
        """This method is used to list volumes.
        :return: List of volumes."""
        cloud_res = self.conn.connect().list_volumes()
        return await mapper(data=cloud_res, resource_name=self.collection)

    @log
    async def get_volume(self, volume_id: str):
        """This method is used to get a volume.
        :param volume_id: Volume ID.
        :return: The volume ``Volume`` object."""
        cloud_res = self.conn.connect().get_volume(volume_id)
        return await mapper(data=cloud_res, resource_name=self.collection)

    @log
    async def attach_volume(self, server, volume):
        """This method is used to attach a volume to a server.
        :param server: Server object.
        :param volume: Volume object.
        :return: True if attachment was successful, else False."""
        self.conn.connect().attach_volume(server=server, volume=volume)

    @log
    async def detach_volume(self, server, volume):
        """This method is used to attach a volume to a server.
        :param server: Server object.
        :param volume: Volume object.
        :return: None"""
        self.conn.connect().detach_volume(server=server, volume=volume)
