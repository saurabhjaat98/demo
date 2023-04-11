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
from ccp_server.service.networks.security_group import SecurityGroupService
from ccp_server.util.constants import Constants

router = APIRouter()
security_group_service: SecurityGroupService = SecurityGroupService()


@router.post("/projects/{project_id}/security-groups",
             description="Create security group.",
             status_code=status.HTTP_201_CREATED,
             response_description="Security Group Creation Response.",
             response_model=None
             )
async def create_security_group(project_id: str, request: schemas.SecurityGroup) -> IDResponse:
    """
    Create security group.
    :param project_id: Project ID.
    :param request: Request body.
    :return: Security Group ID.
    """
    doc_id = await security_group_service.create_security_group(project_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/security-groups",
            description="list all security groups for a project.",
            status_code=status.HTTP_200_OK,
            response_description="Security Groups Response.",
            )
async def list_security_groups_by_project_id(
        project_id: str,
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(
            1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order")):
    """
    list all security groups for a project.
    :param project_id: Project ID.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items per page.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: Security Groups.
    """
    data, total = await security_group_service.list_security_groups_by_project_id(project_id,
                                                                                  Pageable(query_str, page, size,
                                                                                           sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/security-groups",
            description="list all security groups for an org.",
            status_code=status.HTTP_200_OK,
            response_description="Security Groups Response.",
            )
async def list_all_security_groups(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(
            1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order")):
    """
    list all security groups for an org.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items per page.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: Security Groups.
    """
    data, total = await security_group_service.list_all_security_groups(
        Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/security-groups/{security_group_id}",
            description="Get security group by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Security Group Response.",
            )
async def get_security_group(project_id: str, security_group_id: str) -> dict:
    """
    Get security group by ID.
    :param project_id: Project ID.
    :param security_group_id: Security Group ID.
    :return: Security Group.
    """
    return await security_group_service.get_security_group(project_id=project_id, security_group_id=security_group_id)


@router.delete("/projects/{project_id}/security-groups/{security_group_id}",
               description="Delete a security group.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Security group delete Response.",
               )
async def delete_security_group(project_id: str, security_group_id: str):
    """
    Delete a security group.
    :param project_id: Project ID.
    :param security_group_id: Security Group ID.
    :return: None.
    """
    await security_group_service.delete_security_group(project_id=project_id, security_group_id=security_group_id)
