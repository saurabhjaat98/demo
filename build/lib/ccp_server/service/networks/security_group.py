###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from typing import Dict

from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.provider import models as provider_models
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class SecurityGroupService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.SECURITY_GROUP

    @log
    async def create_security_group(self, project_id: str, security_group: schemas.SecurityGroup) -> str:
        """This method is used to create a Security Group in cloud and mongo."""

        """Check for security group if already exist"""
        await self.db.check_document_by_name(Constants.MongoCollection.SECURITY_GROUP, security_group.name,
                                             project_id=project_id, raise_exception=True)

        secg_model: provider_models.SecurityGroup = provider_models.SecurityGroup(
            name=Utils.generate_unique_str(),
            description=security_group.name
        )

        """Save the security group in the OpenStack"""
        cloud_response = await self.connect.security_group.create_security_group(
            secg_model)

        """Save the security group in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=security_group.name,
                                              description=security_group.description,
                                              project_id=project_id)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    async def list_security_groups_by_project_id(self, project_id: str = None, pageable: Pageable = None):
        """ list all the security_group in mongo
        :return: List[Dict] List of all the security groups in the database
        """
        return await self.db.get_document_list_by_ids(
            collection_name=self.collection,
            pageable=pageable,
            project_id=project_id
        )

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_security_groups(self, pageable: Pageable = None, use_db: StrictBool = True):
        """ list all the security_group in mongo and cloud
        :return: List[Dict] List of all the security groups in the database and cloud
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                exclude_project=True
            )
        else:
            cloud_res = await self.connect.security_group.list_all_security_groups()
            return cloud_res, len(cloud_res)

    @log
    async def get_security_group(self, project_id: str, security_group_id: str) -> Dict:
        """
        :param: security_group_id -> str
        :return: Dict
        """
        return await self.db.get_document_by_ids(collection_name=self.collection,
                                                 uid=security_group_id,
                                                 project_id=project_id,
                                                 raise_exception=True)

    @log
    async def delete_security_group(self, project_id: str, security_group_id) -> None:
        """This method is used to delete the security group from mongo.
        :param security_group_id: id of the security group
        :param project_id: id of the project
        :return: None
        """

        """DB Response"""
        sg_db_res = await self.db.get_document_by_ids(collection_name=self.collection,
                                                      uid=security_group_id,
                                                      project_id=project_id,
                                                      raise_exception=True)
        """Cloud Response"""
        await self.connect.security_group.delete_security_group(sg_db_res["reference_id"])

        await self.db.soft_delete_document_by_uuid(Constants.MongoCollection.SECURITY_GROUP, security_group_id)
