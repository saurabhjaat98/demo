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


class SecurityGroup(services.SecurityGroup):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.SECURITY_GROUP

    @log
    async def create_security_group(self, security_group: models.SecurityGroup) -> models.SecurityGroup:
        try:
            cloud_response = self.conn.connect().create_security_group(**
                                                                       security_group.__dict__)
            return await mapper(data=cloud_response, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Security group'), e.status_code, e.details)

    @log
    async def list_all_security_groups(self):
        cloud_res = self.conn.connect().list_security_groups()
        return await mapper(data=cloud_res, resource_name=self.collection)

    @log
    async def delete_security_group(self, security_group_id: str):
        try:
            if not self.conn.connect().delete_security_group(security_group_id):
                raise CCPOpenStackException("Failed To Delete Security Group")
        except Exception as e:
            raise CCPOpenStackException(f' {e.message or e}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
