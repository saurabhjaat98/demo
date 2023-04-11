###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved    #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Vicky Upadhyay <vicky@coredge.io>, Mar 2023                      #
###############################################################################
from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.volume_snapshot import VolumeSnapshotService
from ccp_server.util.constants import Constants

router = APIRouter()

volume_snapshot_service: VolumeSnapshotService = VolumeSnapshotService()


@router.post("/projects/{project_id}/volumes/{volume_id}/snapshots",
             description="Create Volume Snapshot.",
             status_code=status.HTTP_201_CREATED,
             response_description="Volume Snapshot ID.",
             response_model=None
             )
async def create_volume_snapshot(project_id: str, volume_id: str, request: schemas.VolumeSnapshot) -> IDResponse:
    """This API is used to create volume snapshot.
    :param project_id: Project ID.
    :param request: Request body.
    :param volume_id: Volume ID.
    :return: Volume Snapshot ID."""
    doc_id = await volume_snapshot_service.create_volume_snapshot(project_id, volume_id, request)
    return IDResponse(doc_id)


@router.get("/projects/volumes/snapshots",
            description="Get Volume Snapshot list for a org",
            status_code=status.HTTP_200_OK,
            response_description="Volume Snapshot fetching Response."
            )
async def list_all_volume_snapshots(
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
    """This API is used to list volume snapshots.
    :return: List of volume snapshots."""
    data, total = await volume_snapshot_service.list_all_volume_snapshots(
        Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/volumes/snapshots",
            description="Get list of all Volume Snapshots in a project.",
            status_code=status.HTTP_200_OK,
            response_description="List of Volume Snapshots in a project.",
            )
async def list_volume_snapshots_from_project(
    project_id: str,
    query_str: str = Query(
        None, title="Search",
        description="Search item by name or description"),
    page: int = Query(
        1, ge=1, title="Page", description="Page number"),
    size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE,
                      title="Limit",
                      description="Number of items to return"),
    sort_by: List[str] = Query(
        None, title="Sort by",
        description="Sort by fields (comma-separated list)"),
    sort_desc: bool = Query(False, title="Sort descending",
                            description="Sort in descending order")):
    data, total = await volume_snapshot_service.list_volume_snapshots_from_project(
        project_id, Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/volumes/{volume_id}/snapshots",
            description="Get list of all Volume Snapshots for a volume in a project.",
            status_code=status.HTTP_200_OK,
            response_description="List of Volume Snapshots in a project.",
            )
async def list_volume_snapshots_from_volume(
    project_id: str,
    volume_id: str,
    query_str: str = Query(
        None, title="Search",
        description="Search item by name or description"),
    page: int = Query(
        1, ge=1, title="Page", description="Page number"),
    size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE,
                      title="Limit",
                      description="Number of items to return"),
    sort_by: List[str] = Query(
        None, title="Sort by",
        description="Sort by fields (comma-separated list)"),
    sort_desc: bool = Query(False, title="Sort descending",
                            description="Sort in descending order")):
    data, total = await volume_snapshot_service.list_volume_snapshots_from_volume(
        project_id, volume_id, Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/volumes/{volume_id}/snapshots/{volume_snapshot_id}",
            description="Get Volume Snapshot by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Volume Snapshot Detail.",
            )
async def get_volume_snapshot(project_id: str, volume_id: str, volume_snapshot_id: str):
    """This API is used to get volume snapshot by ID.
    :param project_id: Project ID.
    :param volume_id: Volume ID.
    :param volume_snapshot_id: Volume Snapshot ID.
    :return: Volume Snapshot details."""
    return await volume_snapshot_service.get_volume_snapshot(project_id, volume_id, volume_snapshot_id)


@router.delete("/projects/{project_id}/volumes/{volume_id}/snapshots/{volume_snapshot_id}",
               description="Delete a volume snapshot.",
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete_volume_snapshot(project_id: str, volume_id: str, volume_snapshot_id: str):
    """This API is used to delete volume snapshot.
    :param project_id: Project ID.
    :param volume_id: Volume ID.
    :param volume_snapshot_id: Volume Snapshot ID.
    :return: None."""
    await volume_snapshot_service.delete_volume_snapshot(project_id, volume_id, volume_snapshot_id)


@router.put("/projects/{project_id}/volumes/{volume_id}/snapshots/{volume_snapshot_id}",
            description="Update a volume snapshot",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="Volume Snapshot Update Response",
            )
async def update_volume_snapshot(project_id: str, volume_id: str,
                                 volume_snapshot_id: str, request: schemas.VolumeSnapshot):
    """
    Update  volume snapshot
    :param project_id: Project ID.
    :param volume_id: Volume ID.
    :param volume_snapshot_id: UUID of the volume snapshot
    :param request: Request body.
    :return: None
    """
    return await volume_snapshot_service.update_volume_snapshot(project_id, volume_id, volume_snapshot_id, request)
