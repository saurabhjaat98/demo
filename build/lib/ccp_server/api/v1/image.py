###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved    #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Vicky Upadhyay <vicky@coredge.io>, Feb 2023                      #
# Modified by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                   #
###############################################################################
from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.image import ImageService
from ccp_server.util.constants import Constants

router = APIRouter()

image_service: ImageService = ImageService()


@router.get("",
            description="List all images.",
            status_code=status.HTTP_200_OK,
            response_description="Image Response.",
            )
async def list_images(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(False, title="Sort descending", description="Sort in descending order")):
    """
    List all images.
    :param query_str: Filter query string.
    :param page: Page number.
    :param size: Items per page.
    :param sort_by: Sort by fields.
    :param sort_desc: Sort in descending order.
    """
    data, total = await image_service.list_images(Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/{image_id}",
            description="Get image by id.",
            status_code=status.HTTP_200_OK,
            response_description="Image Response.", )
async def get_image(image_id: str) -> dict:
    """
    Get image by id.
    :param image_id: Image id.
    return: Image details.
    """
    return await image_service.get_image(image_id)
