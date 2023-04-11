###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from ccp_server.decorators.common import has_role
from ccp_server.kc.user import KeycloakUserService
from ccp_server.schema.v1 import schemas
from ccp_server.service.org import OrgService
from ccp_server.service.project import ProjectService
from ccp_server.service.providers import Provider
from ccp_server.service.user import UserService
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class OnboardingService(Provider):
    '''
    Organization Onboarding Service
    '''

    def __init__(self):
        self.kc_user_service: KeycloakUserService = KeycloakUserService()
        self.project_service: ProjectService = ProjectService()
        self.org_service: OrgService = OrgService()
        self.user_service: UserService = UserService()

    @has_role(Constants.CCPRole.SUPER_ADMIN)
    @log
    async def onboarding(self, request: schemas.Onboarding):
        default_cloud = Utils.get_default_cloud(request.default_cloud)

        # Set the cloud in context from the request or default in clouds.yaml
        ccp_context.set_request_data(key=Constants.CCPHeader.CLOUD_ID,
                                     value=default_cloud)

        """1. Group created with the name of organization"""
        group_req = schemas.Group(name=request.name, description=request.description,
                                  communication_address=request.communication_address,
                                  billing_address=request.billing_address,
                                  tan_number=request.tan_number, gst_number=request.gst_number)

        org_id = await self.org_service.create_org(group_req)

        ccp_context.set_request_data(
            key=Constants.CCPHeader.ORG_ID, value=org_id)

        """3. Project created with the name of organization"""
        project_req = schemas.Project(
            name=Constants.CCPHeader.DEFAULT_PROJECT_NAME, description=request.description)
        project_id = await self.project_service.create_project(project_req, default=True)

        """4. User created with the name of organization"""
        for user in request.users:
            await self.user_service.create_user(user, project_id=project_id, profile_completed=True, exist_ok=True,
                                                notify=True)
        return org_id
