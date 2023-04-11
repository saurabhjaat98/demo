###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
###############################################################################
from __future__ import annotations

from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.networks.security_group_rule import SecurityGroupRuleService
from ccp_server.util.constants import Constants

router = APIRouter()
security_group_rule_service: SecurityGroupRuleService = SecurityGroupRuleService()


@router.post("/projects/{project_id}/security-groups/{security_group_id}/security-group-rules",
             description="Create security group rule for a security-group.",
             status_code=status.HTTP_201_CREATED,
             response_description="Security group rule Creation Response.",
             response_model=None
             )
async def create_security_group_rule(project_id: str, security_group_id,
                                     request: schemas.SecurityGroupRule
                                     ) -> IDResponse:
    """
    Create security group rule.
    :param project_id: Project ID.
    :param request: Request body.
    :param security_group_id: Security group ID.
    :return: ID of created security group rule.
    """
    doc_id = await security_group_rule_service.create_security_group_rule(project_id, security_group_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/security-groups/{security_group_id}/security-group-rules",
            description="Get all security group rules for a security-group.",
            status_code=status.HTTP_200_OK,
            response_description="Security group rules Response.",
            )
async def list_security_group_rules(project_id: str, security_group_id: str,
                                    query_str: str = Query(
                                        None, title="Search", description="Search item by name or description"),
                                    page: int = Query(
                                        1, ge=1, title="Page", description="Page number"),
                                    size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                                                      description="Number of items to return"),
                                    sort_by: List[str] = Query(
                                        None, title="Sort by", description="Sort by fields (comma-separated list)"),
                                    sort_desc: bool = Query(False, title="Sort descending",
                                                            description="Sort in descending order")):
    data, total = await security_group_rule_service.list_security_group_rules(
        project_id, security_group_id, Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/security-groups/{security_group_id}/security-group-rules/{security_group_rule_id}",
            description="Get security group rule by ID for a security-group.",
            status_code=status.HTTP_200_OK,
            response_description="Security group rule Response.",
            )
async def get_security_group_rule(project_id: str, security_group_id: str, security_group_rule_id: str) -> dict:
    """
    Get security group rule by ID.
    :param project_id: Project ID.
    :param security_group_id: Security group ID.
    :param security_group_rule_id: Security group rule ID.

    """
    return await security_group_rule_service.get_security_group_rule(project_id=project_id,
                                                                     security_group_id=security_group_id,
                                                                     security_group_rule_id=security_group_rule_id)


@router.delete(
    "/projects/{project_id}/security-groups/{security_group_id}/security-group-rules/{security_group_rule_id}",
    description="Delete a security group rule for a security-group.",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Security group rule delete Response.",
)
async def delete_security_group_rule(project_id: str, security_group_id: str, security_group_rule_id: str):
    """
    Delete a security group rule for a project.
    :param project_id: Project ID.
    :param security_group_id: Security group ID.
    :param security_group_rule_id: Security group rule ID.
    """
    await security_group_rule_service.delete_security_group_rule(project_id=project_id,
                                                                 security_group_id=security_group_id,
                                                                 security_group_rule_id=security_group_rule_id)
