###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved    #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Vicky Upadhyay <vicky@coredge.io>, Mar 2023                      #
###############################################################################
from typing import List

from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.messages import Message


class VolumeSnapshot(services.VolumeSnapshot):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.VOLUME_SNAPSHOT

    async def create_volume_snapshot(self, volume_id: str, volume_snapshot: models.VolumeSnapshot
                                     ) -> models.VolumeSnapshot:
        """This method is used to create a volume snapshot
        :param volume_snapshot: Request body.
        :param volume_id: Volume ID.
        :return: The created volume snapshot ``VolumeSnapshot`` object."""
        try:
            cloud_response = self.conn.connect().create_volume_snapshot(
                volume_id=volume_id, force=True, **volume_snapshot.dict())
            map_res = await mapper(data=cloud_response, resource_name=self.collection)
            return map_res
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Volume snapshot'), e.status_code, e.details)

    async def list_volume_snapshots(self) -> List[models.VolumeSnapshot]:
        """This method is used to list all volume snapshots.
        :return: List of fetched volume snapshots ``VolumeSnapshot`` objects."""
        cloud_res = self.conn.connect().list_all_volume_snapshots()
        return await mapper(data=cloud_res, resource_name=self.collection)

    async def delete_volume_snapshot(self, snapshot_id: str):
        try:
            if not await self.conn.connect().delete_volume_snapshot(snapshot_id, wait=True):
                raise CCPOpenStackException("Failed To Delete Volume Snapshot")
        except Exception as e:
            raise CCPOpenStackException(f' {e.message or e}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
