import os


# Keycloak imports
KEYCLOAK_HOST = os.environ.get('KEYCLOAK_HOST', '192.168.100.109:30600')
KEYCLOAK_HOST_PROTOCOL = os.environ.get('KEYCLOAK_HOST_PROTOCOL', 'https')
KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM', 'cloud')
KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID', 'ccp-apiserver')
KEYCLOAK_UI_CLIENT_ID = os.environ.get('KEYCLOAK_UI_CLIENT_ID', 'ccp-react')
KEYCLOAK_CLIENT_SECRET = os.environ.get(
    'KEYCLOAK_CLIENT_SECRET', 'te0cXJGv10TyZfScWXHgy4YegDf75oZB')
KEYCLOAK_ADMIN_USERNAME = os.environ.get('KEYCLOAK_ADMIN_USERNAME', 'admin')
KEYCLOAK_ADMIN_PASSWORD = os.environ.get(
    'KEYCLOAK_ADMIN_PASSWORD', 'password123')
KEYCLOAK_POST_VERIFICATION_LINK = os.environ.get(
    'KEYCLOAK_POST_VERIFICATION_LINK', 'http://192.168.100.127:30140/')
INTERNAL_KEYCLOAK = os.environ.get('INTERNAL_KEYCLOAK', False)

# MongoDB imports
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'root')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'password')
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
MONGO_DB_URL = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}'

# For Configuring the mongodb database for Audit Trails
AUDIT_DB_URL = MONGO_DB_URL

# Provide values as 10M, 2G, 3T
CAPPED_COLLECTION_MAX_SIZE = os.environ.get('CAPPED_COLLECTION_MAX_SIZE', '7M')

# CAPPED_COLLECTION_MAX_COUNT = int(os.environ.get('CAPPED_COLLECTION_max_count', '10000'))


# Redis imports
REDIS_URL = os.environ.get('REDIS_URL', "redis://:password@localhost:6379")
REDIS_TTL_IN_MINS = os.environ.get('REDIS_TTL_IN_MINS', '30')

# Ceph imports
CEPH_OBJECT_GATEWAY_PORT = os.environ.get('CEPH_CLUSTER_PORT', 8081)
CEPH_OBJECT_GATEWAY_HOST = os.environ.get(
    'CEPH_CLUSTER_HOST', '91.106.194.216')
CEPH_CLUSTER_PORT = os.environ.get('CEPH_CLUSTER_PORT', '8443')
CEPH_CLUSTER_HOST = os.environ.get('CEPH_CLUSTER_HOST', '91.106.194.222')
CEPH_CLUSTER_USER = os.environ.get('CEPH_CLUSTER_USER', 'bucketuser')
CEPH_CLUSTER_PASSWORD = os.environ.get('CEPH_CLUSTER_PASSWORD', 'bucket123')
CEPH_SECURE_CONNECTION = os.environ.get('CEPH_SECURE_CONNECTION', False)
CEPH_ACCESS_KEY_ID = os.environ.get(
    'CEPH_ACCESS_KEY_ID', 'G11YK6XHWXTCW55A3NLD')
CEPH_SECRET_ACCESS_KEY = os.environ.get(
    'CEPH_SECRET_ACCESS_KEY', 'mJiG8A6rLhcgHBmTQMLXDeMMAHaqEOfBDsMCdAVC')
MAX_BUCKETS = os.environ.get('MAX_BUCKETS', 1000)

# Cluster
CLUSTER_IMAGE = os.environ.get('CLUSTER_IMAGE', 'ubuntu_20.04')
CLUSTER_FLAVOR = os.environ.get('CLUSTER_FLAVOR', 'm1.small')
CLUSTER_DOCKER_VOLUME_SIZE = os.environ.get('CLUSTER_DOCKER_VOLUME_SIZE', 3)

# TAG_Constants
MAX_TAG_LENGTH = os.environ.get('MAX_TAG_LENGTH', 10)
