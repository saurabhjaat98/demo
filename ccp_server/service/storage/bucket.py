###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
###############################################################################
from typing import Dict
from typing import List
from typing import Tuple

from fastapi import UploadFile
from pydantic.types import StrictBool

import ccp_server.provider.models as provider_models
from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.kc.user import KeycloakUserService
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class BucketService(Provider):
    def __init__(self):
        self.kc_user_service: KeycloakUserService = KeycloakUserService()

    @log
    async def create_bucket(self, project_id, request: schemas.Bucket):
        """This method is used to create a bucket in cloud.
        :param project_id: project id
        :param request: Bucket request body.
        :return: """

        cloud_bucket = provider_models.Bucket(name=Utils.generate_unique_str())

        """Save the bucket in the cloud"""
        cloud_response = await self.connect.bucket.create_bucket(cloud_bucket)
        db_model = MongoAPI.populate_db_model(cloud_response, name=request.name, description=request.description,
                                              project_id=project_id, tags=request.tags)

        """Save the bucket in the mongo db"""
        return await self.db.write_document_with_default_details(Constants.MongoCollection.Bucket,
                                                                 db_model)

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_buckets(self, pageable: Pageable = None, use_db: StrictBool = True) -> Tuple[List[Dict], int]:
        """This method is used to list all buckets in cloud.
        :param pageable: Pageable object.
        :param use_db: Use db or not.
        :param project_id: project id
        :return: all buckets in cloud. """
        # TODO: implement anathor api for this org admin
        if use_db:
            return await self.db.get_document_list_by_ids(collection_name=Constants.MongoCollection.Bucket,
                                                          pageable=pageable,
                                                          exclude_project=True)
        else:
            cloud_res = await self.connect.bucket.list_buckets()
            return cloud_res, len(cloud_res)

    @log
    async def list_buckets_by_project_id(self, pageable: Pageable = None,
                                         project_id: str = None) -> Tuple[List[Dict], int]:
        """This method is used to list all buckets in cloud.
        :param pageable: Pageable object.
        :param use_db: Use db or not.
        :param project_id: project id
        :return: all buckets in project. """
        return await self.db.get_document_list_by_ids(collection_name=Constants.MongoCollection.Bucket,
                                                      pageable=pageable,
                                                      project_id=project_id)

    @log
    async def get_bucket(self, project_id: str, bucket_id):
        """This method is used to fetch the bucket's information from cloud .
        :param project_id: project id
        :param bucket_id: bucket id
        :return: bucket information. """
        db_response = await self.db.get_document_by_ids(Constants.MongoCollection.Bucket, bucket_id,
                                                        project_id=project_id)

        bucket_id = db_response.get('reference_id')

        return await self.connect.bucket.get_bucket(bucket_id=bucket_id)

    @log
    async def delete_bucket(self, project_id: str, bucket_id, ):
        """This method is used to delete the bucket from cloud.
        :param project_id: project id
        :param bucket_id: bucket id
        :return: """

        # TODO: don't delete from bucket directly
        db_response = await self.db.get_document_by_ids(Constants.MongoCollection.Bucket, bucket_id,
                                                        project_id=project_id,
                                                        raise_exception=True)
        bucket_id = db_response.get('reference_id')
        await self.connect.bucket.delete_bucket(bucket_id=bucket_id)
        self.db.soft_delete_document_by_uuid(
            Constants.MongoCollection.Bucket, bucket_id)

    @log
    async def upload_object(self, project_id: str, bucket_id: str, file: UploadFile):
        """This method is used to upload object to the bucket.
        :param project_id: project id.
        :param bucket_id: bucket id.
        :param key_name: key name.
        :param file_path: file path.
        :return: """
        db_response = await self.db.get_document_by_ids(Constants.MongoCollection.Bucket, bucket_id,
                                                        project_id=project_id,
                                                        raise_exception=True)
        bucket_id = db_response.get('reference_id')
        return await self.connect.bucket.upload_object(bucket_id, file)

    @log
    async def get_objects(self, project_id: str, bucket_id: str):
        """This method is used to list all objects in the bucket.
        :param project_id: project id.
        :param bucket_id: bucket id.
        :return: """
        db_response = await self.db.get_document_by_ids(Constants.MongoCollection.Bucket, bucket_id,
                                                        project_id=project_id,
                                                        raise_exception=True)
        bucket_id = db_response.get('reference_id')
        return await self.connect.bucket.get_bucket_objects(bucket_id)

    @log
    async def delete_object(self, project_id: str, bucket_id: str, object_name: str):
        """This method is used to delete object from the bucket.
        :param project_id: project id.
        :param bucket_id: bucket id.
        :param object_name: object name.
        :return: """

        db_response = await self.db.get_document_by_ids(Constants.MongoCollection.Bucket, bucket_id,
                                                        project_id=project_id,
                                                        raise_exception=True)
        bucket_id = db_response.get('reference_id')
        await self.connect.bucket.delete_object(bucket_id, object_name)

    @log
    async def download_object(self, project_id: str, bucket_id: str, object_name: str, path: str):
        """This method is used to download object from the bucket.
        :param project_id: project id.
        :param bucket_id: bucket id.
        :param object_name: object name.
        :param path: local download dir path.
        :return: """
        db_response = await self.db.get_document_by_ids(Constants.MongoCollection.Bucket, bucket_id,
                                                        project_id=project_id,
                                                        raise_exception=True)
        bucket_id = db_response.get('reference_id')
        return await self.connect.bucket.download_object(bucket_id, object_name, path)
