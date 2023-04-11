###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepakpant@coredge.io>, Feb 2023                    #
###############################################################################
from typing import List

from ccp_server.kc.authentication import KeycloakAuthService
from ccp_server.service.org import OrgService
from ccp_server.service.project import ProjectService
from ccp_server.service.user import UserService
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.exceptions import CCPProfileNotCompletedException
from ccp_server.util.exceptions import CCPUnauthenticatedException
from ccp_server.util.exceptions import CCPUnauthorizedException
from ccp_server.util.messages import Message
from ccp_server.util.token import TokenInfo


class Project:

    def __init__(self, uuid: str, name: str, cloud: str):
        self.uuid = uuid
        self.name = name
        self.cloud = cloud


class Organization:

    def __init__(self, uuid: str, name: str, default_project: str, projects: List[Project]):
        self.uuid = uuid
        self.name = name
        self.default_project = default_project
        self.projects = projects


class UserProfile:

    def __init__(self, name: str, email: str, roles: List[str], organizations: List[Organization]):
        self.name = name
        self.email = email
        self.roles = roles
        self.organizations = organizations


class OIDC:
    ADMIN_ROLES = [Constants.CCPRole.SUPER_ADMIN]

    def __init__(self):
        self.auth_service: KeycloakAuthService = KeycloakAuthService()
        self.org_service: OrgService = OrgService()
        self.project_service: ProjectService = ProjectService()
        self.user_service: UserService = UserService()

    async def web_sso(self, token: str = None, token_info: TokenInfo = None) -> UserProfile:

        if not token_info:
            token_info: TokenInfo = self.auth_service.tokeninfo(token)

        #  if token not valid the raise Unauthorized exception
        if not token_info.active:
            raise CCPUnauthorizedException(message=Message.TOKEN_EXPIRED)

        #  if email not verified the raise Unauthenticated exception
        if not token_info.is_email_verified:
            raise CCPUnauthenticatedException(
                message=Message.EMAIL_NOT_VERIFIED)

        if Constants.CCPRole.ORG_ADMIN in token_info.ccp_roles and not token_info.is_profile_completed:
            raise CCPProfileNotCompletedException()

        organizations = []

        # This block will not execute for OIDC.ADMIN_ROLES
        if not any(role.lower() in token_info.ccp_roles for role in OIDC.ADMIN_ROLES):
            try:
                orgs = await self.user_service.get_user_orgs(token_info.email)
                if orgs:
                    for org in orgs:
                        user_projects = await self.user_service.get_user_projects(token_info.email, org['uuid'])
                        if user_projects:
                            _projects = [Project(project['uuid'], project['name'], project['cloud']) for project in
                                         user_projects]
                        else:
                            raise CCPBadRequestException(
                                message=Message.USER_DOESNT_HAVE_PROJECT)
                        organizations.append(Organization(
                            org['uuid'], org['name'], _projects[0].uuid, _projects))
                else:
                    raise CCPBadRequestException(
                        message=Message.USER_DOESNT_HAVE_ORG)
            except CCPBadRequestException as e:
                raise e
            except CCPBadRequestException:
                raise CCPUnauthenticatedException(
                    message=Message.USER_DOESNT_HAVE_ORG)
        profile = UserProfile(email=token_info.email, name=token_info.name, roles=token_info.ccp_roles,
                              organizations=organizations)
        return profile
