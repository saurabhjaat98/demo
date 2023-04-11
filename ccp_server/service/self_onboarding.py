###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, March 2023                    #
###############################################################################
from typing import List

from ccp_server.decorators.common import has_role
from ccp_server.kc.authentication import KeycloakAuthService
from ccp_server.kc.group import KeycloakGroupService
from ccp_server.kc.schemas.schemas import User
from ccp_server.kc.user import KeycloakUserService
from ccp_server.schema.v1 import schemas
from ccp_server.service.oidc import Organization
from ccp_server.service.oidc import Project
from ccp_server.service.oidc import UserProfile
from ccp_server.service.org import OrgService
from ccp_server.service.project import ProjectService
from ccp_server.service.providers import Provider
from ccp_server.service.user import UserService
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBusinessException
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
from ccp_server.util.messages import Message
from ccp_server.util.token import TokenInfo
from ccp_server.util.utils import Utils

LOG = KGLogger(__name__)


class SelfOnboardingService(Provider):
    '''
    Organization Onboarding Service
    '''

    def __init__(self):
        self.project_service: ProjectService = ProjectService()
        self.org_service: OrgService = OrgService()
        self.user_service: UserService = UserService()
        self.kc_user_service: KeycloakUserService = KeycloakUserService()
        self.kc_group_service: KeycloakGroupService = KeycloakGroupService()
        self.auth_service: KeycloakAuthService = KeycloakAuthService()

    @log
    async def self_onboarding(self, request: schemas.SelfOnboarding):
        """
        Signup user
        param request: User signup request
        return: User id
        """
        """1. Creating user in Keycloak"""
        user_obj = User(first_name=request.first_name, last_name=request.last_name,
                        email=request.email, roles=[Constants.CCPRole.ORG_ADMIN])
        LOG.debug(
            f"Creating user in Keycloak with user {user_obj}")
        self.kc_user_service.create_user(user=user_obj)

        """2. Setting Default cloud and setting it to the header"""
        default_cloud = Utils.get_default_cloud()
        ccp_context.set_request_data(key=Constants.CCPHeader.CLOUD_ID,
                                     value=default_cloud)

        """ 4. Creating org in Keycloak and Mongo"""
        kc_group_req = schemas.Group(name=request.organization_name)
        LOG.debug(
            f"Creating Organisation {kc_group_req} in Keycloak and Mongo")
        org_id = await self.org_service.create_org(kc_group_req)

        """ 5. Setting org id in the header"""
        group_id = await self.org_service.get_group_id(org_id)
        ccp_context.set_request_data(
            key=Constants.CCPHeader.ORG_ID, value=org_id)
        ccp_context.set_request_data(
            Constants.CCP_ROLES, [Constants.CCPRole.ORG_ADMIN])

        """ 6. Adding user to the group in Keycloak"""
        LOG.debug(f"Adding user: {request.email} in group")
        self.kc_group_service.add_user_to_group(
            group_id=group_id, username=request.email)

        """7. Adding role Org-Admin of the user"""
        LOG.debug(
            f"Adding role as {[Constants.CCPRole.ORG_ADMIN]} of the user: {request.email}")
        await self.org_service.grant_role_to_member(username=request.email, roles=[Constants.CCPRole.ORG_ADMIN])

        """ 8. Sending Verification mail to the user"""
        email_actions: List[str] = ['VERIFY_EMAIL', 'UPDATE_PASSWORD']
        LOG.debug(f'Sending email to the user')
        await self.user_service.update_email_action(request.email, email_actions)

    @has_role(Constants.CCPRole.ORG_ADMIN)
    @log
    async def complete_profile(self, request: schemas.Profile):
        """
        Self Onboarding user and organization.
        :param request: User and Organization meta.
        :return: org_id.
        """
        token = ccp_context.get_logged_in_token()
        token_info: TokenInfo = self.auth_service.tokeninfo(token)
        project_name = Constants.CCPHeader.DEFAULT_PROJECT_NAME
        if token_info.is_profile_completed:
            raise CCPBusinessException(message=Message.PROFILE_COMPLETED)

        username = ccp_context.get_logged_in_user()
        org_obj = await self.user_service.get_user_orgs(username)
        org_id = org_obj[0]['uuid']

        # Set the cloud in context from the request or default in clouds.yaml
        if request.default_cloud:
            default_cloud = Utils.get_default_cloud(request.default_cloud)
            ccp_context.set_request_data(key=Constants.CCPHeader.CLOUD_ID,
                                         value=default_cloud)
            await self.db.update_document_by_uuid(Constants.MongoCollection.ORGANIZATION,
                                                  uid=org_id,
                                                  data_dict={'default_cloud': request.default_cloud})
        else:
            default_cloud = org_obj[0]['default_cloud']
            ccp_context.set_request_data(key=Constants.CCPHeader.CLOUD_ID,
                                         value=default_cloud)

        ccp_context.set_request_data(
            key=Constants.CCPHeader.ORG_ID, value=org_id)
        """Project created with the name as default"""
        project_req = schemas.Project(
            name=project_name)
        project_id = await self.project_service.create_project(project_req, default=True)

        user_obj = self.kc_user_service.get_user(username)
        user = schemas.User(email=user_obj['username'], first_name=user_obj['firstName'],
                            last_name=user_obj['lastName'], roles=[Constants.CCPRole.ORG_ADMIN])
        await self.user_service.create_user(user, project_id=project_id, exist_ok=True)

        self.kc_user_service.update_user_attributes(
            username=username, attributes={'profile_completed': True})

        org = Organization(
            org_id, org_obj[0]['name'], project_id,
            [Project(uuid=project_id, name=project_name, cloud=default_cloud)])

        profile = UserProfile(email=token_info.email, name=token_info.name, roles=token_info.ccp_roles,
                              organizations=[org])
        return profile
