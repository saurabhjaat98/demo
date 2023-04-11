# ###############################################################################
# # Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# # Unauthorized copying of this file, via any medium is strictly prohibited    #
# # Proprietary and confidential                                                #
# # Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
# ###############################################################################
import asyncio

from ccp_server.service.networks.network import NetworkService
from ccp_server.util import ccp_context
from ccp_server.util import env_variables
from ccp_server.util import utils
from ccp_server.util.constants import Constants
from ccp_server.util.logger import KGLogger
from ccp_syncer.syncer_util import SyncerService

LOG = KGLogger(__name__)


class SyncResources:
    """
    This class is used to sync the resources
    """

    def __init__(self):
        """
        This function is used to initialize the SyncResources class
        func_map:-  func_map includes the mapping of the class and its function to be executed
                    The key of the map is the collection name and the value is a list, on which
                    0 index represents the service module classes and the 1 index represents
                    the function to be executed.
        """
        self.method = None
        self.__func_map__ = {Constants.MongoCollection.NETWORK: [
            NetworkService, 'list_networks']}

    async def list_resources(self, class_name, method_name):
        """
        This function is used to list the resources
        :param class_name: Class name of the resource
        :param method_name: Method name of the resource
        :return: List of resources
        """
        try:
            class_obj = class_name()
            if hasattr(class_obj, method_name):
                self.method = getattr(class_obj, method_name)
                return await self.method(use_db=False)
            else:
                LOG.error(f"{class_name} does not have {method_name} method")
        except Exception as e:
            LOG.error(f"Exception occurred while listing resources: {e}")

    async def sync_resources(self, collection_name, class_name, method_name, cloud: str = None):
        """
        This function is used to sync the resources
        :param collection_name: Name of the collection
        :param class_name: Class name of the resource
        :param method_name: Method name of the resource
        :param cloud: Cloud name
        :return: None
        """
        ccp_context.set_request_data('cloud-id', cloud)
        resources = await self.list_resources(class_name, method_name)
        syncer_obj = SyncerService(
            conn_str=env_variables.MONGO_DB_URL, db=Constants.MONGO_DB_NAME)
        await syncer_obj.sync_and_add_in_db(collection_name=collection_name,
                                            cloud_data=resources, cloud=cloud)


if __name__ == "__main__":
    sync = SyncResources()
    all_clouds = utils.Utils.load_supported_cloud_details()
    for cloud in all_clouds:
        ccp_context.set_request_data('cloud-id', cloud)
        for collection_name in sync.__func_map__:
            asyncio.run(sync.sync_resources(collection_name, sync.__func_map__[collection_name][0],
                                            sync.__func_map__[collection_name][1], cloud=cloud))
