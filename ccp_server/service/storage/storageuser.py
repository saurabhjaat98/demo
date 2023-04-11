###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, March 2023                    #
###############################################################################
from ccp_server.provider.models import StorageUser
from ccp_server.service.providers import Provider


class StorageUserService(Provider):
    async def create_storage_user(self, first_name, last_name, email,  exist_ok: bool = False):
        '''This method is used to create storage user.
        :param first_name: First name of the user.
        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param email: Email of the user.
        :param exist_ok: If True, return None if user already exists.
        :return: dict: StorageUser access key secret key if user is created else None.'''
        cloud_user_req = StorageUser(
            email=email, name=f'{first_name} {last_name}')
        return self.connect.storageuser.create_storage_user(cloud_user_req, exist_ok=exist_ok)
