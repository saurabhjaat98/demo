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
from fastapi.responses import JSONResponse

from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.project import ProjectService
from ccp_server.util.constants import Constants

router = APIRouter()

project_service: ProjectService = ProjectService()


@router.post("",
             description="Create project.",
             status_code=status.HTTP_201_CREATED,
             response_description="Project ID.",
             response_model=None
             )
async def create_project(
        request: schemas.Project
) -> IDResponse:
    doc_id = await project_service.create_project(request)
    return IDResponse(doc_id)


@router.get("",
            description="Get all projects.",
            status_code=status.HTTP_200_OK,
            response_description="Projects Response.",
            )
async def get_projects(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order"),
        tags: List[str] = Query(None,
                                title="tags",
                                description="List of key-value pairs to filter the projects by tags like team=dev ")):
    data, total = await project_service.list_project(Pageable(query_str, page, size, sort_by, sort_desc, tags))
    return Page(page, size, total, data)


@router.get("/{project_id}",
            description="Get project by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Projects Response.",
            )
async def get_project(project_id: str) -> JSONResponse:
    project = await project_service.get_project(project_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=project)


@router.put("/{project_id}",
            description="Update a project.",
            status_code=status.HTTP_204_NO_CONTENT,
            )
async def update_projects(
        project_id: str,
        request: schemas.Project
) -> None:
    await project_service.update_project(project_id, request)


@router.get("/{project_id}/members",
            description="Get the members of a project.",
            status_code=status.HTTP_200_OK,
            )
async def get_members(
        project_id: str,
) -> list[dict]:
    return await project_service.get_project_members(project_id)


@router.delete("/{project_id}",
               description="Delete a project.",
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_project(
        project_id: str
) -> None:
    await project_service.delete_project(project_id)


@router.patch("/{project_id}/members/{username}",
              description="Add a member to the project.",
              status_code=status.HTTP_204_NO_CONTENT,
              )
async def add_member(
        project_id: str,
        username: str,
        role: str = 'member'
) -> None:
    await project_service.add_member(project_id, username, role)


@router.delete("/{project_id}/members/{username}",
               description="Remove a member from the project.",
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def remove_member(
        project_id: str,
        username: str,
        role: str = 'member'
) -> None:
    await project_service.remove_member(project_id, username, role)
