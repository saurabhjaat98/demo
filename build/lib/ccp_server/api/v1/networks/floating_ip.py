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

from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.networks.floating_ip import FloatingIPService
from ccp_server.util.constants import Constants

router = APIRouter()
floating_ip_service: FloatingIPService = FloatingIPService()


@router.post("/projects/{project_id}/networks/{network_id}/floating-ips",
             description="Create floating IP.",
             status_code=status.HTTP_201_CREATED,
             response_description="Floating IP Creation Response.",
             response_model=None
             )
async def create_floating_ip(project_id: str, network_id: str) -> IDResponse:
    """
    Create floating IP.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :return: Floating IP ID.
    """
    doc_id = await floating_ip_service.create_floating_ip(project_id, network_id)
    return IDResponse(doc_id)


@router.get("/projects/networks/floating-ips",
            description="Get all floating IPs.",
            status_code=status.HTTP_200_OK,
            response_description="Floating IPs Response.",
            )
async def list_all_floating_ips(
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
    data, total = await floating_ip_service.list_all_floating_ips(Pageable(query_str, page, size, sort_by,
                                                                           sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/networks/floating-ips",
            description="Get all floating IPs for a project.",
            status_code=status.HTTP_200_OK,
            response_description="Floating IPs Response.",
            )
async def list_floating_ips(
        project_id: str,
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
    data, total = await floating_ip_service.list_floating_ips(project_id, Pageable(query_str, page, size, sort_by,
                                                                                   sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/networks/{network_id}/floating-ips/{floating_ip_id}",
            description="Get floating IP by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Floating IP Response.",
            )
async def get_floating_ip(project_id: str, network_id: str, floating_ip_id: str) -> dict:
    """
    Get floating IP by ID.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param floating_ip_id: Floating IP ID.
    :return: Floating IP.
    """
    return await floating_ip_service.get_floating_ip(project_id, network_id, floating_ip_id)


@router.delete("/projects/{project_id}/networks/{network_id}/floating-ips/{floating_ip_id}",
               description="Delete a floating IP.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Floating IP delete Response.",
               )
async def delete_floating_ip(project_id: str, network_id: str, floating_ip_id: str):
    """
    Delete a floating IP.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param floating_ip_id: Floating IP ID.

    """
    await floating_ip_service.delete_floating_ip(project_id, network_id, floating_ip_id)
