###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
import logging
import traceback
import uuid
from datetime import datetime

import motor.motor_asyncio
import pymongo

from ccp_server.provider.openstack.mapper.mapper import mapper

log = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format=f'%(asctime)s %(process)d %(levelname)s Syncer %(filename)s:%(lineno)d %(message)s')
file_handler = logging.FileHandler('/var/log/syncerservice.log')
file_handler.setLevel(logging.INFO)
log.addHandler(file_handler)


class SyncerService:
    """
    This class is used to synchronize the stack resources with the mongo db resources
    """

    class Constants:
        ACTIVE = 1
        INACTIVE = 0
        DELETED = -1
        BATCH_SIZE = 100

    def __init__(self, conn_str, db):
        """
        Constructor for the SyncerService class
        :param conn: Connection object of the mongo db
        :param db: Name of the mongo db
        """
        self.conn_str = conn_str
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.conn_str)
        self.db = self.client[db]
        self.collection_obj = None

    async def add_in_db(self, cloud_data, collection_name, source=None, source_id=None,
                        cloud=None, unmapped=False):
        """
        This method is used to add the stack resources in the mongo db
        :param cloud_data: Cloud data
        :param collection_name: Collection name
        :param source: Source of the cloud data whether it is created by stack or any other source
        :param source_id: Id of the source of the cloud data
        :param cloud: Cloud name
        :param unmapped: True if the cloud data is unmapped else False
        :return: None
        """
        # Todo: Org Id and created by needs to be Implemented
        try:
            if not cloud_data:
                return cloud_data
            new_data = []
            for key in cloud_data:
                document_dict = {'uuid': str(uuid.uuid4())}
                if unmapped:
                    map_obj = await mapper(data=cloud_data[key], resource_name=collection_name,
                                           cloud=cloud)
                    document_dict.update(dict(map_obj.data))
                else:
                    document_dict.update(dict(cloud_data[key]))

                if 'source_id' in document_dict:
                    source_id = document_dict['source_id']
                document_dict['source'] = source
                document_dict['source_id'] = source_id
                new_data.append(document_dict)

            for i in range(0, len(new_data), SyncerService.Constants.BATCH_SIZE):
                batch = new_data[i:i + SyncerService.Constants.BATCH_SIZE]
                try:
                    await self.collection_obj.insert_many(batch)
                except Exception as e:
                    log.error(
                        f"Error while inserting into mongo db of batch {i} due to {e}")
                    log.error(traceback.print_exc())
                log.info(f"Inserted {len(batch)} documents")

        except Exception as e:
            log.error(f"Error while adding in db due to {e}")
            log.error(traceback.print_exc())

    async def syncer(self, collection_name, cloud_data, cloud=None, source=None):
        """
        This method is used to synchronize the stack resources with the mongo db
        :param collection_name: Name of the collection
        :param cloud_data: Cloud data
        :param cloud: Cloud name
        :param source: Source of the cloud data whether it is created by stack or any other source
        :return: None
        """
        try:
            log.info(f"Syncer started for collection {collection_name}")
            self.collection_obj = self.db[collection_name]
            cursor = self.collection_obj.find({'active': 1,
                                               'cloud': cloud,
                                               'source': source})
            update_requests = []
            async for document in cursor:
                resource_id = document['reference_id']
                if resource_id in cloud_data:
                    """ Checking if the mongo resource is equals to cloud resource or not.
                        If changed we will mark flag as 1 and change the document and will update the same
                    """
                    flag = 0
                    for key in document:
                        if key not in cloud_data[resource_id]:
                            continue
                        if document[key] != cloud_data[resource_id][key]:
                            flag = 1
                            document[key] = cloud_data[resource_id][key]
                    if flag == 1:
                        filter_query = {'uuid': {'$eq': document['uuid']}}
                        update_dict = {"$set": cloud_data[resource_id]}
                        update_requests.append(pymongo.UpdateOne(
                            filter_query, update_dict, upsert=False))

                    """Removing the existing data from cloud"""
                    cloud_data.pop(resource_id)

                else:
                    """Setting active = -1 for deleted entry in cloud"""
                    log.info(
                        f"Setting active -1 for deleted resource {resource_id} for collection {collection_name}"
                    )
                    document['active'] = SyncerService.Constants.DELETED
                    document['terminated_at'] = datetime.now()
                    filter_query = {'uuid': {'$eq': document['uuid']}}
                    update_dict = {"$set": document}
                    update_requests.append(pymongo.UpdateOne(
                        filter_query, update_dict, upsert=False))

            """Updating all the update object at once in mongo db"""
            if update_requests:
                result = await self.collection_obj.bulk_write(update_requests)
                if result.modified_count:
                    log.info(f"Updated {result.modified_count} documents")
            log.info(
                f"These are the new resources created in Cloud: {cloud_data}")

            """Returning data which is created in cloud but not exists in DB"""
            return cloud_data
        except Exception as e:
            log.error(
                f"Error while syncing for collection: {collection_name} due to {e}")
            log.error(traceback.print_exc())

    async def convert_to_dict_of_dict(self, cloud_data):
        """
        This method is used to convert the cloud data to dict of dict
        :param cloud_data: List of Cloud data
        :return: Dict of dict
        """
        try:
            temp_dict = {}
            for data in cloud_data:
                data = dict(data)
                temp_dict[data['reference_id']] = data
            return temp_dict
        except Exception as e:
            log.error(f"Error in convert_to_dict_of_dict due to {e}")
            log.error(traceback.print_exc())

    async def sync_and_add_in_db(self, collection_name, cloud_data, cloud=None, source=None,
                                 source_id=None, unmapped=False):
        """
        This method is used to synchronize the cloud resources with the mongo db
        :param collection_name: Name of the collection
        :param cloud_data: Cloud data
        :param cloud: Cloud name
        :param source: Source of the cloud data whether it is created by stack or any other source
        :param source_id: Id of the source of the cloud data
        :param unmapped: True if the cloud data is unmapped else False
        :return: None
        """
        try:
            if isinstance(cloud_data, list):
                cloud_data = await self.convert_to_dict_of_dict(cloud_data)
            new_resources_cloud = await self.syncer(collection_name=collection_name,
                                                    cloud_data=cloud_data,
                                                    cloud=cloud,
                                                    source=source)
        except Exception as e:
            log.error(f"Error while syncing due to {e}")
            log.error(traceback.print_exc())

        try:
            await self.add_in_db(cloud_data=new_resources_cloud, collection_name=collection_name,
                                 source=source, source_id=source_id, cloud=cloud, unmapped=unmapped)
        except Exception as e:
            log.error(f"Error while adding in DB due to {e}")
            log.error(traceback.print_exc())
