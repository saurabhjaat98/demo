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
from ccp_server.schema.v1.schemas import InstanceActionsSchema
from ccp_server.service.compute.instance import InstanceService
from ccp_server.util.constants import Constants
from ccp_server.util.enums import InstanceActionEnum

router = APIRouter()

instance_service: InstanceService = InstanceService()


@router.post("/projects/{project_id}/instances",
             description="Create a new instance for a project",
             status_code=status.HTTP_201_CREATED,
             response_description="Instance Created Response",
             response_model=None
             )
async def create_instance(project_id: str, request: schemas.Instance) -> IDResponse:
    """
    Create a new instance with the given name and public key
    :param project_id: Project ID
    :param request: Contains Name of the instance and the public key
    returns: The created compute ``Server`` object
    """
    doc_id = await instance_service.create_instance(project_id, request)
    return IDResponse(doc_id)


@router.get("/projects/instances",
            description="List all instances for a organization",
            status_code=status.HTTP_200_OK,
            response_description="Instance List Response",
            )
async def list_all_instances(
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order"),
        tags: List[str] = Query(None,
                                title="tags",
                                description="List of key-value pairs to filter the instances by tags like team=dev ")
):
    """
    List all instances for a organization
    :param query_str: Search item by name or description
    :param page: Page number
    :param size:  of items to return
    :param sort_by: Sort by fields (comma-separated list)
    :param sort_desc: Sort in descending order
    :return: List of instances
    """
    data, total = await instance_service.list_all_instances(Pageable(query_str, page, size, sort_by, sort_desc, tags))

    return Page(page, size, total, data)


@router.get("/projects/{project_id}/instances",
            description="List all instances for a project",
            status_code=status.HTTP_200_OK,
            response_description="Instance List Response",
            )
async def list_instances_by_project_id(
        project_id: str,
        query_str: str = Query(
            None, title="Search", description="Search item by name or description"),
        page: int = Query(1, ge=1, title="Page", description="Page number"),
        size: int = Query(10, ge=1, le=Constants.DOCUMENT_TO_LIST_SIZE, title="Limit",
                          description="Number of items to return"),
        sort_by: List[str] = Query(
            None, title="Sort by", description="Sort by fields (comma-separated list)"),
        sort_desc: bool = Query(
            False, title="Sort descending", description="Sort in descending order"),
        tags: List[str] = Query(None,
                                title="tags",
                                description="List of key-value pairs to filter the instances by tags like team=dev ",)
):
    """
    List all instances for a project
    :param project_id:  Project ID
    :param query_str: Search item by name or description
    :param page: Page number
    :param size:  of items to return
    :param sort_by: Sort by fields (comma-separated list)
    :param sort_desc: Sort in descending order
    :return: List of instances
    """
    data, total = await instance_service.list_instances_by_project_id(
        Pageable(query_str, page, size, sort_by, sort_desc, tags), project_id)

    return Page(page, size, total, data)


@router.delete("/projects/{project_id}/instances/{instance_id}",
               description="Delete a Instance for a project",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Instance Delete Response",
               )
async def delete_instance(project_id: str, instance_id: str):
    """
    Delete an instance
    :param project_id: Project ID
    :param instance_id: UUID of the instance
    :return: None
    """
    await instance_service.delete_instance(project_id=project_id,
                                           instance_id=instance_id)


@router.put("/projects/{project_id}/instances/{instance_id}",
            description="Update a Instance for a project",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="Instance Update Response",
            )
async def update_instance(project_id: str, instance_id: str, request: schemas.Instance):
    """
    Update an instance
    :param project_id: Project ID
    :param instance_id: UUID of the instance
    :param name: Name of the instance
    :param description: Description of the instance
    :return: None
    """
    await instance_service.update_instance(project_id, instance_id, request)


@router.patch("/projects/{project_id}/instances/{instance_id}",
              description="Actions on an Instance for a project",
              status_code=status.HTTP_204_NO_CONTENT,
              response_description="Instance Action Response",
              )
async def actions(project_id: str, instance_id: str, action: InstanceActionEnum, actions_schema: InstanceActionsSchema):
    """
    Actions on an instance
    :param project_id: Project ID
    :param instance_id: UUID of the instance
    :param action: Action to be performed
    :param actions_schema: Action to be performed
    :return: None
    """
    return await instance_service.instance_action(project_id, instance_id, action, actions_schema)
