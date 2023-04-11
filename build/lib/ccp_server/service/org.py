###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List
from typing import Tuple

from ccp_server.db.models import Organization
from ccp_server.decorators.common import has_role
from ccp_server.kc.group import KeycloakGroupService
from ccp_server.kc.schemas.schemas import Group as KCGroup
from ccp_server.kc.user import KeycloakUserService
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBusinessException
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils

LOG = KGLogger(__name__)


class OrgService(Provider):
    def __init__(self):
        self.kc_group_service: KeycloakGroupService = KeycloakGroupService()
        self.kc_user_service: KeycloakUserService = KeycloakUserService()

    @log
    async def create_org(self, org_req: schemas.Group):
        kc_group_req = KCGroup(name=org_req.name)

        # Raise exception if the org already exists with the same name
        await self.db.check_document_by_name(Constants.MongoCollection.ORGANIZATION, org_req.name, raise_exception=True)

        """Save the group in Keycloak"""
        group_id = self.kc_group_service.create_group(kc_group_req)

        """Save the group/Organization in mongo db"""
        mongo_data = Organization(
            name=org_req.name,
            description=org_req.description,
            default_cloud=ccp_context.get_cloud(),
            cloud=ccp_context.get_cloud(),
            external_id=group_id,
            communication_address=org_req.communication_address,
            billing_address=org_req.billing_address,
            tan_number=org_req.tan_number,
            gst_number=org_req.gst_number
        )
        _, doc_id = await self.db.write_document(Constants.MongoCollection.ORGANIZATION, mongo_data)
        return doc_id

    @log
    async def get_org(self, org_id: str = None, org_name: str = None) -> Dict:
        """Get org details by id
        :param org_id: Org id
        :param org_name: Org Name
        :return: Org details
        """
        if not org_id and not org_name:
            LOG.error(f"Both Org id and Org name can't be None or blank")
            raise CCPBusinessException(f"Organisation can't be None or blank")
        return await self.db.get_document_by_ids(Constants.MongoCollection.ORGANIZATION, org_id, exclude_org=True)

    async def get_logged_in_user_orgs(self) -> Tuple[
            List[Dict], int]:
        """
        Get logged user org details
        :param pageable: Pageable object
        :return: Pageable object
        """
        groups = self.kc_user_service.get_user_groups(
            ccp_context.get_logged_in_user())
        group_ids = [group['id'] for group in groups]
        return await self.db.get_document_list_by_ids(Constants.MongoCollection.ORGANIZATION,
                                                      projection_dict={
                                                          'external_id': 0, },
                                                      filter_dict={
                                                          'external_id': {'$in': group_ids}},
                                                      exclude_org=True)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN)
    async def get_orgs(self, pageable: Pageable = None) -> Tuple[
            List[Dict], int]:
        """Get org details by id
        :return: List of Orgs based on filter and pagination
        """
        return await self.db.get_document_list_by_ids(
            collection_name=Constants.MongoCollection.ORGANIZATION,
            pageable=pageable,
            exclude_org=True)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def delete_org(self, org_id: str) -> None:
        """Delete org by id
        :param org_id: Org id
        :return: None
        """
        await self.db.soft_delete_document_by_uuid(Constants.MongoCollection.ORGANIZATION, org_id)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def add_member(self, org_id: str, username: str, project_id: str) -> None:
        """Add member to org
        :param org_id: Org id
        :param username: Username of the user
        :param project_id : Project id
        :return: None
        """
        group_id = await self.get_group_id(org_id)
        self.kc_group_service.add_user_to_group(
            group_id=group_id, username=username)

        cloud = await self.db.get_cloud_by_org_id(org_id=org_id)
        ccp_context.set_request_data(Constants.CCPHeader.CLOUD_ID, cloud)

        from ccp_server.service.project import ProjectService
        project_service = ProjectService()
        await project_service.add_member(project_id=project_id, username=username, role=Constants.CCPRole.MEMBER)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def remove_member(self, org_id: str, username: str) -> None:
        """Remove member from org.
        :param org_id: Org id
        :param username: Username of the user
        :return: None
        """

        group_id = await self.get_group_id(org_id)
        self.kc_group_service.remove_user_from_group(
            group_id=group_id, username=username)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def grant_role_to_member(self, username: str, roles: List[str]) -> None:
        """Grant role to member
        :param org_id: Org id
        :param username: Username of the user
        :param roles: name of the role
        :return: None
        """

        self.kc_user_service.grant_roles(username, roles)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def revoke_role_from_member(self, org_id: str, username: str, role_name: str) -> None:
        """Revoke role from member
        :param org_id: Org id
        :param username: Username of the user
        :param role_name: role of the user
        :return: None
        """

        await self.kc_user_service.revoke_roles(username, role_name)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def get_org_members(self, org_id: str, query: dict = {}, subgroup_id: str = None) -> List[Dict]:
        """Get members of org.
        :param query: dict
        :param org_id: org id
        :return: List of members
        """
        group_id = await self.get_group_id(org_id)

        return await self.get_group_members(group_id, query)

    async def get_group_members(self, group_id, query) -> List[Dict]:
        """Get members of group or a subgroup.
        :param group_id: group id
        :param query: dict
        :return: List of members
        """
        members = self.kc_group_service.get_group_members(
            group_id=group_id, query=query)
        users: List[Dict] = []
        # Convert Keycloak response into user details
        for member in members:
            user_roles = self.kc_user_service.get_user_roles(
                member['username'])

            # Convert the timestamp to seconds then in datetime format
            dt_object = Utils.to_utc_datetime(member['createdTimestamp'])
            user = {
                'email': member['email'],
                'first_name': member['firstName'],
                'last_name': member['lastName'],
                'username': member['username'],
                'email_verified': member['emailVerified'],
                'created_at': dt_object.strftime(Constants.TIMESTAMP_FORMAT),
                'roles': user_roles
            }
            attributes = member.get('attributes', {})
            for key in attributes:
                user[key] = attributes[key][0]
            users.append(user)
        return users

    async def get_group_id(self, org_id):
        org = await self.get_org(org_id)
        group_id = org['external_id']
        return group_id

    async def get_default_project(self, org_id):
        """This function used to get default project of an organization"""
        org_projects = await self.db.get_document_by_projection_and_filter(
            collection_name=Constants.MongoCollection.PROJECT,
            filter_dict={'org_id': org_id, 'default': True},
        )
        if org_projects:
            return org_projects[0]
        else:
            LOG.error(f"Organization {org_id} does not have default project")
            raise CCPBusinessException(
                message=f"Organization {org_id} does not have default project")
