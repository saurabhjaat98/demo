###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from keycloak.keycloak_admin import KeycloakAdmin
from keycloak.keycloak_admin import KeycloakOpenID

from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPKeycloakException
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log

LOG = KGLogger(__name__)


class KeycloakAdminClient:
    __client_secret_key = None

    def __init__(self):
        pass

    @property
    @log
    def connect(self) -> KeycloakAdmin:
        try:
            return KeycloakAdmin(
                verify=False,
                server_url=Constants.KEYCLOAK_URL,
                client_id=Constants.KEYCLOAK_CLIENT_ID,
                client_secret_key=self.client_secret_key,
                user_realm_name=Constants.KEYCLOAK_REALM,
            )
        except Exception:
            raise CCPKeycloakException()

    @property
    @log
    def oid_connect(self):
        try:
            return KeycloakOpenID(
                verify=False,
                server_url=Constants.KEYCLOAK_URL,
                client_id=Constants.KEYCLOAK_CLIENT_ID,
                client_secret_key=self.client_secret_key,
                realm_name=Constants.KEYCLOAK_REALM,
            )
        except Exception:
            raise CCPKeycloakException()

    @property
    @log
    def __admin(self) -> KeycloakAdmin:
        try:
            keycloak_admin = KeycloakAdmin(
                verify=False,
                server_url=Constants.KEYCLOAK_URL,
                username=Constants.KEYCLOAK_ADMIN_USERNAME,
                password=Constants.KEYCLOAK_ADMIN_PASSWORD
            )

            # Set the provided realm
            keycloak_admin._realm_name = Constants.KEYCLOAK_REALM

            return keycloak_admin
        except Exception:
            raise CCPKeycloakException()

    @property
    def client_secret_key(self) -> str:
        """Get client secret key.
        :return: client secret key"""

        if KeycloakAdminClient.__client_secret_key:
            return KeycloakAdminClient.__client_secret_key

        if Constants.INTERNAL_KEYCLOAK:
            LOG.info('Using internal keycloak')
            client_uuid = self.__admin.get_client_id(
                client_id=Constants.KEYCLOAK_CLIENT_ID)
            response = self.__admin.get_client_secrets(client_uuid)
            if response:
                KeycloakAdminClient.__client_secret_key = response['value']
        else:
            LOG.info('Using external keycloak')
            KeycloakAdminClient.__client_secret_key = Constants.KEYCLOAK_CLIENT_SECRET

        return KeycloakAdminClient.__client_secret_key
