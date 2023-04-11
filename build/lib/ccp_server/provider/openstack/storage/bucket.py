###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
###############################################################################
# from datetime import datetime
import re

from fastapi import UploadFile

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider import utils
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants

CEPH_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class Bucket(services.Bucket):
    CEPH_PATH_PATTERN = r"\/$"

    def __init__(self, connection: services.Connection):
        self.conn = connection

    async def create_bucket(self, bucket: models.Bucket) -> models.Bucket:
        """This method is used to create bucket in ceph cluster.
        :param bucket: bucket object"""
        cloud_response = self.conn.botoclient().create_bucket(bucket.name)
        return await mapper(data=cloud_response.__dict__, resource_name=Constants.MongoCollection.Bucket)

    async def list_buckets(self):
        """This method is used to list bucket in ceph cluster.
        :return: list of bucket objects"""
        response = self.conn.botoclient().get_all_buckets()
        buckets = []
        for bucket in response:
            buckets.append(bucket.name)
        return {"buckets": buckets}

    async def get_bucket(self, bucket_id: str):
        """This method is used to get bucket in ceph cluster.
        :param bucket_id: bucket id
        :return: bucket object"""
        return self.conn.rgw().get_bucket(bucket_id)

    async def delete_bucket(self, bucket_id: str):
        """This method is used to delete bucket in ceph cluster.
        :param bucket_id: bucket id
        :return: None"""
        return self.conn.botoclient().delete_bucket(bucket_id)

    async def upload_object(self, bucket_id: str, file: UploadFile):
        """This method is used to upload data in bucket in ceph cluster.
        :param bucket_id: bucket id
        :param file: file
        :return: None"""

        # set the bucket name
        bucket = self.conn.botoclient().get_bucket(bucket_id)

        # read the contents of the file into a bytes object
        file_bytes = await file.read()

        # Upload the file to the bucket
        bucket.new_key(file.filename).set_contents_from_string(file_bytes)

    async def get_bucket_objects(self, bucket_id: str):
        """This method is used to list bucket info in ceph cluster.
        :param bucket_id: bucket id
        :return: list of bucket info"""
        bucket = self.conn.botoclient().get_bucket(bucket_id)
        return [{"name": obj.key, "size": obj.size,
                 "updated_at": utils.format_datetime(obj.last_modified, CEPH_TIMESTAMP_FORMAT)} for obj in
                bucket.list()]

    async def delete_object(self, bucket_id: str, key_name: str):
        """This method is used to delete object in bucket in ceph cluster.
        :param bucket_id: bucket id
        :param key_name: key name
        :return: None"""
        self.conn.botoclient().get_bucket(bucket_id).delete_key(key_name)

    async def download_object(self, bucket_id: str, object_name: str, path: str):
        """This method is used to download object from ceph cluster's bucket.
        :param bucket_id: bucket id
        :param object_name: object name
        :param path: path to save the file
        :return: None"""
        # set the bucket name
        bucket = self.conn.botoclient().get_bucket(bucket_id)

        # Get a handle to the object
        s3_key = bucket.get_key(object_name)

        # correct path string.
        corrected_path_string = await self.correct_path(object_name, path)

        # Download the object to a file
        s3_key.get_contents_to_filename(corrected_path_string)

    async def correct_path(self, object_name, path):
        if re.search(Bucket.CEPH_PATH_PATTERN, path):
            correct_path = f'{path}{object_name}'
        else:
            correct_path = f'{path}/{object_name}'
        return correct_path
