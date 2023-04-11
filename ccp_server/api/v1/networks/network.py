###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Feb 2023    #
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
from ccp_server.service.networks.network import NetworkService
from ccp_server.util.constants import Constants

router = APIRouter()
network_service: NetworkService = NetworkService()


@router.post("/projects/{project_id}/networks",
             description="Create network.",
             status_code=status.HTTP_201_CREATED,
             response_description="Network Creation Response.",
             response_model=None
             )
async def create_network(project_id: str,
                         request: schemas.Network
                         ) -> IDResponse:
    """
    Create network.
    :param project_id: Project ID.
    :param request: Request body.
    :return: ID of created network.
    """
    doc_id = await network_service.create_network(project_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/networks",
            description="List all networks for a project.",
            status_code=status.HTTP_200_OK,
            response_description="Networks Response.",
            )
async def list_networks_by_project_id(
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
            False, title="Sort descending", description="Sort in descending order"),
        tags: List[str] = Query(None,
                                title="tags",
                                description="List of key-value pairs to filter the netowrks by tags like team=dev ")

):
    """
    List all networks.
    :param project_id: Project ID.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items to return.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: List of networks.
    """
    data, total = await network_service.list_networks_by_project_id(
        Pageable(query_str, page, size, sort_by, sort_desc, tags), project_id)
    return Page(page, size, total, data)


@router.get("/projects/networks",
            description="List all networks for an org.",
            status_code=status.HTTP_200_OK,
            response_description="Networks Response.",
            )
async def list_all_networks(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(
            1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=100, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order"),
        tags: List[str] = Query(None,
                                title="tags",
                                description="List of key-value pairs to filter the netowrks by tags like team=dev ")
):
    """
    List all networks for db.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items to return.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: List of networks.
    """
    data, total = await network_service.list_all_networks(Pageable(query_str, page, size, sort_by, sort_desc, tags))

    return Page(page, size, total, data)


@router.get("/projects/{project_id}/networks/{network_id}",
            description="Get network by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Network Response.",
            )
async def get_network(project_id: str, network_id: str) -> dict:
    """
    Get network by ID.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :return: Network.
    """
    return await network_service.get_network(project_id=project_id, network_id=network_id)


@router.put("/projects/{project_id}/network/{network_id}",
            description="Update a network",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="network Update Response",
            )
async def update_network(project_id: str, network_id: str, request: schemas.Network):
    """
    Update  network
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param request: Request body.
    :return: None
    """
    await network_service.update_network(project_id, network_id, request)


@router.delete("/projects/{project_id}/networks/{network_id}",
               description="Delete a network.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Network delete Response.",
               )
async def delete_network(project_id: str, network_id: str):
    """
    Delete a network.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :return: None.
    """
    await network_service.delete_network(project_id=project_id, network_id=network_id)
