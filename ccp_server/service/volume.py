###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
#  Modified by Vicky Upadhyay <vicky@coredge.io>, Feb 2023                    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, march 2023     #
###############################################################################
from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBusinessException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message
from ccp_server.util.utils import Utils


class VolumeService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.VOLUME

    @log
    async def create_volume(self, project_id: str, request):
        """This method is used to create a volume in cloud and mongo.
        :param request: Volume request body.
        :param project_id: Project ID
        :return: Volume ID."""

        """Check for volume if already exist"""
        await self.db.check_document_by_name(collection_name=Constants.MongoCollection.VOLUME,
                                             name=request.name,
                                             project_id=project_id,
                                             raise_exception=True)

        """generate a random UUID for the cloud volume name"""
        db_volume_name = request.name
        request.name = Utils.generate_unique_str()

        """Save the volume in the OpenStack"""
        cloud_response = await self.connect.volume.create_volume(request)

        """Save the volume in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=db_volume_name,
                                              project_id=project_id, tags=request.tags)
        return await self.db.write_document_with_default_details(Constants.MongoCollection.VOLUME, db_model)

    @log
    async def list_volumes_by_project_id(self, pageable: Pageable = None, project_id: str = None):
        """This method is used to fetch the data of volumes from db.
        :param pageable: Pageable object.
        :param project_id: Project ID.
        :return: List of volumes.
        """
        return await self.db.get_document_list_by_ids(
            collection_name=self.collection,
            pageable=pageable,
            project_id=project_id
        )

    @log
    async def list_all_volumes(self, pageable: Pageable = None, use_db: StrictBool = True):
        """This method is used to fetch the data of all volumes of the organization form db or cloud.
        :param pageable: Pageable object.
        :param use_db: Use db or not.
        :return : List of volumes.
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                exclude_project=True,
                pageable=pageable
            )
        else:
            mapper_res = await self.connect.volume.list_all_volumes()
            return mapper_res, len(mapper_res)

    @log
    async def get_volume(self, project_id: str, volume_id: str) -> any:
        """This method is used to fetch the data of volume from mongo by using volume_id
        :param volume_id: id of the volume
        :param project_id: Project ID.
        :return: returns the volume data or None
        """

        return await self.db.get_document_by_ids(collection_name=Constants.MongoCollection.VOLUME,
                                                 uid=volume_id,
                                                 project_id=project_id)

    @log
    async def delete_volume(self, project_id: str, volume_id):
        """This method is used to delete a volume in cloud and mongo.
        :param volume_id: Volume ID.
        :param project_id: Project ID.
        :return: None."""

        """DB Response"""
        db_response = await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.VOLUME,
            uid=volume_id,
            project_id=project_id,
            raise_exception=True)

        """Delete the volume in the OpenStack"""
        await self.connect.volume.delete_volume(db_response['reference_id'])

        """Delete the volume in the mongo db"""
        await self.db.soft_delete_document_by_uuid(Constants.MongoCollection.VOLUME, volume_id)

    @log
    async def update_volume(self, project_id, volume_id, request):
        """This method is used to update a volume in db.
        :param project_id: Project ID.
        :param volume_id: Volume ID.
        :param request: Volume request body.
        """

        """check if volume exsit in db and part of this project"""
        await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.VOLUME,
            uid=volume_id,
            project_id=project_id,
            raise_exception=True)

        return await self.db.update_document_by_uuid(Constants.MongoCollection.VOLUME,
                                                     uid=volume_id,
                                                     data_dict=request.dict(include={'name', 'description', 'tags'}))

    @log
    async def attach_volume(self, project_id: str, volume_id: str, instance_id: str):
        """
        This function is used to attach volume to an instance
        :param project_id: Project ID.
        :param volume_id: UUID of the volume
        :param instance_id: UUID of the instance
        :return: None."""

        '''get the volume details from db'''
        volume_db_response = await self.db.get_document_by_ids(Constants.MongoCollection.VOLUME,
                                                               uid=volume_id,
                                                               project_id=project_id,
                                                               raise_exception=True)
        """Instance DB response"""
        instance_db_response = await self.db.get_document_by_ids(collection_name=Constants.MongoCollection.INSTANCE,
                                                                 uid=instance_id,
                                                                 project_id=project_id,
                                                                 raise_exception=True)

        '''get the attached instance IDs'''
        attached_instance_ids = [attached_instance.get(
            'instance_id') for attached_instance in volume_db_response['attachments']]

        cloud_volume_id = volume_db_response['cloud_meta']['name']
        volume_cloud = volume_db_response['cloud_meta']

        # If volume is already attached to the given instance then raise an exception
        if Utils.is_found(instance_id, attached_instance_ids):
            raise CCPBusinessException(
                Message.VOLUME_ALREADY_ATTACHED.format(volume_id, instance_id))

        instance_cloud = instance_db_response['cloud_meta']

        '''attach the volume to the instance'''
        await self.connect.volume.attach_volume(instance_cloud, volume_cloud)

        '''get the volume details from cloud'''
        cloud_response = await self.connect.volume.get_volume(cloud_volume_id)

        attachments = volume_db_response['attachments']
        attachments.append({
            'instance_id': instance_id,
            'attached_at': Utils.get_utc_datetime(),
        })

        '''update the volume details in db'''
        await self.update_volume_db_data(cloud_response, volume_id, attachments)

    @log
    async def detach_volume(self, project_id: str, volume_id: str, instance_id: str):
        """
        Detach volume from instance
        :param project_id: id of the project
        :param volume_id: id of the volume
        :param instance_id: id of the instance
        :return: None
        """
        '''get the volume details'''
        volume_db_response = await self.db.get_document_by_ids(collection_name=Constants.MongoCollection.VOLUME,
                                                               uid=volume_id,
                                                               project_id=project_id,
                                                               raise_exception=True)

        """Instance DB response"""
        instance_db_response = await self.db.get_document_by_ids(collection_name=Constants.MongoCollection.INSTANCE,
                                                                 uid=instance_id,
                                                                 project_id=project_id,
                                                                 raise_exception=True)

        # If volume is not attached to any instance then raise an exception
        if not volume_db_response['attachments']:

            raise CCPBusinessException(
                Message.VOLUME_NOT_ATTACHED.format(volume_id, instance_id))

        attached_instance_ids = [attached_instance.get('instance_id') for attached_instance in
                                 volume_db_response['attachments']]

        # If volume is not attached to the given instance then raise an exception
        if not Utils.is_found(instance_id, attached_instance_ids):
            raise CCPBusinessException(
                Message.VOLUME_NOT_ATTACHED.format(volume_id, instance_id))

        cloud_volume_id = volume_db_response['cloud_meta']['name']
        volume_cloud = volume_db_response['cloud_meta']

        instance_cloud = instance_db_response['cloud_meta']

        '''detach the volume from the instance'''
        await self.connect.volume.detach_volume(instance_cloud, volume_cloud)

        '''get the volume details from cloud'''
        cloud_response = await self.connect.volume.get_volume(cloud_volume_id)

        attachments = volume_db_response['attachments']

        # Remove the detached instance from the attachments list
        for item in attachments:
            if item['instance_id'] == instance_id:
                attachments.remove(item)
                break

        '''update the volume details in db'''
        await self.update_volume_db_data(cloud_response, volume_id, attachments)

    @log
    async def update_volume_db_data(self, cloud_response, volume_id, attachments):
        """update the volume details in mongo db
        :param cloud_response: cloud volume details
        :param volume_id: volume id
        :param attachments: attachments list
        """
        await self.db.update_document_by_uuid(Constants.MongoCollection.VOLUME,
                                              uid=volume_id,
                                              data_dict={
                                                  'cloud_meta': cloud_response.cloud_meta,
                                                  'volume_type': cloud_response.volume_type,
                                                  'is_bootable': cloud_response.is_bootable,
                                                  'is_encrypted': cloud_response.is_encrypted,
                                                  'is_multiattach': cloud_response.is_multiattach,
                                                  'attachments': attachments,
                                                  'status': cloud_response.status}
                                              )
