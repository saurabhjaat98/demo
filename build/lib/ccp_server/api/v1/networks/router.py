###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
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
from ccp_server.service.networks.router import RouterService
from ccp_server.util.constants import Constants

router = APIRouter()
router_service: RouterService = RouterService()


@router.post("/projects/{project_id}/routers",
             description="Create router for a project.",
             status_code=status.HTTP_201_CREATED,
             response_description="Router Creation Response.",
             response_model=None
             )
async def create_router(project_id: str, request: schemas.Router) -> IDResponse:
    """
    Create router.
    :param project_id: Project ID.
    :param request: Request body.
    :return: ID of created router.
    """
    doc_id = await router_service.create_router(project_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/routers",
            description="List all routers for a project.",
            status_code=status.HTTP_200_OK,
            response_description="Routers Response.",
            )
async def list_routers_by_project_id(
        project_id: str,
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order")
):
    """
    List all routers for a project.
    :param project_id: Project ID.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items to return.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: List of routers.
    """
    data, total = await router_service.list_routers_by_project_id(Pageable(query_str, page, size, sort_by, sort_desc),
                                                                  project_id)
    return Page(page, size, total, data)


@router.get("/projects/routers",
            description="List all routers for an org.",
            status_code=status.HTTP_200_OK,
            response_description="Routers Response.",
            )
async def list_all_routers(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order")
):
    """
    List all routers for an org.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items to return.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: List of routers.
    """
    data, total = await router_service.list_all_routers(Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/routers/{router_id}",
            description="Get router by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Router Response.",
            )
async def get_router(project_id: str, router_id: str) -> dict:
    """
    Get router by ID.
    :param project_id: Project ID.
    :param router_id: Router ID.
    :return: Router.
    """
    return await router_service.get_router(project_id=project_id, router_id=router_id)


@router.delete("/projects/{project_id}/routers/{router_id}",
               description="Delete a router.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Router delete Response.",
               )
async def delete_router(project_id: str, router_id: str):
    """
    Delete router.
    :param project_id: Project ID.
    :param router_id: Router ID.
    :return: None.
    """
    await router_service.delete_router(project_id=project_id, router_id=router_id)
