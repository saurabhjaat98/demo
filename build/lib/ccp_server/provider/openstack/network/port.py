###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.schema.v1 import schemas
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class Port(services.Port):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.FLOATING_IP

    @log
    async def create_port(self, network_id: str, port: schemas.Port):
        try:
            binding_dict = {
                "binding:vnic_type": port.binding.vnic_type,
                "binding:host_id": port.binding.host_id
            }
            cloud_response = self.conn.connect().create_port(
                name=port.name,
                network_id=network_id,
                admin_state_up=port.admin_state_up,
                device_id=port.device_id,
                device_owner=port.device_owner,
                mac_address=port.mac_address,
                port_security_enabled=port.port_security_enabled,
                fixed_ips=port.fixed_ips,
                **binding_dict,
            )
            return await mapper(data=cloud_response, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(
                Message.OPENSTACK_CREATE_ERR_MSG.format('Port'), e.status_code, e.details)

    @log
    async def list_ports_by_network_id(self, network_id: str):
        cloud_res = self.conn.connect().list_ports(
            filters={"network_id": network_id})
        return await mapper(data=cloud_res, resource_name=self.collection)

    @log
    async def delete_port(self, port_id: str):
        try:
            if not self.conn.connect().delete_port(port_id):
                raise CCPOpenStackException("Failed To Delete Port")
        except Exception as e:
            raise CCPOpenStackException(f' {e.message or e}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
