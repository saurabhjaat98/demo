###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
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


class Router(services.Router):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.ROUTER

    @log
    async def create_router(self, router: models.Router) -> models.Router:
        try:
            cloud_response = self.conn.connect().create_router(
                name=router.name,
                admin_state_up=router.admin_state_up,
                ext_gateway_net_id=router.ext_gateway_net_id,
                enable_snat=router.enable_snat,
                ext_fixed_ips=router.ext_fixed_ips,
                project_id=router.project_id,
                availability_zone_hints=router.availability_zone_hints
            )
            return await mapper(data=cloud_response, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Router'), e.status_code, e.details)

    @log
    async def list_all_routers(self):
        cloud_response = self.conn.connect().list_routers()
        return await mapper(data=cloud_response, resource_name=self.collection)

    @log
    async def delete_router(self, router_id: str):
        try:
            if not self.conn.connect().delete_router(router_id):
                raise CCPOpenStackException("Failed To Delete Router")
        except Exception as e:
            raise CCPOpenStackException(f' {e.message or e}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
