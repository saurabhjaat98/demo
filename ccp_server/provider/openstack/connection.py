###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Any
from typing import Dict

import boto.s3.connection
import httplib2
import openstack
from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from openstack import connection
from openstack.connection import Connection as _Connection
from pydantic import StrictStr
from rgwadmin import RGWAdmin

from ccp_server.provider import services
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPCephException
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message
from ccp_server.util.utils import Utils


class OpenstackConnection(services.Connection):
    # Admin roles
    ADMIN_ROLES = [Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN, Constants.CCPRole.PROJECT_ADMIN,
                   Constants.CCPRole.MEMBER]
    os_connections: Dict[StrictStr, _Connection] = {}

    @log
    def connect(self):
        try:
            cloud_name = ccp_context.get_cloud()
            cloud: Dict[StrictStr, Any] = Utils.load_cloud_details(cloud_name)
            if any(role.lower() in ccp_context.get_logged_in_user_roles() for role in OpenstackConnection.ADMIN_ROLES):
                """get openstack Connection object"""
                os_connection: _Connection = openstack.connect(
                    auth_url=cloud['auth']['auth_url'],
                    username=cloud['auth']['username'],
                    password=cloud['auth']['password'],
                    project_name=cloud['auth']['project_name'],
                    project_domain_id=cloud['auth']['project_domain_id'],
                    user_domain_id=cloud['auth']['user_domain_id'],
                    region_name=cloud['region_name'],
                    identity_api_version=cloud.get(
                        'identity_api_version', '3'),
                    interface=cloud.get('interface', 'public')
                )

                return os_connection
            else:
                http = httplib2.Http(disable_ssl_certificate_validation=True)
                auth_url = cloud.get('auth_url')
                token = ccp_context.get_logged_in_token()
                project = ccp_context.get_cloud_project_id()
                endpoint = auth_url + Constants.OPENSTACK_OPENID_AUTH_URL

                headers, _ = http.request(endpoint, "GET", headers={
                    "Authorization": "Bearer " + token})
                un_scoped_subject_token = headers.get('x-subject-token')

                auth = v3.Token(auth_url=auth_url, token=un_scoped_subject_token, project_name=project,
                                project_domain_name=cloud.get(
                                    'project_domain_id'),
                                reauthenticate=False)

                sess = Session(auth=auth)
                os_connection = connection.Connection(
                    session=sess,
                    user_domain_name=cloud.get('user_domain_id'),
                    region_name=cloud.get('region_name'),
                    compute_api_version='2',
                    identity_interface='internal'
                )
                # TODO: Need to configure connection for all user.
            return os_connection.list_images()
        except Exception:
            raise CCPOpenStackException(
                message=Message.OPENSTACK_CONNECTION_ERR_MSG.format(ccp_context.get_cloud()))

    @log
    def botoclient(self):
        """This method is used to get botoclient object for perfrom bucket operation in  storage
        :return: botoclient object"""
        access_key, secret_key = ccp_context.get_logged_in_user_ceph_details()
        try:
            return boto.connect_s3(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                port=Constants.CEPH_OBJECT_GATEWAY_PORT,
                host=Constants.CEPH_OBJECT_GATEWAY_HOST,
                is_secure=False,
                calling_format=boto.s3.connection.OrdinaryCallingFormat(),
            )
        except Exception:
            raise CCPCephException(
                message=Message.CEPH_CONNECTION_ERR_MSG.format(ccp_context.get_cloud()))

    @log
    def rgw(self):
        """This method is used to get rgw object for create user in storage
        :return: rgw object"""
        try:
            return RGWAdmin(access_key=Constants.CEPH_ACCESS_KEY_ID,
                            secret_key=Constants.CEPH_SECRET_ACCESS_KEY,
                            server=Constants.CEPH_CLUSTER_SERVER,
                            verify=Constants.CEPH_SECURE_CONNECTION,
                            secure=Constants.CEPH_SECURE_CONNECTION)
        except Exception:
            raise CCPCephException(
                message=Message.CEPH_CONNECTION_ERR_MSG.format(ccp_context.get_cloud()))
