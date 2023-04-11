###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.enums import InstanceActionEnum
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class Instance:
    """
    Class to represent an instance
    """

    def __init__(self, connection: services.Connection):
        """
        Constructor for the Instance class
        :param connection: Connection object
        """
        self.conn = connection

    @log
    async def create_instance(self, instance: models.Instance):
        """
        Create a new instance with the given name and the public key
        :param instance: Contains Name of the instance and the public key
        returns: The created compute ``Server`` object
        """
        try:
            cloud_response = self.conn.connect().create_server(**instance.dict(exclude_unset=True, exclude_none=True,
                                                                               exclude={'instance_username',
                                                                                        'instance_password', 'tags'}),
                                                               wait=True)
            resp = await mapper(data=cloud_response, resource_name=Constants.MongoCollection.INSTANCE)
            resp.security_groups = resp.cloud_meta['security_groups']
            return resp
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Instance'), e.status_code, e.details)

    @log
    async def list_all_instances(self):
        """
        List all instances
        :return: List of all instances
        """
        cloud_response = self.conn.connect().list_servers()
        return await mapper(data=cloud_response, resource_name=Constants.MongoCollection.INSTANCE)

    @log
    async def delete_instance(self, instance_id: str):
        """
        Delete an instance
        :param instance_id: id of the instance
        :return: None
        """
        try:
            if not self.conn.connect().delete_server(name_or_id=instance_id):
                raise CCPOpenStackException(f'Failed to delete instance ')
        except Exception as e:
            raise CCPOpenStackException(f' {e.message or e}',
                                        status_code=e.status_code or e.http_status, detail=e.details)

    @log
    async def instance_action(self, instance_id: str, action: InstanceActionEnum, action_schema):
        """
        Perform an action on an instance
        :param instance_id: id of the instance
        :param action: Action to perform
        :return: None
        """
        if action == InstanceActionEnum.STOP:
            return self.conn.connect().compute.stop_server(server=instance_id)
        elif action == InstanceActionEnum.START:
            return self.conn.connect().compute.start_server(server=instance_id)
        elif action == InstanceActionEnum.REBOOT:
            return self.conn.connect().compute.reboot_server(server=instance_id,
                                                             reboot_type=action_schema.__dict__[action].reboot)
        elif action == InstanceActionEnum.REBUILD:
            return self.conn.connect().compute.rebuild_server(server=instance_id,
                                                              **action_schema.__dict__[action].dict(exclude_unset=True,
                                                                                                    exclude_none=True))
        elif action == InstanceActionEnum.RESIZE:
            return self.conn.connect().compute.resize_server(server=instance_id,
                                                             flavor=action_schema.__dict__[action].flavorRef)
        elif action == InstanceActionEnum.RESUME:
            return self.conn.connect().compute.resume_server(server=instance_id)
        elif action == InstanceActionEnum.PAUSE:
            return self.conn.connect().compute.pause_server(server=instance_id)
        elif action == InstanceActionEnum.UNPAUSE:
            return self.conn.connect().compute.unpause_server(server=instance_id)
        else:
            raise NotImplementedError
