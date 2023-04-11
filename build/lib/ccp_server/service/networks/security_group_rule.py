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
from ccp_server.provider import models as provider_models
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log


class SecurityGroupRuleService(Provider):

    @log
    async def create_security_group_rule(self, project_id: str, security_group_id: str,
                                         security_group_rule: schemas.SecurityGroupRule) -> str:
        """This method is used to create a security group rule in cloud and mongo."""

        """ Project Meta """
        project_db_response = await self.db.get_document_by_uuid(Constants.MongoCollection.PROJECT,
                                                                 uid=project_id, raise_exception=True)

        """ Security Group Meta """
        securitygroup_db_response = await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.SECURITY_GROUP,
            uid=security_group_id, project_id=project_id, raise_exception=True)

        """ Remote Security Group Meta """
        remote_security_group_db_response = None
        if security_group_rule.remote_group_id:
            remote_security_group_db_response = await self.db.get_document_by_ids(
                collection_name=Constants.MongoCollection.SECURITY_GROUP,
                uid=security_group_rule.remote_group_id, project_id=project_id, raise_exception=True)

        """ Check for security group rule if already exist with same name"""
        await self.db.check_document_by_name(
            collection_name=Constants.MongoCollection.SECURITY_GROUP_RULE,
            name=security_group_rule.name,
            project_id=project_id,
            filter_dict={"security_group_id": security_group_id},
            raise_exception=True)

        security_group_rule_model: provider_models.SecurityGroupRule = provider_models.SecurityGroupRule(
            security_group=securitygroup_db_response['reference_id'],
            port_range_min=security_group_rule.port_range_min,
            port_range_max=security_group_rule.port_range_max,
            ethertype=security_group_rule.ethertype,
            protocol=security_group_rule.protocol,
            direction=security_group_rule.direction,
            remote_ip_prefix=security_group_rule.remote_ip_prefix,
            remote_group_id=remote_security_group_db_response[
                'reference_id'] if security_group_rule.remote_group_id else None,
            project_id=project_db_response['reference_id'],
            description=security_group_rule.name
        )

        """Save the security group rule in the OpenStack"""
        cloud_response = await self.connect.security_group_rule.create_security_group_rule(
            security_group_rule_model)

        """Save the security group rule in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=security_group_rule.name,
                                              description=security_group_rule.description,
                                              project_id=project_id,
                                              security_group_id=security_group_id)
        return await self.db.write_document_with_default_details(
            Constants.MongoCollection.SECURITY_GROUP_RULE, db_model)

    @log
    async def list_security_group_rules(self, project_id: str, security_group_id: str, pageable: Pageable = None,
                                        use_db: StrictBool = True):
        """ Fetch all the security group rules for the given security group
        :return: List[Dict] List of all the security group rules in the database
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=Constants.MongoCollection.SECURITY_GROUP_RULE,
                project_id=project_id,
                pageable=pageable,
                filter_dict={'security_group_id': security_group_id},
            )
        else:
            db_response = await self.db.get_document_by_ids(Constants.MongoCollection.SECURITY_GROUP,
                                                            uid=security_group_id,
                                                            raise_exception=True
                                                            )
            mapper_res = await self.connect.security_group_rule.list_security_group_rules(
                security_group_id=db_response['reference_id'])
            return mapper_res, len(mapper_res)

    @log
    async def get_security_group_rule(self, project_id: str, security_group_id: str,
                                      security_group_rule_id: str) -> Dict:
        """
        :param: security_group_rule_id -> str
        :param: security_group_id -> str
        :param: project_id -> str
        :return: Dict
        """
        return await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.SECURITY_GROUP_RULE,
            uid=security_group_rule_id,
            project_id=project_id,
            filter_dict={'security_group_id': security_group_id},
            raise_exception=True)

    @log
    async def delete_security_group_rule(self, project_id: str, security_group_id: str, security_group_rule_id) -> None:
        """This method is used to delete the security group rule.
        :param project_id: str
        :param security_group_id: str
        :param security_group_rule_id: id of the security group rule
        :return: None
        """
        """ Security Group Rules Meta """
        sgr_db_response = await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.SECURITY_GROUP_RULE,
            uid=security_group_rule_id,
            project_id=project_id,
            filter_dict={'security_group_id': security_group_id},
            raise_exception=True)

        await self.connect.security_group_rule.delete_security_group_rule(
            security_group_rule_id=sgr_db_response['reference_id'],
        )

        await self.db.soft_delete_document_by_uuid(Constants.MongoCollection.SECURITY_GROUP_RULE,
                                                   security_group_rule_id)
