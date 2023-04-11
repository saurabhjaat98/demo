###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List

from ccp_server.kc.connection import KeycloakAdminClient
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log


class KeycloakClientService(KeycloakAdminClient):

    @log
    def get_client_uuid(self) -> str:
        """Get default client internal id
        :return: client uuid"""

        return self.connect.get_client_id(client_id=Constants.KEYCLOAK_CLIENT_ID)

    @log
    def get_client_roles(self) -> List[Dict]:
        """Get default client roles
        :return: client roles"""

        return self.connect.get_client_roles(self.get_client_uuid())

    @log
    def get_client_role(self, roles: List[str]) -> Dict:
        """Get client role details
         :param roles: role name
         :return: role details"""
        s = set(roles)
        client_roles = self.get_client_roles()

        target_role = [d for d in client_roles if d['name'] in s]

        if len(target_role) > 0:
            return target_role
        return None

    @log
    def get_client_roles_name(self) -> List:
        """
        Get default client roles name
        :return: client roles list
        """
        roles_meta = self.get_client_roles()
        roles = [role["name"] for role in roles_meta]
        return roles
