###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, March 2023                    #
###############################################################################
from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.util.constants import Constants


class StorageUser(services.StorageUser):

    def __init__(self, connection: services.Connection):
        self.conn = connection

    def create_storage_user(self, storageuser: models.StorageUser, exist_ok: bool = False):
        """This method is used to create storage user.
        :param storageuser: storage user object
        :param exist_ok: If True, return None if user already exists."""
        cloud_response = self.conn.rgw().create_user(uid=storageuser.email,
                                                     display_name=storageuser.name,
                                                     email=storageuser.email,
                                                     user_caps='buckets=*',
                                                     max_buckets=Constants.MAX_BUCKETS)

        access_key = cloud_response.get('keys')[0]['access_key']
        secret_key = cloud_response.get('keys')[0]['secret_key']

        return {'access_key': access_key, 'secret_key': secret_key}
