from fastapi import Depends
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from ccp_server.kc.authentication import KeycloakAuthService
from ccp_server.kc.user import KeycloakUserService
from ccp_server.service.oidc import OIDC
from ccp_server.service.oidc import UserProfile
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPNotFoundException
from ccp_server.util.exceptions import CCPUnauthenticatedException
from ccp_server.util.exceptions import CCPUnauthorizedException
from ccp_server.util.messages import Message
from ccp_server.util.token import TokenInfo
from ccp_server.util.utils import Utils

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=Constants.KEYCLOAK_OPENID_CONNECT_TOKEN_URL)

auth_service: KeycloakAuthService = KeycloakAuthService()
user_service: KeycloakUserService = KeycloakUserService()


async def authenticate(request: Request, token: str = Depends(oauth2_scheme)) -> None:
    token_info: TokenInfo = auth_service.tokeninfo(token)

    #  if token not valid the raise Unauthorized exception
    if not token_info.active:
        raise CCPUnauthorizedException(
            message=Message.TOKEN_EXPIRED)

    #  if email not verified the raise Unauthenticated exception
    if not token_info.is_email_verified:
        raise CCPUnauthenticatedException(
            message=Message.EMAIL_NOT_VERIFIED)

    cloud_id = request.headers.get(Constants.CCPHeader.CLOUD_ID, None)
    org_id = request.headers.get(Constants.CCPHeader.ORG_ID, None)
    project_id = request.state.__getattr__(Constants.CCPHeader.PROJECT_ID)

    #  if cloud not valid raise Unauthenticated exception
    if cloud_id and cloud_id not in Utils.load_supported_clouds():
        """raise cloud not found exception"""
        raise CCPUnauthenticatedException(
            message=Message.CLOUD_NOT_VALID)

    if org_id:
        user_profile: UserProfile = await OIDC().web_sso(token_info=token_info)
        orgs = [org for org in user_profile.organizations if org_id == org.uuid]
        org = orgs[0] if orgs else None

        #  if org not valid raise Unauthenticated exception
        if org is None:
            raise CCPNotFoundException(
                message=Message.ORG_NOT_VALID)

        if project_id:
            projects = [
                project for project in org.projects if project_id == project.uuid]
            project = projects[0] if projects else None

            #  if project not valid raise Unauthenticated exception
            if not project:
                raise CCPNotFoundException(
                    message=Message.PROJECT_NOT_VALID)
            elif hasattr(project, 'reference_id'):
                # set the cloud-project-id in ccp_context
                request.state.__setattr__(
                    Constants.CLOUD_PROJECT_ID, project['reference_id'])

    # set the ceph user access key and secret key in ccp_context if user profile is complete
    if Constants.CCPRole.SUPER_ADMIN not in token_info.ccp_roles:
        user_attributes = user_service.get_user_attributes(token_info.email)
        if user_attributes.get(Constants.CEPH_USER_ACCESS_KEY) and\
                user_attributes.get(Constants.CEPH_USER_SECRET_KEY):
            request.state.__setattr__(
                Constants.CEPH_USER_ACCESS_KEY, user_attributes.get(Constants.CEPH_USER_ACCESS_KEY)[0])
            request.state.__setattr__(
                Constants.CEPH_USER_SECRET_KEY, user_attributes.get(Constants.CEPH_USER_SECRET_KEY)[0])

    # set the logged-in user username in ccp_context
    request.state.__setattr__(Constants.USERNAME, token_info.username)

    # set the logged-in user roles in request scope
    request.state.__setattr__(Constants.CCP_ROLES, token_info.ccp_roles)

    # set the logged-in user token in request scope
    request.state.__setattr__(Constants.LOGGED_IN_USER_TOKEN, token)
