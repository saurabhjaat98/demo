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
from ccp_server.service.compute.hypervisor import HypervisorService
from ccp_server.util.constants import Constants

router = APIRouter()

hypervisor_service: HypervisorService = HypervisorService()


@router.get("",
            description="Get compute ``Hypervisor`` list.",
            status_code=status.HTTP_200_OK,
            response_description="compute ``Hypervisor`` Response.",
            )
async def list_hypervisors(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(False, title="Sort descending", description="Sort in descending order")):
    """This method is used to fetch the list all hypervisors.
      :return: hypervisor data """
    data = await hypervisor_service.list_hypervisors(query_str, page, size, sort_by, sort_desc)
    return Page(page, size, 0, data)
