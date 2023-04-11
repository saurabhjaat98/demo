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


class SecurityGroupRule(services.SecurityGroupRule):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.SECURITY_GROUP_RULE

    @log
    async def create_security_group_rule(self,
                                         security_group_rule: models.SecurityGroupRule) -> models.SecurityGroupRule:
        try:
            cloud_response = self.conn.connect().create_security_group_rule(
                secgroup_name_or_id=security_group_rule.security_group,
                port_range_min=security_group_rule.port_range_min,
                port_range_max=security_group_rule.port_range_max,
                ethertype=security_group_rule.ethertype,
                protocol=security_group_rule.protocol,
                direction=security_group_rule.direction,
                remote_ip_prefix=security_group_rule.remote_ip_prefix,
                remote_group_id=security_group_rule.remote_group_id,
                project_id=security_group_rule.project_id,
                description=security_group_rule.description
            )
            return await mapper(data=cloud_response, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Security group rule'), e.status_code, e.details)

    @log
    async def list_security_group_rules(self, security_group_id: str):
        cloud_res = self.conn.connect().get_security_group_by_id(
            id=security_group_id)
        return await mapper(data=cloud_res.security_group_rules, resource_name=self.collection)

    @log
    async def delete_security_group_rule(self, security_group_rule_id: str):
        try:
            if not self.conn.connect().delete_security_group_rule(rule_id=security_group_rule_id):
                raise CCPOpenStackException(
                    "Failed To Delete Security Group Rule")
        except Exception as e:
            raise CCPOpenStackException(f' {e.message or e}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
