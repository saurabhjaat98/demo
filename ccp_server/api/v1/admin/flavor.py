###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
# Modified by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                   #
###############################################################################
from __future__ import annotations

from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.flavor import FlavorService
from ccp_server.util.constants import Constants

router = APIRouter()

flavor_service: FlavorService = FlavorService()


@router.get("",
            description="List all flavors.",
            status_code=status.HTTP_200_OK,
            response_description="Flavor fetching Response.",
            )
async def list_flavors(
    query_str: str = Query(
        None, title="Search", description="Search item by name or description"),
    page: int = Query(1, ge=1, title="Page", description="Page number"),
    size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                      description="Number of items to return"),
    sort_by: List[str] = Query(
        None, title="Sort by", description="Sort by fields (comma-separated list)"),
    sort_desc: bool = Query(
        False, title="Sort descending", description="Sort in descending order")):
    """
    List all flavors.
    :param query_str: Filter query string.
    :param page: Page number.
    :param size: Items per page.
    :param sort_by: Sort by fields.
    :param sort_desc: Sort in descending order.
    """

    data, total = await flavor_service.list_flavors(Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/{flavor_id}",
            description="Get flavor by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Flavor Detail.",
            )
async def get_flavor(flavor_id: str):
    """
    Get flavor by ID.
    :param flavor_id: Flavor ID.
    """
    return await flavor_service.get_flavor(flavor_id)
