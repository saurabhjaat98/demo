###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
import openstack

from ccp_server.util import ccp_context
from ccp_server.util import env_variables
from ccp_server.util import utils
from ccp_server.util.constants import Constants
from ccp_server.util.logger import KGLogger
from ccp_server.util.resource_collection_map import openstack_map
from ccp_syncer.heatstack_resources import StackResources
from ccp_syncer.syncer_util import SyncerService

LOG = KGLogger(__name__)


async def heat_sync_and_add_in_db(resource_collection_map: dict, cloud_conn: object,
                                  db_conn_str: str, db_name: str,
                                  cloud: str = None, source: str = None):
    """
    This method is used to synchronize the stack resources with the mongo db
    :param resource_collection_map: A Resource Collection Map should have the format below:
                                    {'Flavor': ['Flavor', 'get_flavor'],
                                    'Image': ['Image', 'get_image'],
                                    'Network': ['Network', 'get_network'],
                                    }
                                    where the key is the name of the stack resource and the value is a list and the
                                      first element of the list is the name of the collection name and the second
                                      element is the function to get the resource.
    :param cloud: Cloud name
    :param source: Source of the cloud data whether it is created by stack or any other source
    :param cloud_conn: Connection object of the cloud
    :param db_conn_str: Connection string of the mongo db
    :param db_name: Name of the mongo db
    :return: None
    """
    resource_collection_map = resource_collection_map
    r = StackResources(cloud_conn, resource_collection_map)
    stack_resources = r.list_all_stack_resources()
    r.fetch_detailed_resource_to_dict_of_dict(stack_resources=stack_resources)
    s = SyncerService(db_conn_str, db_name)
    for resource in resource_collection_map:
        collection = resource_collection_map[resource][0]
        new_created_cloud_data = await s.syncer(collection_name=collection,
                                                cloud_data=r.resource_details.get(
                                                    collection),
                                                cloud=cloud, source=source)
        if new_created_cloud_data:
            await s.add_in_db(cloud_data=new_created_cloud_data, source=source, collection_name=collection,
                              unmapped=True)


async def heatsyncer():
    """
    This method is used to synchronize the stack resources with the mongo db
    :param resource_collection_map: A Resource Collection Map should have the format below:
    """
    clouds = utils.Utils.load_supported_cloud_details()
    for cloud in clouds:
        ccp_context.set_request_data('cloud-id', cloud)
        if clouds[cloud]['type'] == "openstack":
            cloud_dict = clouds[cloud]
            conn = openstack.connection.Connection(
                auth_url=cloud_dict.get('auth_url'),
                username=cloud_dict.get('username'),
                password=cloud_dict.get('password'),
                project_name=cloud_dict.get('project_name'),
                project_domain_id=cloud_dict.get('project_domain_id'),
                user_domain_id=cloud_dict.get('user_domain_id'),
                region_name=cloud_dict.get('region_name'),
            )
            resource_collection_map = openstack_map
            await heat_sync_and_add_in_db(resource_collection_map, cloud=cloud, source='stack', cloud_conn=conn,
                                          db_conn_str=env_variables.MONGO_DB_URL, db_name=Constants.MONGO_DB_NAME)


if __name__ == '__main__':
    import asyncio

    database_conn = env_variables.MONGO_DB_URL
    clouds = utils.Utils.load_supported_cloud_details()
    for cloud in clouds:
        ccp_context.set_request_data('cloud-id', cloud)
        if clouds[cloud]['type'] == "openstack":
            cloud_dict = clouds[cloud]
            conn = openstack.connection.Connection(
                auth_url=cloud_dict.get('auth_url'),
                username=cloud_dict.get('username'),
                password=cloud_dict.get('password'),
                project_name=cloud_dict.get('project_name'),
                project_domain_id=cloud_dict.get('project_domain_id'),
                user_domain_id=cloud_dict.get('user_domain_id'),
                region_name=cloud_dict.get('region_name'),
            )
            resource_collection_map = openstack_map
        asyncio.run(heat_sync_and_add_in_db(resource_collection_map, cloud=cloud, source='stack', cloud_conn=conn,
                                            db_conn_str=env_variables.MONGO_DB_URL, db_name=Constants.MONGO_DB_NAME))
