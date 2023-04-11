###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Mohammad Yameen <yameen@coredge.io>, Feb 2023                    #
# Modified by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                  #
###############################################################################
from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.org import OrgService

router = APIRouter()

org_service: OrgService = OrgService()


@router.get("",
            description="Get all organizations.",
            status_code=status.HTTP_200_OK,
            response_description="Organization Response.",
            )
async def get_orgs(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=100, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(False, title="Sort descending", description="Sort in descending order")):
    data, total = await org_service.get_orgs(Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/me",
            description="Get the organization of Logged in user",
            status_code=status.HTTP_200_OK,
            response_description="Organization of Logged in user response"
            )
async def get_logged_in_user_orgs():
    return await org_service.get_logged_in_user_orgs()


@router.get("/{org_id}",
            description="Get organization by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Organization Response.",
            )
async def get_org(org_id: str):
    return await org_service.get_org(org_id)


@router.delete("/{org_id}",
               description="Delete a organization.",
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_org(
        org_id: str
) -> None:
    await org_service.delete_org(org_id)


@router.patch("/{org_id}/members/{username}",
              description="Add a member to an organization.",
              status_code=status.HTTP_204_NO_CONTENT,
              )
async def add_member(
        org_id: str,
        username: str,
        project_id: str
) -> None:
    await org_service.add_member(org_id=org_id, username=username, project_id=project_id)


@router.delete("/{org_id}/members/{username}",
               description="Remove a member from an organization.",
               status_code=status.HTTP_204_NO_CONTENT, )
async def remove_member(
        org_id: str,
        username: str
) -> None:
    await org_service.remove_member(org_id, username)


@router.get("/{org_id}/members",
            description="Get members from an organization.",
            status_code=status.HTTP_200_OK, )
async def get_org_members(
        org_id: str,
) -> List[dict]:
    return await org_service.get_org_members(org_id)
