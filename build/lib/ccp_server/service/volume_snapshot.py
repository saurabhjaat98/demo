###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved    #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Vicky Upadhyay <vicky@coredge.io>, Mar 2023                      #
###############################################################################
from fastapi import status
from pydantic.types import StrictBool

from ccp_server.db import models
from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBusinessException
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class VolumeSnapshotService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.VOLUME_SNAPSHOT

    @log
    async def create_volume_snapshot(self, project_id: str, volume_id: str, request: models.VolumeSnapshot) -> str:
        """This method is used to create a snapshot in cloud and mongo.
        :param project_id: Project ID.
        :param request: Snapshot request body.
        :param volume_id: Volume ID.
        :return: Snapshot ID."""
        db_response = await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.VOLUME,
            uid=volume_id,
            project_id=project_id,
            raise_exception=True)
        if db_response['status'] == 'in-use':  # Volume is in use
            raise CCPBusinessException(
                message="Volume is in use Cannot create volume snapshot",
                status_code=status.HTTP_400_BAD_REQUEST)

        """Check for volumesnapshot if already exist"""
        await self.db.check_document_by_name(
            collection_name=self.collection,
            name=request.name,
            project_id=project_id,
            raise_exception=True)
        # generate a random UUID for the cloud snapshot name
        db_volume_snapshot_name = request.name
        request.name = Utils.generate_unique_str()

        # Save the snapshot in the OpenStack

        cloud_response = await self.connect.volume_snapshot.create_volume_snapshot(
            volume_id=db_response['reference_id'], volume_snapshot=request)
        # Save the snapshot in the mongo db
        db_model = MongoAPI.populate_db_model(cloud_response, name=db_volume_snapshot_name,
                                              description=request.description,
                                              project_id=project_id)
        doc_id = await self.db.write_document_with_default_details(self.collection, db_model)
        return doc_id

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_volume_snapshots(self, pageable: Pageable = None, use_db: StrictBool = True):
        """This method is used to fetch the data of snapshots of a volume from mongo.
        :return: List of snapshots."""
        if use_db:
            return await self.db.get_document_list_by_ids(collection_name=self.collection,
                                                          pageable=pageable,
                                                          exclude_project=True)
        else:
            mapper_res = await self.connect.volume_snapshot.list_volume_snapshots()
            return mapper_res, len(mapper_res)

    @log
    async def list_volume_snapshots_from_project(self, project_id: str, pageable: Pageable = None):
        """Fetches the data of snapshots of a volume for a specific project from mongo.
        :param project_id: The ID of the project to filter snapshots by.
        :param pageable: Pageable object.
        :return: List of snapshots for the specified project."""
        return await self.db.get_document_list_by_ids(collection_name=self.collection,
                                                      pageable=pageable,
                                                      project_id=project_id)

    @log
    async def list_volume_snapshots_from_volume(self, project_id: str, volume_id: str, pageable: Pageable = None):
        """Fetches the data of snapshots of a volume for a specific project from mongo.
        :param project_id: The ID of the project to filter snapshots by.
        :param volume_id: The ID of the volume to filter snapshots by.
        :param pageable: Pageable object.
        :return: List of snapshots for the specified project."""
        return await self.db.get_document_list_by_ids(collection_name=self.collection,
                                                      pageable=pageable,
                                                      project_id=project_id,
                                                      filter_dict={'volume_id': volume_id})

    @log
    async def get_volume_snapshot(self, project_id: str, volume_id: str, volume_snapshot_id: str) -> any:
        """This method is used to fetch the data of a snapshot from mongo by using snapshot_id

        :param volume_snapshot_id: id of the snapshot
        :param volume_id: id of the volume
        :param project_id: id of the project
        :return: returns the snapshot data or None
        """

        return await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.VOLUME_SNAPSHOT,
            uid=volume_snapshot_id,
            project_id=project_id,
            filter_dict={'volume_id': volume_id})

    @log
    async def delete_volume_snapshot(self, project_id: str, volume_id: str, volume_snapshot_id: str) -> None:
        """This method is used to delete a snapshot of a volume in cloud and mongo.
        :param volume_snapshot_id: Volume snapshot ID.
        :param volume_id: Volume ID.
        :param project_id: Project ID.
        :return: None."""
        """Volume snapshot DB response"""
        db_response = await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.VOLUME_SNAPSHOT,
            uid=volume_snapshot_id,
            project_id=project_id,
            filter_dict={'volume_id': volume_id},
            raise_exception=True)

        """Delete the snapshot in the Cloud"""
        await self.connect.volume_snapshot.delete_volume_snapshot(db_response['reference_id'])

        """Delete the snapshot in the mongo db"""
        await self.db.soft_delete_document_by_uuid(Constants.MongoCollection.VOLUME_SNAPSHOT, volume_snapshot_id)

    @log
    async def update_volume_snapshot(self, project_id: str, volume_id: str,
                                     volume_snapshot_id: str, request: models.VolumeSnapshot) -> None:
        """
        Update volume snapshot
        :param volume_snapshot_id: id of the snapshot
        :param volume_id: id of the volume
        :param project_id: id of the project
        :param request: Volume snapshot request body.
        """
        """Volume snapshot DB response"""
        await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.VOLUME_SNAPSHOT,
            uid=volume_snapshot_id,
            project_id=project_id,
            filter_dict={'volume_id': volume_id},
            raise_exception=True)
        return await self.db.update_document_by_uuid(Constants.MongoCollection.VOLUME_SNAPSHOT,
                                                     uid=volume_snapshot_id,
                                                     data_dict={
                                                         'name': request.name, 'description': request.description},
                                                     )
