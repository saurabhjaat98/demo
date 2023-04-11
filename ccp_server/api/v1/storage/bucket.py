###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
###############################################################################
from typing import List

from fastapi import APIRouter
from fastapi import File
from fastapi import Query
from fastapi import status
from fastapi import UploadFile

from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.schema.v1.response_schemas import Page
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.storage.bucket import BucketService
from ccp_server.util.constants import Constants

router = APIRouter()

bucket_service: BucketService = BucketService()


@router.post("/projects/{project_id}/buckets",
             description="Create storage `Bucket`.",
             status_code=status.HTTP_201_CREATED,
             response_description="create `Bucket` Response.",
             )
async def create_bucket(project_id: str, request: schemas.Bucket):
    doc_id = await bucket_service.create_bucket(project_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/buckets",
            description="List All storage `Buckets` for a project.",
            status_code=status.HTTP_200_OK,
            response_description="List `Buckets` Response.",
            )
async def list_buckets_by_project_id(project_id: str,
                                     query_str: str = Query(
                                         None, title="Search", description="Search item by name or description"),
                                     page: int = Query(1, ge=1, title="Page",
                                                       description="Page number"),
                                     size: int = Query(
                                         10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE,
                                         title="Limit", description="Number of items to return"),
                                     sort_by: List[str] = Query(None, title="Sort by",
                                                                description="Sort by fields (comma-separated list)"),
                                     sort_desc: bool = Query(False, title="Sort descending",
                                                             description="Sort in descending order"),
                                     tags: List[str] = Query(None,
                                                             title="tags",
                                                             description="List of key-value pairs "
                                                                         "to filter the buckets by tags")
                                     ):
    data, total = await bucket_service.list_buckets_by_project_id(
        Pageable(query_str, page, size, sort_by, sort_desc, tags), project_id=project_id,)
    return Page(page, size, total, data)


@router.get("/projects/buckets",
            description="List All storage `Buckets`.",
            status_code=status.HTTP_200_OK,
            response_description="List `Buckets` Response.",
            )
async def list_buckets(query_str: str = Query(None, title="Search", description="Search item by name or description"),
                       page: int = Query(1, ge=1, title="Page",
                                         description="Page number"),
                       size: int = Query(
                           10, ge=1, le=100, title="Limit", description="Number of items to return"),
                       sort_by: List[str] = Query(None, title="Sort by",
                                                  description="Sort by fields (comma-separated list)"),
                       sort_desc: bool = Query(
                           False, title="Sort descending", description="Sort in descending order"),
                       tags: List[str] = Query(None,
                                               title="tags",
                                               description="List of key-value pairs to filter the buckets by tags"),
                       use_db: bool = Query(True, title="use database",
                                            description="Fetch the result from database or directly from cloud",
                                            include_in_schema=False)
                       ):
    data, total = await bucket_service.list_buckets(
        Pageable(query_str, page, size, sort_by, sort_desc, tags), use_db=use_db)
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/buckets/{bucket_id}",
            description="List storage `Bucket`.",
            status_code=status.HTTP_200_OK,
            response_description="`Bucket` Response.",
            )
async def get_bucket(project_id: str, bucket_id: str):
    return await bucket_service.get_bucket(project_id, bucket_id)


@router.delete("/project/{project_id}/buckets/{bucket_id}",
               description="Delete storage `Bucket`.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Delete `Bucket` Response.",
               )
async def delete_bucket(project_id: str, bucket_id: str):
    await bucket_service.delete_bucket(project_id, bucket_id)


@router.post("/projects/{project_id}/buckets/{bucket_id}/objects/upload",
             description="store `Data or File` into Bucket.",
             status_code=status.HTTP_204_NO_CONTENT,
             response_description="store `Data` Bucket Response.",
             )
async def upload(project_id: str, bucket_id: str, file: UploadFile = File(...)):
    await bucket_service.upload_object(bucket_id=bucket_id, file=file, project_id=project_id)


@router.get("/projects/{project_id}/buckets/{bucket_id}/objects",
            description="List  All `Objects` in Bucket.",
            status_code=status.HTTP_200_OK,
            response_description="List `Objects` Buckets Response.",
            )
async def get_objects(project_id: str, bucket_id: str):
    data = await bucket_service.get_objects(project_id, bucket_id)
    return Page(1, len(data), len(data), data)


@router.delete("/projects/{project_id}/buckets/{bucket_id}/objects/{object_id}",
               description="Delete `Object` from Bucket.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Delete `Object` Response.",
               )
async def delete_object(project_id: str, bucket_id: str, object_id: str):
    await bucket_service.delete_object(project_id, bucket_id, object_id)


@router.get("/projects/{project_id}/buckets/{bucket_id}/objects/download",
            description="Download `Data or Object` into local.",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="Download `Data or Object` into local Response.",
            )
async def download(project_id: str, bucket_id: str, object_name: str, path: str):
    await bucket_service.download_object(bucket_id=bucket_id, object_name=object_name, project_id=project_id,
                                         path=path)
