###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List

from ccp_server.kc.connection import KeycloakAdminClient
from ccp_server.kc.schemas import schemas
from ccp_server.util.logger import log


class KeycloakGroupService(KeycloakAdminClient):

    @log
    def create_group(self, group: schemas.Group) -> schemas.Group:
        """Create a group in Keycloak"""
        group_meta = group.__dict__

        return self.connect.create_group(payload=group_meta)

    @log
    def get_group(self, group_id: str) -> schemas.Group:
        """Get a group from Keycloak"""

        return self.connect.get_group(group_id)

    @log
    def add_user_to_group(self, group_id: str, username: str) -> schemas.Group:
        """Add a user to a group"""

        user_id = self.connect.get_user_id(username)

        return self.connect.group_user_add(group_id=group_id, user_id=user_id)

    @log
    def remove_user_from_group(self, group_id: str, username: str) -> schemas.Group:
        """Remove a user from a group"""

        user_id = self.connect.get_user_id(username)

        return self.connect.group_user_remove(group_id=group_id, user_id=user_id)

    @log
    def get_group_members(self, group_id: str, query: dict) -> List[Dict]:
        """Get users in a group
        :param query: dict
        :param group_id: Id of the group
        :return: List of users in the group"""
        return self.connect.get_group_members(group_id=group_id)

    def create_sub_group(self, sub_group: schemas.Group, parent: str) -> schemas.Group:
        """Create a subgroup in a group
        :param sub_group: Subgroup payload
        :param parent: ID of the group.
        :return: Subgroup"""

        return self.connect.create_group(payload=sub_group.__dict__, parent=parent)
