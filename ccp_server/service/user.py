###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List

from ccp_server.config.redis import cache
from ccp_server.decorators.common import has_role
from ccp_server.kc.group import KeycloakGroupService
from ccp_server.kc.schemas.schemas import User as KCUser
from ccp_server.kc.user import KeycloakUserService
from ccp_server.provider.models import User as CloudUser
from ccp_server.schema.v1 import schemas
from ccp_server.service.org import OrgService
from ccp_server.service.providers import Provider
from ccp_server.service.storage.storageuser import StorageUserService
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.enums import Status
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils

LOG = KGLogger(__name__)

LOG = KGLogger(__name__)


class UserService(Provider):

    def __init__(self):

        self.kc_user_service: KeycloakUserService = KeycloakUserService()
        self.kc_group_service: KeycloakGroupService = KeycloakGroupService()
        self.org_service: OrgService = OrgService()
        self.storage_user_service: StorageUserService = StorageUserService()

    @log
    @has_role(Constants.CCPRole.ORG_ADMIN, Constants.CCPRole.SUPER_ADMIN)
    async def create_user(self, user_req: schemas.User, project_id: str = None,
                          exist_ok: bool = False, profile_completed: bool = False,
                          notify: bool = False) -> None:
        """ Create the user in keycloak and OpenStack and send a verification mail on the user's email ID.
                :param user_req: User request
                :param project_id: Project id of the user
                :param profile_completed: Profile completed or not
                :param exist_ok: If True, ignore if user already exists
                :param notify: If notify True, send verification email to the user
                :return: user_id"""
        from ccp_server.service.project import ProjectService
        project_service: ProjectService = ProjectService()

        org_id = ccp_context.get_org()

        """get cloud  by org id"""
        cloud = await self.db.get_cloud_by_org_id(org_id)

        LOG.debug(f"Setting cloud as {cloud} in ccp_context ")
        ccp_context.set_request_data(Constants.CCPHeader.CLOUD_ID, cloud)

        if project_id:
            """get project by project id"""
            user_project = await project_service.get_project(project_id)
        else:
            """get default project of org"""
            user_project = await self.org_service.get_default_project(org_id)
        cloud_project_id = user_project['reference_id']
        keycloak_project_id = user_project['external_id']

        """1. User creation in Keycloak"""
        kc_user_req = KCUser(first_name=user_req.first_name, last_name=user_req.last_name, email=user_req.email,
                             mobile_number=user_req.mobile_number, roles=user_req.roles)

        LOG.debug(f"Creating user as {user_req.first_name} in Keycloak")
        self.kc_user_service.create_user(
            kc_user_req, profile_completed=profile_completed, exist_ok=exist_ok)

        """2. User creation in Cloud and attached to the Project if provided and """
        cloud_user_req = CloudUser(name=user_req.email, description=f'{user_req.first_name} {user_req.last_name}',
                                   email=user_req.email, default_project=cloud_project_id)

        LOG.debug(f"Creating user as {user_req.email} in Cloud")
        self.connect.user.create_user(cloud_user_req, exist_ok=exist_ok)

        try:
            """3. User creation in Storage """
            LOG.debug(
                f"Adding user as {user_req.email} in org {org_id}in Storage")
            storage_user_creds = await self.storage_user_service.create_storage_user(first_name=user_req.first_name,
                                                                                     last_name=user_req.last_name,
                                                                                     email=user_req.email,
                                                                                     exist_ok=exist_ok)

            """4. Update User in Keycloak and add storage user creds"""
            LOG.debug(
                f"Adding user as {user_req.email} in org {org_id}in Storage")
            self.kc_user_service.update_user_attributes(
                username=user_req.email, attributes=storage_user_creds)
        except Exception as e:
            LOG.error(
                f"Failed to add user {user_req.email} in Storage. Error: {e}")

        """5. Add user to org"""
        LOG.debug(
            f"Adding user as {user_req.email} in org {org_id}in Keycloak")
        await self.org_service.add_member(org_id=org_id, username=user_req.email, project_id=project_id)

        """6. Add user into the Sub-group in Keycloak"""
        LOG.debug(
            f"Adding user as {user_req.email} into subgroup of org {org_id} in Keycloak")
        self.kc_group_service.add_user_to_group(
            keycloak_project_id, user_req.email)

        """7. Add role to user"""
        LOG.debug(
            f"Adding role as {user_req.roles} of the user: {user_req.email}")
        await self.org_service.grant_role_to_member(username=user_req.email, roles=user_req.roles)

        if notify:
            """8. Send the user email to verification and to set password"""
            email_actions: List[str] = ['VERIFY_EMAIL', 'UPDATE_PASSWORD']
            await self.update_email_action(user_req.email, email_actions)

    @log
    @cache()
    async def get_user(self, username: str) -> schemas.User:
        """Get a user from Keycloak"""
        user = self.kc_user_service.get_user(username)
        attributes = user.get('attributes', {})
        dt_object = Utils.to_utc_datetime(user['createdTimestamp'])
        user = {
            'email': user['email'],
            'first_name': user['firstName'],
            'last_name': user['lastName'],
            'username': user['username'],
            'email_verified': user['emailVerified'],
            'created_at': dt_object.strftime(Constants.TIMESTAMP_FORMAT),
        }
        user_roles = self.kc_user_service.get_user_roles(username)
        user['roles'] = user_roles

        for key in attributes:
            user[key] = attributes[key][0]

        return user

    @log
    @cache()
    async def get_user_from_cloud(self, username: str) -> schemas.User:
        """Get a user from Cloud"""
        return self.connect.user.get_user(username)

    @log
    async def update_user(self, username: str, user: schemas.User) -> None:
        """Update a user in Keycloak
        :param username: Username
        :param user: User object.
        :return: None"""

        kc_user_req = KCUser(first_name=user.first_name,
                             last_name=user.last_name, email=user.email)
        self.kc_user_service.update_user(kc_user_req)

    @log
    async def delete_user(self, username: str) -> None:
        """Delete a user from Keycloak and OpenStack
        :param username: Username
        :return: None"""

        # Delete user from Keycloak
        self.kc_user_service.delete_user(username)

        # Delete user from OpenStack
        self.connect.user.delete_user(username)

    @log
    async def grant_roles(self, username: str, roles: List[str]) -> None:
        """Grant role to a user in Keycloak and Openstack
        :param username: Username
        :param roles: Roles name
        :return: None."""

        # assign role in Keycloak
        self.kc_user_service.grant_roles(username, roles)

    @log
    async def revoke_roles(self, username: str, roles: List[str]) -> None:
        """Revoke role to a user in Keycloak and Openstack
        :param username: Username
        :param roles: Roles name
        :return: None."""

        # revoke role in Keycloak
        self.kc_user_service.revoke_roles(username, roles)

    @log
    @has_role(Constants.CCPRole.ORG_ADMIN, Constants.CCPRole.MEMBER)
    @cache()
    async def get_users(self, query_str, page, size, sort_by, sort_desc) -> List[Dict]:
        """Get a list of users from Keycloak
        :return: List of users."""

        query = {'first': page, 'max': size}
        org_id = ccp_context.get_org()
        users = await self.org_service.get_org_members(org_id=org_id, query=query)

        return users

    @log
    async def update_email_action(self, username: str, actions: List[str]) -> None:
        """Send email to user to verify email address and set the password
        :param username: Username
        :param actions: Actions to be performed.
        :return: None."""

        group_id = await self.org_service.get_group_id(org_id=ccp_context.get_org())
        self.kc_user_service.is_user_exists_in_group(
            group_id, username, raise_exception=True)

        self.kc_user_service.update_email_action(username, actions)

    @log
    @cache()
    async def get_user_orgs(self, username: str):
        """Get a list of groups from Keycloak"""
        groups = self.kc_user_service.get_user_groups(username)
        group_ids = [group['id'] for group in groups]

        return await self.db.get_document_by_projection_and_filter(Constants.MongoCollection.ORGANIZATION,
                                                                   projection_dict={
                                                                       '_id': 0, },
                                                                   filter_dict={'external_id': {'$in': group_ids},
                                                                                'active': Status.ACTIVE.value})

    @log
    async def get_logged_in_user_projects(self) -> List[Dict]:
        """Get a list of projects from of logged-in user"""
        return await self.get_user_projects(username=ccp_context.get_logged_in_user())

    @log
    @cache()
    async def get_user_projects(self, username: str, org_id: str = None) -> List[Dict]:
        """Get a list of projects for provided user
        :param username: Username
        :param org_id: Organization id
        :return: List of projects."""

        subgroups = self.kc_user_service.get_user_subgroup(username)
        if subgroups:
            external_ids = [subgroup['id'] for subgroup in subgroups]
            projects, _ = await self.db.get_document_list_by_ids(Constants.MongoCollection.PROJECT, org_id=org_id,
                                                                 exclude_project=True)

            return [project for project in projects if project.get('external_id') in external_ids]

    @log
    async def logout(self) -> None:
        """Logout from Keycloak"""
        self.kc_user_service.logout(ccp_context.get_logged_in_user())

    @log
    async def generate_access_token(self, refresh_token: str) -> None:
        """Logout from Keycloak"""
        return self.kc_user_service.generate_access_token(refresh_token)
