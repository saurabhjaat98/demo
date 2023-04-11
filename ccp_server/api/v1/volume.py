###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
# Modified by Vicky Upadhyay <vicky@coredge.io>, Feb 2023                     #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, march 2023     #
###############################################################################
from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.volume import VolumeService
from ccp_server.util.constants import Constants
from ccp_server.util.enums import VolumeActionEnum

router = APIRouter()

volume_service: VolumeService = VolumeService()


@router.post("/projects/{project_id}/volumes",
             description="Create ``Volume`` for a project",
             status_code=status.HTTP_201_CREATED,
             response_description="``Volume`` ID.",
             response_model=None
             )
async def create_volume(project_id: str, request: schemas.Volume) -> IDResponse:
    """This API is used to create volume.
    :param project_id: Project ID.
    :param request: Request body.
    :return: Volume ID."""
    doc_id = await volume_service.create_volume(project_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/volumes",
            description="List Volumes for a project",
            status_code=status.HTTP_200_OK,
            response_description="Volume fetching Response.",
            )
async def list_volumes_by_project_id(project_id: str,
                                     query_str: str = Query(
                                         None, title="Search", description="Search item by name or description"),
                                     page: int = Query(1, ge=1, title="Page",
                                                       description="Page number"),
                                     size: int = Query(10, ge=1, le=100, title="Limit",
                                                       description="Number of items to return"),
                                     sort_by: List[str] = Query(
                                         None, title="Sort by", description="Sort by fields (comma-separated list)"),
                                     sort_desc: bool = Query(
                                         False, title="Sort descending", description="Sort in descending order")
                                     ):
    """This API is used to list Volumes list for a project.
        :param project_id: Project ID.
        :param query_str: Search query.
        :param page: Page number.
        :param size: Number of items to return.
        :param sort_by: Sort by fields (comma-separated list).
        :param sort_desc: Sort in descending order.
        :return: Volumes list."""
    data, total = await volume_service.list_volumes_by_project_id(Pageable(query_str, page, size, sort_by, sort_desc),
                                                                  project_id)
    return Page(page, size, total, data)


@router.get("/projects/volumes",
            description="List all volumes for an org",
            status_code=status.HTTP_200_OK,
            response_description="Volume Detail")
async def list_all_volumes(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page",
                          description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order"),
        tags: List[str] = Query(None,
                                title="tags",
                                description="List of key-value pairs to filter the volumes by tags  like team=dev ")
):
    """This API is used to list all Volumes for the organization.
        :param query_str: Search query.
        :param page: Page number.
        :param size: Number of items to return.
        :param sort_by: Sort by fields (comma-separated list).
        :param sort_desc: Sort in descending order.
        :param tags: List of key-value pairs to filter the volumes by tags
        :return: Volumes list. """
    data, total = await volume_service.list_all_volumes(Pageable(query_str, page, size, sort_by, sort_desc, tags))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/volumes/{volume_id}",
            description="Get Volume by ID for a project",
            status_code=status.HTTP_200_OK,
            response_description="Volume Detail.",
            )
async def get_volume(project_id: str, volume_id: str):
    """This API is used to get Volume by ID for a project.
    :param project_id: Project ID.
    :param volume_id: Volume ID.
    :return: Volume detail."""
    return await volume_service.get_volume(project_id, volume_id)


@router.delete("/projects/{project_id}/volumes/{volume_id}",
               description="``Delete a volume by ID``",
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_volume(project_id: str, volume_id: str) -> None:
    """This API is used to delete volume.
    :param project_id: Project ID.
    :param volume_id: Volume ID.
    :return: None."""
    await volume_service.delete_volume(project_id, volume_id)


@router.put("/projects/{project_id}/volumes/{volume_id}",
            description="Update a volume",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="Volume Update Response",
            )
async def update_volume(project_id: str, volume_id: str, request: schemas.Volume) -> None:
    """
    Update  volume
    :param project_id: Project ID.
    :param volume_id: UUID of the volume
    :param request: request
    :return: None
    """
    await volume_service.update_volume(project_id, volume_id, request)


@router.patch("/projects/{project_id}/volumes/{volume_id}/instances/{instance_id}",
              description="Attach/Detach ``Volume`` to a Instance",
              status_code=status.HTTP_204_NO_CONTENT,
              response_description="``Volume`` attachment Response.",
              response_model=None)
async def volume_action(project_id: str, volume_id: str, instance_id: str, action: VolumeActionEnum):
    """This API is used to attach/detach ``Volume`` to an Instance.
    :param project_id: Project ID.
    :param volume_id: UUID of the volume
    :param instance_id: UUID of the instance
    :param action: Attach/Detach action
    :return: None."""

    if action == VolumeActionEnum.ATTACH:
        return await volume_service.attach_volume(project_id, volume_id, instance_id)
    elif action == VolumeActionEnum.DETACH:
        return await volume_service.detach_volume(project_id, volume_id, instance_id)
