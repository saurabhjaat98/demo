###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List

from ccp_server.db.models import Organization
from ccp_server.kc.group import KeycloakGroupService
from ccp_server.kc.schemas.schemas import Group as KCGroup
from ccp_server.schema.v1 import schemas
from ccp_server.service.providers import Provider
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log


class GroupService(Provider):

    def __init__(self):
        self.kc_group_service: KeycloakGroupService = KeycloakGroupService()

    @log
    async def create_group(self, group_req: schemas.Group):
        kc_group_req = KCGroup(name=group_req.name)

        """Save the group in Keycloak"""
        group_id = self.kc_group_service.create_group(kc_group_req)

        """Save the group/Organization in mongo db"""
        mongo_data = Organization(
            name=group_req.name,
            description=group_req.name,
            default_cloud=ccp_context.get_cloud(),
            cloud=ccp_context.get_cloud(),
            reference_id=group_id,
            communication_address=group_req.communication_address,
            billing_address=group_req.billing_address,
            tan_number=group_req.tan_number,
            gst_number=group_req.gst_number
        )
        _meta, doc_id = await self.db.write_document(Constants.MongoCollection.ORGANIZATION, mongo_data)
        return doc_id

    @log
    async def add_user_to_group(self, group_id: str, username: str) -> None:
        """Add a user to a group.
        :param group_id: Group id
        :param username: Username
        :return: None"""

        return self.kc_group_service.add_user_to_group(group_id=group_id, username=username)

    @log
    async def remove_user_from_group(self, group_id: str, username: str) -> None:
        """Remove a user from a group.
        :param group_id: Group id
        :param username: Username
        :return: None"""

        return self.kc_group_service.remove_user_from_group(group_id=group_id, username=username)

    @log
    async def get_group_members(self, group_id: str, query: dict) -> List[Dict]:
        """Get members of group.
        :param query: dict
        :param group_id: group id
        :return: List of members
        """

        return self.kc_group_service.get_group_members(group_id=group_id, query=query)
