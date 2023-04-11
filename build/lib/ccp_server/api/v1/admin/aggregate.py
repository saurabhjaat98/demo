###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, Feb 2023       #
###############################################################################
from __future__ import annotations

from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1.response_schemas import Page
from ccp_server.service.compute.aggregate import AggregateService
from ccp_server.util.constants import Constants

router = APIRouter()

aggregate_service: AggregateService = AggregateService()


@router.get("",
            description="Get compute ``Aggregate`` list.",
            status_code=status.HTTP_200_OK,
            response_description="compute ``Aggregate`` Response.",
            )
async def list_aggregates(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(False, title="Sort descending", description="Sort in descending order")):
    """This method is used to fetch the list all aggregates.
      :return: aggregate data """
    data = await aggregate_service.list_aggregates(query_str, page, size, sort_by, sort_desc)
    return Page(page, size, 0, data)


@router.get("/{aggregate_id}",
            description="Get compute ``Aggregate``.",
            status_code=status.HTTP_200_OK,
            response_description="compute ``Aggregate`` Response.",
            )
async def get_aggregate(aggregate_id: str):
    """
       This method is used to fetch the data of aggregate
       :param aggregate_id: id of the aggregate
       :param filters: filters
       :return: aggregate data
    """
    return await aggregate_service.get_aggregate(name_or_id=aggregate_id)
