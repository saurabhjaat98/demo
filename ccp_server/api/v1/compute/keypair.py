###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.compute.keypair import KeyPairService
from ccp_server.util.constants import Constants

router = APIRouter()

keypair_service: KeyPairService = KeyPairService()


@router.post("/projects/keypairs",
             description="Create a new keypair",
             status_code=status.HTTP_201_CREATED,
             response_description="Keypair Created Response",
             response_model=None
             )
async def create_keypair(request: schemas.KeyPair) -> IDResponse:
    """
    Create a new keypair with the given name and public key
    :param request: Contains Name of the keypair and the public key
    :param project_id: Project ID
    Returns: id of the keypair
    """
    doc_id = await keypair_service.create_keypair(request)
    return IDResponse(doc_id)


@router.get("/projects/keypairs",
            description="List all Keypairs",
            status_code=status.HTTP_200_OK,
            response_description="Keypair List Response"
            )
async def list_keypairs(
    query_str: str = Query(
        None, title="Search", description="Search item by name or description"),
    page: int = Query(
        1, ge=1, title="Page", description="Page number"),
    size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                      description="Number of items to return"),
    sort_by: List[str] = Query(
        None, title="Sort by", description="Sort by fields (comma-separated list)"),
    sort_desc: bool = Query(
        False, title="Sort descending", description="Sort in descending order")
):
    """
    List all keypairs
    :param project_id: Project ID
    :param query_str: Search query
    :param page: Page number
    :param size: Items per page
    :param sort_by: Sort by fields
    :param sort_desc: Sort in descending order
    :return: List of keypairs
    """
    data, total = await keypair_service.list_keypairs(Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.delete("/projects/keypairs/{keypair_id}",
               description="Delete a Keypair",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Keypair Delete Response",
               )
async def delete_keypair(keypair_id: str):
    """
    Delete a keypair
    :param keypair_id: UUID of the keypair
    :return: True if keypair deleted else False
    """
    await keypair_service.delete_keypair(keypair_id)
