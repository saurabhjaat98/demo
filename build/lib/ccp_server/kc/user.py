###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List

import httpx
from fastapi import status

from ccp_server.kc.client import KeycloakClientService
from ccp_server.kc.connection import KeycloakAdminClient
from ccp_server.kc.schemas import schemas
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.exceptions import CCPBusinessException
from ccp_server.util.exceptions import CCPKeycloakException
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
from ccp_server.util.messages import Message

LOG = KGLogger(__name__)


class KeycloakUserService(KeycloakAdminClient):

    def __init__(self):
        self.client_service: KeycloakClientService = KeycloakClientService()

    @log
    def create_user(self, user: schemas.User, exist_ok: bool = False, profile_completed: bool = False) -> schemas.User:
        """Create a user in Keycloak
        :param user: User object.
        :param profile_completed: Profile completed or not
        :param exist_ok: If True, ignore if user already exists
        :return: User object."""

        # Checks if the user already exists
        if not exist_ok:
            _user = None
            try:
                _user = self.get_user(user.email)
            except Exception:
                pass
            if _user:
                raise CCPBadRequestException(
                    message=Message.USER_ALREADY_EXISTS.format(user.email))

        attributes = {'mobile_number': user.mobile_number}
        if Constants.CCPRole.ORG_ADMIN in user.roles:
            attributes['profile_completed'] = profile_completed

        user_dict = {'username': user.email.lower(), 'firstName': user.first_name, 'lastName': user.last_name,
                     'email': user.email.lower(), 'enabled': True, 'groups': user.groups, 'attributes': attributes}

        # Create a user in Keycloak
        return self.connect.create_user(payload=user_dict, exist_ok=exist_ok)

    @log
    def update_email_action(self, username: str, actions: List[str]) -> None:
        """ This update_email_action function is to send mail to user after creating a new user in Keycloak.
        :param username: Username of the user.
        :param actions: List of actions to be performed. Possible actions are: 'VERIFY_EMAIL', 'UPDATE_PASSWORD'
        :return: None"""

        # if any of the actions does not match with the KEYCLOAK_SUPPORTED_EMAIL_ACTION then raise an exception
        if any(action not in Constants.KEYCLOAK_SUPPORTED_EMAIL_ACTION for action in actions):
            raise CCPBadRequestException(
                message=Message.INVALID_EMAIL_ACTION)

        user_id = self.connect.get_user_id(username)
        try:
            self.connect.send_update_account(user_id=user_id, payload=actions,
                                             client_id=Constants.KEYCLOAK_CLIENT_ID,
                                             lifespan=Constants.KEYCLOAK_USER_VERIFICATION_MAIL_TTL_IN_SEC,
                                             redirect_uri=Constants.KEYCLOAK_POST_VERIFICATION_LINK
                                             )
        except Exception as e:
            LOG.error(
                f'Error while sending email to user: {username}, Error {e}')

    # redirect_uri = Constants.KEYCLOAK_POST_VERIFICATION_LINK

    @log
    def update_user(self, username: str, user: schemas.User) -> None:
        """Update a user in Keycloak
        :param username: Username
        :param user: User object.
        :return: None."""

        user_dict = {"firstName": user.first_name, "lastName": user.last_name,
                     "enabled": True}

        user_id = self.get_user_id_by_username(username=username)

        # Update a user in Keycloak
        return self.connect.update_user(user_id=user_id, payload=user_dict)

    @log
    def get_user(self, username: str) -> schemas.User:
        """Get a user from Keycloak
        :param username: Username
        :return: User object."""

        user_id = self.get_user_id_by_username(username=username)

        return self.connect.get_user(user_id)

    @log
    def get_user_id_by_username(self, username: str) -> str:
        """Get a user id from Keycloak
        :param username: Username
        :return: User id."""

        return self.connect.get_user_id(username.lower())

    @log
    def delete_user(self, username: str) -> None:
        """Delete a user from Keycloak
        :param username: Username
        :return: None."""

        user_id = self.get_user_id_by_username(username=username)

        return self.connect.delete_user(user_id)

    @log
    def grant_roles(self, username: str, roles: List[str]) -> None:
        """Grant role to a user in Keycloak
        :param username: Username
        :param roles: Roles name
        :return: None."""

        user_id = self.get_user_id_by_username(username=username)
        kc_roles = self.client_service.get_client_role(roles=roles)
        client_id = self.client_service.get_client_uuid()

        self.connect.assign_client_role(
            user_id=user_id, client_id=client_id, roles=kc_roles)

    @log
    def revoke_roles(self, username: str, role_name: str) -> None:
        """Revoke role to a user in Keycloak
        :param username: Username
        :param role_name: Roles name
        :return: None."""

        user_id = self.get_user_id_by_username(username=username)
        role = self.client_service.get_client_role(roles=role_name)
        client_id = self.client_service.get_client_uuid()

        self.connect.delete_client_roles_of_user(user_id=user_id, client_id=client_id,
                                                 roles=role)

    @log
    def is_user_exists_in_group(self, group_id: str, username: str, raise_exception: bool = False) -> bool:
        """Check if a user is member of a group
        :param group_id: Id of the group
        :param username: Username of the user
        :param raise_exception: Raise exception if user is not member of the group
        :return: True if user is member of the group else False"""

        user_id = self.get_user_id_by_username(username=username)
        groups = self.connect.get_user_groups(user_id=user_id)

        for group in groups:
            if group_id == group['id']:
                return True
        if raise_exception:
            LOG.error(
                f"User: {user_id} is not member of any Keycloak Groups: {groups}")
            raise CCPBusinessException(
                message=Message.USER_DOESNT_HAVE_ORG)
        else:
            LOG.debug(
                f"User: {user_id} is not member of any Keycloak Groups: {groups}")
            return False

    @log
    def get_user_roles(self, username: str):
        """Get roles of a user in Keycloak
        :param username: Username
        :return: Roles of the user."""

        user_id = self.get_user_id_by_username(username=username)
        client_id = self.client_service.get_client_uuid()
        user_roles = self.connect.get_client_roles_of_user(user_id, client_id)
        return [role['name'] for role in user_roles]

    @log
    def get_user_groups(self, username: str):
        """Get groups of a user in Keycloak
        :param username: Username
        :return: Roles of the user."""

        user_id = self.get_user_id_by_username(username=username)

        return self.connect.get_user_groups(user_id)

    @log
    def get_user_subgroup(self, username: str):
        """Get subgroups of a group from Keycloak
        :param username: Username
        :return: Subgroup of the user."""

        subgroups: List[str] = []

        user_id = self.get_user_id_by_username(username=username)
        groups = self.connect.get_user_groups(user_id)

        for group in groups:
            if group['path'].count('/') == 2:
                subgroups.append(group)

        return subgroups

    @log
    def logout(self, username: str):
        """Logout a user from Keycloak
        :param username: Username
        :return: None."""

        user_id = self.get_user_id_by_username(username=username)

        self.connect.user_logout(user_id)

    @log
    def generate_access_token(self, refresh_token: str):
        """Logout a user from Keycloak
        :param refresh_token: refresh_token of the logged-in user
        :return: None."""

        headers = {
            Constants.KEYCLOAK_CONTENT_TYPE_HEADER_KEY: Constants.KEYCLOAK_FORM_URLENCODED_TYPE}
        data = {
            'client_id': Constants.KEYCLOAK_UI_CLIENT_ID,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        response = httpx.post(url=Constants.KEYCLOAK_OPENID_CONNECT_TOKEN_URL, headers=headers,
                              data=data, verify=False)
        if response.status_code != status.HTTP_200_OK:
            LOG.error('Error occured during fetching access token')
            raise CCPKeycloakException()

        return response.json()

    @log
    def update_user_attributes(self, username: str, attributes: Dict[str, bool]) -> None:
        """Update user attributes in Keycloak
        :param username: Username
        :param attributes: Dict of attributes
        :return: None."""
        user_id = self.get_user_id_by_username(username=username)
        kc_attributes = {}
        user = self.get_user(username=username)

        if user['attributes']:
            kc_attributes.update(user['attributes'])
        kc_attributes.update(attributes)

        self.connect.update_user(user_id=user_id, payload={
            'attributes': kc_attributes})

    @log
    def get_user_attributes(self, username: str) -> Dict[str, str]:
        """Get user attributes from Keycloak
        :param username: Username
        :return: Dict of attributes."""
        kc_user = self.get_user(username)
        return kc_user['attributes']

    @log
    def grant_roles_to_user(self, username: str, roles: List[str]) -> None:
        """
         Update user role in Keycloak
        :param username: Username
        :param roles: Role name
        :return: None
        """
        user_id = self.get_user_id_by_username(username=username)
        client_id = self.client_service.get_client_uuid()
        kc_roles = self.client_service.get_client_role(roles=roles)

        self.connect.assign_client_role(
            user_id=user_id, client_id=client_id, roles=kc_roles)

    @log
    def delete_user_role(self, username: str, roles: str) -> None:
        """
         Delete user role in Keycloak
        :param username: Username
        :param roles: Role name
        :return: None
        """
        user_id = self.get_user_id_by_username(username=username)
        client_id = self.client_service.get_client_uuid()
        kc_roles = self.client_service.get_client_role(roles=roles)

        self.connect.delete_client_roles_of_user(
            user_id=user_id, client_id=client_id, roles=kc_roles)
