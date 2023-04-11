###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
# Modified by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                   #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class Flavor(services.Flavor):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.FLAVOR

    @log
    async def create_flavor(self, flavor: models.Flavor) -> models.Flavor:
        try:
            cloud_res = self.conn.connect().create_flavor(**flavor.__dict__)
            return await mapper(data=cloud_res, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Flavor'), e.status_code, e.details)

    @log
    async def delete_flavor(self, name_or_id):
        return self.conn.connect().delete_flavor(
            name_or_id=name_or_id
        )

    async def list_flavors(self):
        flavors = self.conn.connect().list_flavors()
        return await mapper(data=flavors, resource_name=self.collection)
