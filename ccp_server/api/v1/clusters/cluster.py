###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Apr 2023    #
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
from ccp_server.service.clusters.cluster import ClusterService

router = APIRouter()
cluster_service: ClusterService = ClusterService()


@router.post("/projects/{project_id}/cluster-templates/{cluster_template_id}/clusters",
             description="Create cluster for a project.",
             status_code=status.HTTP_201_CREATED,
             response_description="Cluster Creation Response.",
             response_model=None
             )
async def create_cluster(project_id: str, cluster_template_id: str, request: schemas.Cluster) -> IDResponse:
    """
    Create cluster.
    :param project_id: Project ID.
    :param cluster_template_id: Cluster template ID.
    :param request: Request body.
    :return: ID of created cluster.
    """
    doc_id = await cluster_service.create_cluster(project_id, cluster_template_id, request)
    return IDResponse(doc_id)


@router.get("/projects/{project_id}/clusters",
            description="List all clusters for a project.",
            status_code=status.HTTP_200_OK,
            response_description="Clusters Response.",
            )
async def list_clusters_by_project(
        project_id: str,
        query_str: str = Query(None, title="Search",
                               description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=100, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(None, title="Sort by",
                                   description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order")
):
    """
    List all clusters for a project.
    :param project_id: Project ID.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items to return.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: List of clusters.
    """
    data, total = await cluster_service.list_clusters_by_project(
        Pageable(query_str, page, size, sort_by, sort_desc), project_id)
    return Page(page, size, total, data)


@router.get("/projects/clusters",
            description="List all clusters for an org.",
            status_code=status.HTTP_200_OK,
            response_description="Clusters Response.",
            )
async def list_all_clusters(
        query_str: str = Query(None, title="Search",
                               description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=100, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(None, title="Sort by",
                                   description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order")
):
    """
    List all clusters.
    :param query_str: Search query.
    :param page: Page number.
    :param size: Number of items to return.
    :param sort_by: Sort by fields (comma-separated list).
    :param sort_desc: Sort in descending order.
    :return: List of clusters.
    """
    data, total = await cluster_service.list_all_clusters(
        Pageable(query_str, page, size, sort_by, sort_desc))
    return Page(page, size, total, data)


@router.get("/projects/{project_id}/clusters/{cluster_id}",
            description="Get cluster by ID.",
            status_code=status.HTTP_200_OK,
            response_description="Cluster Response.",
            )
async def get_cluster(project_id: str, cluster_id: str) -> dict:
    """
    Get cluster by ID.
    :param project_id: Project ID.
    :param cluster_id: Cluster ID.
    :return: Cluster .
    """
    return await cluster_service.get_cluster(project_id, cluster_id)


@router.delete("/projects/{project_id}/clusters/{cluster_id}",
               description="Delete a cluster.",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Cluster delete Response.",
               )
async def delete_cluster(project_id: str, cluster_id: str):
    """
    Delete cluster.
    :param project_id: Project ID.
    :param cluster_id: Cluster ID.
    :return: None.
    """
    await cluster_service.delete_cluster(project_id, cluster_id)
