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
from ccp_server.service.networks.port import PortService
from ccp_server.util.constants import Constants

router = APIRouter()
port_service: PortService = PortService()


@router.post("/projects/{project_id}/networks/{network_id}/ports",
             description="Create port in a network.",
             status_code=status.HTTP_201_CREATED,
             response_description="Port Creation Response.",
             response_model=None
             )
async def create_port(project_id: str, network_id: str, request: schemas.Port) -> IDResponse:
    """
    Create port.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param request: Request body.
    :return: Port ID.
    """
    doc_id = await port_service.create_port(project_id, network_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/networks/{network_id}/ports",
            description="List all ports of a network.",
            status_code=status.HTTP_200_OK,
            response_description="Ports Response.",
            )
async def list_ports_by_network_id(
        project_id: str, network_id: str,
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
    Get all ports.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items per page.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: List of ports.
    """
    data, total = await port_service.list_ports_by_network_id(project_id, network_id,
                                                              Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/networks/{network_id}/ports/{port_id}",
            description="Get port by ID of a network.",
            status_code=status.HTTP_200_OK,
            response_description="Port Response.",
            )
async def get_port(project_id: str, network_id: str, port_id: str) -> dict:
    """
    Get port by ID.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param port_id: Port ID.
    :return: Port.
    """
    return await port_service.get_port(project_id=project_id, network_id=network_id, port_id=port_id)


@router.delete("/projects/{project_id}/networks/{network_id}/ports/{port_id}",
               description="Delete a port by ID of a network.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Port delete Response.",
               )
async def delete_port(project_id: str, network_id: str, port_id: str):
    """
    Delete port by ID.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param port_id: Port ID.
    :return: None.
    """
    await port_service.delete_port(project_id=project_id, network_id=network_id, port_id=port_id)
