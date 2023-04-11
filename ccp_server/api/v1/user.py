###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Shubham Kumar <shubhamkumar@coredge.io>, Feb 2023                #
###############################################################################
from typing import Dict
from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status
from fastapi.responses import JSONResponse

from ccp_server.schema.v1 import schemas
from ccp_server.service.user import UserService
from ccp_server.util import ccp_context

router = APIRouter()

user_service: UserService = UserService()


@router.post("",
             description="Create user.",
             status_code=status.HTTP_204_NO_CONTENT,
             response_description="USer Creation Response.",
             )
async def create_user(
        request: schemas.User,
):
    await user_service.create_user(request, project_id=request.project_id, notify=True)


@router.get("",
            description="Get all users belongs to the organization.",
            status_code=status.HTTP_200_OK,
            response_description="User Response.",
            )
async def get_users(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=0, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=100, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order")
) -> JSONResponse:
    users = await user_service.get_users(query_str, page, size, sort_by, sort_desc)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router.get("/me",
            description="Get logged in user details.",
            status_code=status.HTTP_200_OK,
            response_description="User Response.",
            )
async def get_logged_in_user() -> JSONResponse:
    return await user_service.get_user(ccp_context.get_logged_in_user())


@router.get('/me/projects', description="get logged-in user's projects",
            status_code=status.HTTP_200_OK)
async def get_projects_users() -> List[Dict]:
    return await user_service.get_logged_in_user_projects()


@router.get("/{username}",
            description="Get user belongs to the organization.",
            status_code=status.HTTP_200_OK,
            response_description="User Response.",
            )
async def get_user(username: str) -> JSONResponse:
    users = await user_service.get_user(username)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router.put("/{username}/email-actions",
            description="Take email action. Possible actions are: VERIFY_EMAIL, UPDATE_PASSWORD",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="User Response.",
            )
async def perform_user_action(username: str,
                              actions: List[str] = Query(
                                  title="action",
                                  description="Email action")) -> JSONResponse:
    await user_service.update_email_action(username, actions)


@router.put("/{username}/projects",
            description="Take email action. Possible actions are: VERIFY_EMAIL, UPDATE_PASSWORD",
            status_code=status.HTTP_200_OK,
            response_description="Project Response.",
            )
async def get_user_projects(username: str) -> JSONResponse:
    return await user_service.get_user_projects(username)


@router.post("/{username}/roles",
             description="Grant role to a user",
             status_code=status.HTTP_204_NO_CONTENT,
             )
async def assign_role_to_user(username: str, roles: List[str]) -> None:
    return await user_service.grant_roles(username=username, roles=roles)


@router.delete("/{username}/roles",
               description="Delete role of a user.",
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_role_of_user(username: str, roles: List[str]) -> None:
    return await user_service.revoke_roles(username=username, roles=roles)
