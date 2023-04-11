###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
import os
from typing import List

from distutils.sysconfig import get_python_lib

from ccp_server.util import env_variables


def convert_to_bytes(size):
    size = size.strip()
    actual_size = int(size[:-1])
    unit = size[-1]
    units = {'B': 0, 'K': 1, 'M': 2, 'G': 3, 'T': 4}
    return int(float(actual_size) * (1024 ** units[unit]))


class Constants(object):
    class CCPHeader:
        """Header for CCP"""
        AUDIT_ID = 'audit-id'
        CLOUD_ID: str = 'cloud-id'
        ORG_ID: str = 'org-id'
        PROJECT_ID: str = 'project-id'
        DEFAULT_PROJECT_NAME: str = 'default'

    class MongoCollection:
        """Class for MongoDB collection constants"""

        ORGANIZATION: str = 'Organization'
        PROJECT: str = 'Project'
        USER: str = 'User'
        INSTANCE: str = 'Instance'
        NETWORK: str = 'Network'
        SUBNET: str = 'Subnet'
        SECURITY_GROUP: str = 'SecurityGroup'
        FLAVOR: str = 'Flavor'
        KEYPAIR: str = 'KeyPair'
        AGGREGATE: str = 'Aggregate'
        VOLUME: str = 'Volume'
        FLOATING_IP: str = 'FloatingIP'
        IMAGE: str = 'Image'
        PORT: str = 'Port'
        SECURITY_GROUP_RULE: str = 'SecurityGroupRule'
        ROUTER: str = 'Router'
        VOLUME_SNAPSHOT: str = 'VolumeSnapshot'
        Bucket: str = 'Bucket'
        AUDIT_COLLECTION_NAME: str = 'AuditLog'
        CLUSTER_TEMPLATE: str = 'ClusterTemplate'
        CLUSTER: str = 'Cluster'

    class Cluster:
        """Class for COE Cluster"""
        IMAGE: str = env_variables.CLUSTER_IMAGE
        FLAVOR: str = env_variables.CLUSTER_FLAVOR
        DOCKER_VOLUME_SIZE: int = env_variables.CLUSTER_DOCKER_VOLUME_SIZE

    class CCPRole:
        """Class for CCP ROles"""
        SUPER_ADMIN: str = 'super-admin'
        ORG_ADMIN: str = 'org-admin'
        PROJECT_ADMIN: str = 'project-admin'
        BILLING_ADMIN: str = 'billing-admin'
        MEMBER: str = 'member'
        READER: str = 'reader'

    # Cloud constants
    CLOUD_TYPE_AWS: str = "aws"
    CLOUD_TYPE_GCP: str = "gcp"
    CLOUD_TYPE_OPENSTACK: str = "openstack"
    CLOUD_TYPE_AZURE: str = "azure"

    # Project constants
    MONGO_DB_NAME: str = 'ccp_db'
    CCP_AUDIT_DB_NAME: str = 'ccp_audit_db'
    USERNAME = 'username'
    CLOUD_PROJECT_ID = 'cloud-project-id'
    CCP_ROLES: str = 'ccp_roles'
    LOGGED_IN_USER_TOKEN: str = 'token'
    CURRENT_REQUEST = 'current_request'
    PATH_ID_REGEX = '/{}/[a-f0-9-]+/?'
    CEPH_USER_ACCESS_KEY: str = 'access_key'
    CEPH_USER_SECRET_KEY: str = 'secret_key'

    # Keycloak constants
    KEYCLOAK_REALM: str = env_variables.KEYCLOAK_REALM
    KEYCLOAK_URL: str = f'{env_variables.KEYCLOAK_HOST_PROTOCOL}://{env_variables.KEYCLOAK_HOST}'
    KEYCLOAK_ADMIN_BASE_URL = f'{KEYCLOAK_URL}/admin/realms/{KEYCLOAK_REALM}'
    KEYCLOAK_BASE_URL: str = f'{KEYCLOAK_URL}/realms/{env_variables.KEYCLOAK_REALM}'
    KEYCLOAK_AUTHORIZATION_HEADER_KEY: str = 'Authorization'
    KEYCLOAK_CONTENT_TYPE_HEADER_KEY: str = 'Content-Type'
    KEYCLOAK_FORM_URLENCODED_TYPE: str = 'application/x-www-form-urlencoded'
    KEYCLOAK_TOKEN_BEARER: str = 'Bearer '
    KEYCLOAK_CLIENT_ID: str = env_variables.KEYCLOAK_CLIENT_ID
    KEYCLOAK_UI_CLIENT_ID: str = env_variables.KEYCLOAK_UI_CLIENT_ID
    KEYCLOAK_CLIENT_SECRET: str = env_variables.KEYCLOAK_CLIENT_SECRET
    KEYCLOAK_GRANT_TYPE: str = 'client_credentials'
    KEYCLOAK_USER_VERIFICATION_MAIL_TTL_IN_SEC: int = 86400
    KEYCLOAK_ADMIN_USERNAME: str = env_variables.KEYCLOAK_ADMIN_USERNAME
    KEYCLOAK_ADMIN_PASSWORD: str = env_variables.KEYCLOAK_ADMIN_PASSWORD
    KEYCLOAK_OPENID_CONNECT_TOKEN_URL = f'{KEYCLOAK_URL}/realms/cloud/protocol/openid-connect/token'
    KEYCLOAK_POST_VERIFICATION_LINK = env_variables.KEYCLOAK_POST_VERIFICATION_LINK
    KEYCLOAK_SUPPORTED_EMAIL_ACTION: List[str] = [
        'VERIFY_EMAIL', 'UPDATE_PASSWORD']

    INTERNAL_KEYCLOAK: bool = env_variables.INTERNAL_KEYCLOAK

    # OpenStack constants
    OPENSTACK_MEMBER_ROLE_NAME: str = 'member'
    OPENSTACK_READER_ROLE_NAME: str = 'reader'
    OPENSTACK_OPENID_AUTH_URL = 'auth/OS-FEDERATION/identity_providers/keycloak-oidc-idp/protocols/openid/auth'

    TIMESTAMP_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    MAPPER_YAML_PATH = os.path.join('ccp_server', 'provider', 'openstack', 'mapper', 'clouds',
                                    'mapper.yaml')

    RESTRICTED_EMAIL_FILE_LOCAL_PATH: str = os.path.join(
        'ccp_server', 'files', 'restricted_domains.json')
    RESTRICTED_EMAIL_FILE_DEFAULT_PATH: str = os.path.join(os.sep, get_python_lib(), 'ccp_server', 'files',
                                                           'restricted_domains.json')

    PINCODE_JSON_FILE_LOCAL_PATH: str = os.path.join(
        'ccp_server', 'files', 'pincode.json')
    PINCODE_JSON_FILE_DEFAULT_PATH: str = os.path.join(os.sep, get_python_lib(), 'ccp_server', 'files',
                                                       'pincode.json')

    # Regex Constants
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    FIRST_NAME_REGEX = '^[A-Za-z]{3,20}$'
    LAST_NAME_REGEX = '^[A-Za-z]{3,20}$'
    MOBILE_NUMBER_REGEX = '^$|[1-9][0-9]{9}$'
    POSTAL_CODE_REGEX = '^[1-9][0-9]{5}$'
    CITY_REGEX = '^[A-Za-z]{2,30}$'
    ADDRESS_REGEX = '^$|[A-Za-z0-9_.-]{3,50}$'
    DESCRIPTION_REGEX = '^[A-Za-z0-9.,)( _-]{10,50}$'
    USERNAME_REGEX = '^[a-zA-Z0-9_-]{3,20}$'
    PASSWORD_REGEX = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
    PUBLIC_KEY_REGEX = '^[a-zA-Z -+0-9]+$'
    NAME_REGEX = '^[a-zA-Z0-9][a-zA-Z0-9_-]{1,18}[a-zA-Z0-9]$'
    GST_REGEX = '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    TAN_NUMBER_REGEX = "^[A-Z]{4}[0-9]{5}[A-Z]{1}$"
    UUID4_REGEX = '^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$'
    PINCODE_REGEX = r'\d{6}'

    # Ceph Constants
    CEPH_OBJECT_GATEWAY_PORT = int(env_variables.CEPH_OBJECT_GATEWAY_PORT)
    CEPH_OBJECT_GATEWAY_HOST = env_variables.CEPH_OBJECT_GATEWAY_HOST
    CEPH_CLUSTER_HOST = env_variables.CEPH_CLUSTER_HOST
    CEPH_CLUSTER_PORT = env_variables.CEPH_CLUSTER_PORT
    CEPH_SECURE_CONNECTION = env_variables.CEPH_SECURE_CONNECTION
    CEPH_ACCESS_KEY_ID = env_variables.CEPH_ACCESS_KEY_ID
    CEPH_SECRET_ACCESS_KEY = env_variables.CEPH_SECRET_ACCESS_KEY
    CEPH_CLUSTER_SERVER = f'{CEPH_OBJECT_GATEWAY_HOST}:{CEPH_OBJECT_GATEWAY_PORT}'
    CEPH_CLUSTER_USER = env_variables.CEPH_CLUSTER_USER
    CEPH_CLUSTER_PASSWORD = env_variables.CEPH_CLUSTER_PASSWORD
    MAX_BUCKETS = int(env_variables.MAX_BUCKETS)

    # Redis Constants
    REDIS_URL = env_variables.REDIS_URL
    REDIS_TTL_IN_MINS: int = int(env_variables.REDIS_TTL_IN_MINS)
    REDIS_TTL_IN_SECONDS: int = int(env_variables.REDIS_TTL_IN_MINS) * 60

    # MongoDB Constants
    AUDIT_DOCUMENT_SIZE_PER_ROW: int = 700
    DOCUMENT_TO_LIST_SIZE: int = 250

    # Converting size into bytes
    CAPPED_COLLECTION_MAX_SIZE_BYTES: int = convert_to_bytes(
        env_variables.CAPPED_COLLECTION_MAX_SIZE)

    # Calculates max entries based on capped collection size and size of per row
    CAPPED_COLLECTION_MAX_NUM_ENTRIES: int = CAPPED_COLLECTION_MAX_SIZE_BYTES / \
        AUDIT_DOCUMENT_SIZE_PER_ROW

    # Tag Constants
    MAX_TAG_LENGTH: int = env_variables.MAX_TAG_LENGTH
