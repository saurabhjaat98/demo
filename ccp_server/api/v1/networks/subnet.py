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
from ccp_server.service.networks.subnet import SubnetService
from ccp_server.util.constants import Constants

router = APIRouter()
subnet_service: SubnetService = SubnetService()


@router.post("/projects/{project_id}/networks/{network_id}/subnets",
             description="Create subnet for a network.",
             status_code=status.HTTP_201_CREATED,
             response_description="Subnet Creation Response.",
             response_model=None
             )
async def create_subnet(project_id: str, network_id: str, request: schemas.Subnet) -> IDResponse:
    """
    Create subnet.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param request: Request body.
    :return: Subnet ID.
    """
    doc_id = await subnet_service.create_subnet(project_id, network_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/networks/{network_id}/subnets",
            description="Get all subnets for a network.",
            status_code=status.HTTP_200_OK,
            response_description="Subnets Response.",
            )
async def list_subnets_by_network_id(project_id: str, network_id: str,
                                     query_str: str = Query(
                                         None, title="Search", description="Search item by name or description"),
                                     page: int = Query(1, ge=1, title="Page",
                                                       description="Page number"),
                                     size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                                                       description="Number of items to return"),
                                     sort_by: List[str] = Query(
                                         None, title="Sort by", description="Sort by fields (comma-separated list)"),
                                     sort_desc: bool = Query(False, title="Sort descending",
                                                             description="Sort in descending order")):
    data, total = await subnet_service.list_subnets_by_network_id(Pageable(query_str, page, size, sort_by, sort_desc),
                                                                  project_id, network_id)
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/networks/{network_id}/subnets/{subnet_id}",
            description="Get subnet by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Subnet Response.",
            )
async def get_subnet(project_id: str, network_id: str, subnet_id: str) -> dict:
    """
    Get subnet by ID.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param subnet_id: Subnet ID.
    :return: Subnet.
    """
    return await subnet_service.get_subnet(project_id, network_id, subnet_id)


@router.delete("/projects/{project_id}/networks/{network_id}/subnets/{subnet_id}",
               description="Delete a subnet.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Subnet delete Response.",
               )
async def delete_subnet(project_id: str, network_id: str, subnet_id: str):
    """
    Delete a subnet.
    :param project_id: Project ID.
    :param network_id: Network ID.
    :param subnet_id: Subnet ID.
    :return: None.
    """
    await subnet_service.delete_subnet(project_id, network_id, subnet_id)
