###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from ccp_server.kc.connection import KeycloakAdminClient
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.exceptions import CCPKeycloakException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message
from ccp_server.util.token import TokenInfo


class KeycloakAuthService(KeycloakAdminClient):

    @log
    def introspect(self, token: str) -> dict:
        """Get token info from the Keycloak server.
        :param token: str
        :return: dict Token information
        """

        if not token:
            raise CCPBadRequestException(message=Message.TOKEN_EMPTY)

        try:
            return self.oid_connect.introspect(token)
        except Exception:
            raise CCPKeycloakException()

    @log
    def tokeninfo(self, token: str) -> TokenInfo:
        """Get the token information from the JWT token.
        :param token: str
        :return: TokenInfo
        """

        token_details = self.introspect(token)
        return TokenInfo(token_details)
