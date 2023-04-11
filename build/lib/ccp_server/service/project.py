###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Mohammad Yameen <yameen@coredge.io>, Feb 2023                    #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                    #
###############################################################################
from typing import Dict
from typing import List
from typing import Tuple

from pydantic.types import StrictBool

import ccp_server.provider.models as models
from ccp_server.decorators.common import duplicate_name
from ccp_server.decorators.common import has_role
from ccp_server.kc.group import KeycloakGroupService
from ccp_server.kc.schemas.schemas import Group as KCGroup
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.org import OrgService
from ccp_server.service.providers import Provider
from ccp_server.service.user import UserService
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils

LOG = KGLogger(__name__)


class ProjectService(Provider):

    def __init__(self):
        self.kc_group_service: KeycloakGroupService = KeycloakGroupService()
        self.org_service: OrgService = OrgService()
        self.user_service: UserService = UserService()

    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    @duplicate_name(collection=Constants.MongoCollection.PROJECT)
    @log
    async def create_project(self, project: schemas.Project, default: bool = False) -> str:
        """generate a random UUID for the cloud project name"""
        cloud_project_name = Utils.generate_unique_str()

        # Create project in Keycloak as a subgroup
        kc_sub_group_req = KCGroup(name=project.name)
        kc_group_id = await self.org_service.get_group_id(ccp_context.get_org())

        LOG.debug(f"Creating project in Keycloack with name: {project.name}")
        sub_group_id = self.kc_group_service.create_sub_group(
            kc_sub_group_req, parent=kc_group_id)

        cloud_model: models.Project = models.Project(
            name=cloud_project_name,
            description=project.name
        )

        LOG.debug(
            f"Creating the project in the Cloud with name: {cloud_project_name}")
        project_obj = await self.connect.project.create_project(cloud_model)
        LOG.debug(f"Saving the project in the Mongo with name: {project.name}")
        db_model = self.db.populate_db_model(project_obj, name=project.name, description=project.description,
                                             external_id=sub_group_id, default=default, tags=project.tags)
        project_id = await self.db.write_document_with_default_details(Constants.MongoCollection.PROJECT, db_model)
        logged_user = ccp_context.get_logged_in_user()

        LOG.debug(
            f"Adding user: {logged_user} as member in Cloud and Keycloak for project_id:{project_id}")
        await self.add_member(project_id=project_id, username=logged_user, role=Constants.CCPRole.MEMBER)

        return project_id

    @log
    async def list_project(self, pageable: Pageable, use_db: StrictBool = True) -> Tuple[
            List[Dict], int]:

        """Get project details by id
        :return: List of Project based on filter and pagination
        """
        if use_db:
            return await self.db.get_document_list_by_ids(Constants.MongoCollection.PROJECT, pageable=pageable)
        else:
            cloud_res = await self.connect.project.list_projects()
            return cloud_res, len(cloud_res)

    @log
    async def get_project(self, project_id: str) -> Dict:
        """Fetching cloud and org from thread_local
        :param project_id: str
        :return: Dict
        """

        return await self.db.get_document_by_ids(Constants.MongoCollection.PROJECT, project_id, exclude_project=True)

    @log
    async def update_project(self, project_id: str, request) -> None:
        """Update the project name and description in mongo db only if the project_id is valid.
        :param project_id: str
        :param request: ObjectUpdate Request body
        :return: None"""

        """ get the project from the mongo db and update"""
        await self.db.update_document_by_uuid(Constants.MongoCollection.PROJECT,
                                              uid=project_id,
                                              data_dict=request.dict(include={'name', 'description', 'tags'}))

    @log
    async def delete_project(self, project_id) -> None:
        """Delete the project from the mongo db
        :param project_id: str
        :return: None"""

        await self.db.soft_delete_document_by_uuid(Constants.MongoCollection.PROJECT, project_id)

    @log
    async def add_member(self, project_id: str, username: str, role: str) -> None:
        """Add member to project means adding member to Keycloak group and Project in OpenStack
        :param role:str
        :param project_id: str
        :param username: str
        :return: None"""

        project = await self.get_project(project_id)

        # Add member to Keycloak Subgroup
        self.kc_group_service.add_user_to_group(
            project['external_id'], username)

        # Check user exist in Cloud
        cloud_project_id = project['reference_id']
        cloud_user = await self.user_service.get_user_from_cloud(username=username)

        if not cloud_user:
            self.user_service.connect.user.create_user(user=models.User(email=username, name=username,
                                                                        default_project=cloud_project_id,
                                                                        role=role))
        else:
            # Add member to Project in Cloud
            await self.connect.project.add_member(cloud_project_id, username, role)

    @log
    async def remove_member(self, project_id: str, username: str, role: str) -> None:
        """Remove member from project means removing member from Project in OpenStack
        :param role:
        :param project_id: str
        :param username: str
        :return: None"""

        project = await self.get_project(project_id)

        # Remove member from Keycloak Subgroup
        self.kc_group_service.remove_user_from_group(
            project['external_id'], username)

        # Remove member from Project in OpenStack
        cloud_project_id = project['reference_id']
        await self.connect.project.remove_member(cloud_project_id, username, role)

    @log
    async def get_project_members(self, project_id: str) -> List[Dict]:
        """Fetch project members from Keycloak group
        :param project_id: str
        :return: List[Dict]
        """
        query: dict = {}
        project = await self.get_project(project_id)

        return await self.org_service.get_group_members(project['external_id'], query)
