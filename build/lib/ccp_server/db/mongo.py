##############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved    #
# Unauthorized copying of this file, via any medium is strictly prohibited   #
# Proprietary and confidential                                               #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                  #
##############################################################################
import traceback
import uuid
from datetime import datetime
from typing import Dict
from typing import List
from typing import Tuple

import motor.motor_asyncio

from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.util import ccp_context
from ccp_server.util import env_variables
from ccp_server.util.constants import Constants
from ccp_server.util.enums import Status
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.exceptions import CCPException
from ccp_server.util.exceptions import CCPNotFoundException
from ccp_server.util.logger import KGLogger
from ccp_server.util.messages import Message
from ccp_server.util.utils import Utils

LOG = KGLogger(name=__name__)


class MongoAPI(object):
    def __init__(self, conn_str: str = None, db_name: str = None):
        # Initialize client and DB

        conn_str = conn_str if conn_str else env_variables.MONGO_DB_URL
        db_name = db_name if db_name else Constants.MONGO_DB_NAME

        self.conn_str = conn_str
        self._client = motor.motor_asyncio.AsyncIOMotorClient(self.conn_str)
        self._db = self._client[db_name]

    @property
    def db(self):
        if self._db is None:
            self._db = self._client[Constants.MONGO_DB_NAME]
        return self._db

    @property
    def client(self):
        if not self._client:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(
                self._conn_str)
        return self._client

    async def create_capped_collection(self, collection_name, max_size_bytes, max_count):
        collection_names = await self._db.list_collection_names()
        if collection_name in collection_names:
            LOG.info(f"Collection {collection_name} detected")
            return
        await self._db.create_collection(collection_name, size=max_size_bytes, capped=True, max=max_count)

    async def get_document_by_uuid(self, collection_name, uid, projection_dict: dict = {},
                                   raise_exception: bool = True) -> Dict:
        """
        Get a document by uuid. This uuid is for API management
        :param collection_name: Name of the collection
        :param uid: uuid to look for
        :param projection_dict: Projection dictionary
        :param raise_exception: Raise exception if document not found
        :return: returns document as dict or None
        """
        filter_dict = {'uuid': uid}
        cloud = ccp_context.get_cloud()

        if cloud:
            filter_dict['cloud'] = cloud

        projection_dict.update({
            '_id': 0})
        result = await self.get_document_by_projection_and_filter(collection_name, filter_dict, projection_dict)

        # If no document is found, return None else return the first document
        if len(result) != 0:
            return result[0]
        elif raise_exception:
            raise CCPNotFoundException(
                message=f"Document with uuid {uid} not found")
        return None

    async def get_document_by_ids(self,
                                  collection_name: str,
                                  uid: str,
                                  project_id: str = None,
                                  cloud: str = None,
                                  org_id: str = None,
                                  projection_dict={},
                                  exclude_org: bool = False,
                                  exclude_project: bool = False,
                                  filter_dict: Dict = None,
                                  raise_exception: bool = True) -> Dict:

        """
        Get a document by uuid, cloud, org_id and project_id if applicable. This uuid is the unique key of the object
        :param collection_name: Name of the collection
        :param uid: uuid to look for
        :param project_id: Project id
        :param cloud: Cloud name to look for, if not provided, it will be fetched from ccp_context.get_cloud()
        :param org_id: Organization name to look for, if not provided, it will be fetched from ccp_context.get_org()
        :param projection_dict: Projection dictionary
        :param exclude_org: True if we want to exclude the org_id from the filter
        :param exclude_project: True if we want to exclude the project_id from the filter
        :param raise_exception: Raise exception if document not found
        :param filter_dict: Filter dictionary
        :return: returns document as dict or None. The dict will have the keys: uuid, cloud, org_id, project_id,
                cloud_meta, reference_id, created_at, updated_at, created_by, updated_by
        """

        _filter_dict = self.populate_default_filter_dict(cloud=cloud, org_id=org_id, project_id=project_id,
                                                         exclude_org=exclude_org, exclude_project=exclude_project)
        _filter_dict.update({'uuid': uid})
        projection_dict.update({
            '_id': 0})
        if filter_dict:
            _filter_dict.update(filter_dict)
        result = await self.get_document_by_projection_and_filter(collection_name, _filter_dict, projection_dict)
        # If no document is found, return None else return the first document
        if result:
            return result[0]
        elif raise_exception:
            raise CCPNotFoundException(
                message=f"Document with uuid {uid} not found")
        return None

    def populate_default_filter_dict(self, cloud: str = None, org_id: str = None, project_id: str = None,
                                     created_by: str = None,
                                     exclude_org: bool = False, exclude_project: bool = False) -> Dict:
        filter_dict = {}
        if not cloud:
            cloud = ccp_context.get_cloud()
        if not org_id:
            org_id = ccp_context.get_org()
        # TODO: remove this
        if not project_id and not exclude_project:
            project_id = ccp_context.get_project_id()

        # Adds only the cloud, org_id and project_id if they are not None
        if cloud:
            filter_dict['cloud'] = cloud
        if org_id:
            filter_dict['org_id'] = org_id
        if project_id:
            filter_dict['project_id'] = project_id
        if created_by:
            filter_dict['created_by'] = created_by
        if exclude_org and 'org_id' in filter_dict:
            filter_dict.pop('org_id')

        return filter_dict

    async def get_document_list_by_ids(self,
                                       collection_name: str,
                                       project_id: str = None,
                                       cloud: str = None,
                                       org_id: str = None,
                                       created_by: str = None,
                                       projection_dict={},
                                       exclude_org: bool = False,
                                       exclude_project: bool = False,
                                       pageable: Pageable = None,
                                       filter_dict: Dict = None,
                                       ) -> Tuple[List[Dict], int]:
        """
        Get the document list by cloud, org_id and project_id if applicable.
        :param collection_name: Name of the collection
        :param project_id: Project id
        :param cloud: Cloud name to look for, if not provided, it will be fetched from ccp_context.get_cloud()
        :param org_id: Organization name to look for, if not provided, it will be fetched from ccp_context.get_org()
        :param created_by: Created by
        :param projection_dict: Projection dictionary
        :param exclude_org: True if we want to exclude the org_id from the filter
        :param exclude_project: True if we want to exclude the project_id from the filter
        :param pageable: Pageable object
        :param filter_dict: Filter dictionary
        :return: returns list of document as list[dict] or None. The dict will have the keys: uuid, cloud, org_id,
                project_id, created_at, updated_at, created_by, updated_by
        """
        _filter_dict = self.populate_default_filter_dict(cloud=cloud, org_id=org_id, project_id=project_id,
                                                         exclude_org=exclude_org, exclude_project=exclude_project,
                                                         created_by=created_by)

        # if 'active' not in filter_dict:
        _filter_dict['active'] = Status.ACTIVE.value
        if filter_dict:
            _filter_dict.update(filter_dict)

            # TODO as description is not mandatory, removing it from the filter_dict
            # filter_dict["description"] = {"$regex": f".*{query_str}.*", "$options": "i"}

        sort = []

        docs = []
        collection_obj = self.db[collection_name]

        projection_dict.update({'reference_id': 0,
                                'cloud_meta': 0,
                                '_id': 0})

        if pageable:
            if pageable.query_str is not None:
                _filter_dict["name"] = {
                    "$regex": f".*{pageable.query_str}.*", "$options": "i"}
            if pageable.sort_by is not None:
                for field in pageable.sort_by:
                    sort.append((field, -1 if pageable.sort_desc else 1))
            else:
                sort.append(
                    ('created_by_str', -1 if pageable.sort_desc else 1))

            # skip value will be page-1 * size, means mongo will skip the number of skipped documents
            skip: int = (pageable.page - 1) * pageable.size
            if pageable.tags:
                # TO add the tags in filter creates the syntax like tags.name: "value1" and tags.type: "value2"
                _filter_dict = {f"tags.{key}": value for key,
                                value in pageable.tags.items()}
            cursor = collection_obj.find(_filter_dict, projection_dict).sort(
                sort).skip(skip).limit(Constants.DOCUMENT_TO_LIST_SIZE)
            docs = await cursor.to_list(length=Constants.DOCUMENT_TO_LIST_SIZE)
        else:
            cursor = collection_obj.find(_filter_dict, projection_dict)
            docs = await cursor.to_list(length=Constants.DOCUMENT_TO_LIST_SIZE)

        await self.update_dates(docs)

        total = await collection_obj.count_documents(_filter_dict)
        return docs, total

    async def get_document_by_projection_and_filter(self, collection_name, filter_dict={},
                                                    projection_dict={}):
        docs = []
        collection_obj = self.db[collection_name]
        # msidana: no need to await here as its a cursor.
        # Added active to the filter_dict to search for only active resources
        if 'active' not in filter_dict:
            filter_dict['active'] = Status.ACTIVE.value
        cursor = collection_obj.find(filter_dict, projection_dict)
        docs = await cursor.to_list(length=Constants.DOCUMENT_TO_LIST_SIZE)

        await self.update_dates(docs)
        return docs

    async def update_dates(self, docs):
        """Updates the created_by_str and updated_by_str fields in the documents"""
        for doc in docs:
            if 'created_at' in doc and doc['created_at'] is not None and isinstance(doc['created_at'], datetime):
                doc['created_at'] = doc['created_at'].strftime(
                    Constants.TIMESTAMP_FORMAT)
            if 'updated_at' in doc and doc['updated_at'] is not None and isinstance(doc['updated_at'], datetime):
                doc['updated_at'] = doc['updated_at'].strftime(
                    Constants.TIMESTAMP_FORMAT)

    async def check_document_by_name(self, collection_name: str, name: str, project_id: str = None,
                                     cloud: str = None, org_id: str = None, raise_exception: bool = False,
                                     filter_dict: dict = None) -> bool:
        """
        Check if a document exists by name.
        :param collection_name: Name of the collection
        :param name: Name of the document
        :param project_id: Project id
        :param cloud: Cloud name to look for, if not provided, it will be fetched from ccp_context.get_cloud()
        :param org_id: Organization name to look for, if not provided, it will be fetched from ccp_context.get_org()
        :param raise_exception: If true, raise exception if document does not exist
        :param filter_dict: Filter dictionary"""

        _filter_dict = self.populate_default_filter_dict(
            cloud=cloud, org_id=org_id, project_id=project_id)
        _filter_dict.update(
            {'name': {"$regex": f".*{name}.*", "$options": "i"}})
        if filter_dict:
            _filter_dict.update(filter_dict)

        doc = await self.get_document_by_projection_and_filter(collection_name, _filter_dict)

        if doc:
            if raise_exception:
                raise CCPBadRequestException(
                    message=Message.NAME_ALREADY_EXISTS.format(name))
            return True
        return False

    async def check_document_by_uuid(self, collection_name: str, uid: str, project_id: str = None, cloud: str = None,
                                     org_id: str = None, raise_exception: bool = False) -> bool:
        """
        Check if a document exists by uuid
        :param collection_name: Name of the collection
        :param uid: uuid of the document
        :param project_id: Project id
        :param cloud: Cloud name to look for, if not provided, it will be fetched from ccp_context.get_cloud()
        :param org_id: Organization name to look for, if not provided, it will be fetched from ccp_context.get_org()
        :param raise_exception: If true, raise exception if document does not exist"""

        filter_dict = self.populate_default_filter_dict(
            cloud=cloud, org_id=org_id, project_id=project_id)
        filter_dict.update({'uuid': uid})

        doc = await self.get_document_by_projection_and_filter(collection_name, filter_dict)

        if doc:
            if raise_exception:
                raise CCPBadRequestException(
                    message=Message.UUID_ALREADY_EXISTS.format(uid))

            return True
        return False

    async def write_document_with_default_details(self, collection_name, document_dict,
                                                  exclude_org: bool = False, exclude_project: bool = False, ):
        """
        Write a document with default details like created_at, created_by, cloud and org_id
        :param collection_name: Name of the collection
        :param document_dict: Document dict
        :param exclude_org: True if we want to exclude the org_id from the filter
        :param exclude_project: True if we want to exclude the project_id from the filter
        :return: returns document as dict or None. The dict will have the keys: uuid, cloud, org_id, project_id,
                reference_id, created_at, updated_at, created_by, updated_by
        """

        # converts object into dict to add default values
        if not isinstance(document_dict, dict):
            document_dict: dict = vars(document_dict)

        # Add created_by from ccp_context
        if ccp_context.get_logged_in_user():
            document_dict.update(
                {'created_by': ccp_context.get_logged_in_user()})

        if 'cloud' not in document_dict or not document_dict['cloud']:
            """Added cloud from ccp_context"""
            document_dict.update(
                {'cloud': ccp_context.get_cloud()})

        if 'org_id' not in document_dict or not document_dict['org_id'] and not exclude_org:
            """Added org_id from ccp_context"""
            document_dict.update({'org_id': ccp_context.get_org()})

        if 'project_id' not in document_dict or not document_dict['project_id'] and not exclude_project:
            """ Added project_id from ccp_context"""
            document_dict.update({'project_id': ccp_context.get_project_id()})

        _, doc_id = await self.write_document(collection_name, document_dict)
        return doc_id

    async def write_document(self, collection_name, document_dict):
        try:
            if 'uuid' not in document_dict:
                doc_id = str(uuid.uuid4())
                data_with_uuid = {'uuid': doc_id}
                data_with_uuid.update(document_dict)
            else:
                doc_id = str(document_dict['uuid'])
                data_with_uuid = document_dict

            # Remove empty values from dict
            data_with_uuid = {k: v for k,
                              v in data_with_uuid.items() if v is not None}

            collection_obj = self.db[collection_name]
            result = await collection_obj.insert_one(data_with_uuid)
            return repr(result.inserted_id), doc_id
        except Exception as e:
            LOG.error('Error occurred while performing database operation.', e)
            return None, None

    async def write_many(self, collection_name, document_list):
        if not isinstance(document_list, list):
            raise CCPException(
                message=Message.DOCUMENT_LIST)
        try:
            collection_obj = self.db[collection_name]

            data_list = []
            for document_dict in document_list:
                if 'uuid' not in document_dict:
                    data_with_uuid = {'uuid': uuid.uuid4()}
                    data_list.append(data_with_uuid.update(document_dict))
                else:
                    data_list.append(document_dict)

            result = await collection_obj.insert_many(data_list)
            return result
        except Exception as e:
            LOG.error(e)
            LOG.error(traceback.print_exc())

    async def update_document_by_uuid(self, collection_name, uid, data_dict):
        try:
            collection = self.db[collection_name]

            # Convert the object into dict
            if type(data_dict) is object:
                data_dict = vars(data_dict)

            # Adding the updated by from ccp_context and updated_at
            data_dict.update({'updated_by': ccp_context.get_logged_in_user(),
                              'updated_at': Utils.get_utc_datetime()})

            update_dict = {"$set": data_dict}

            collection.update_one({'uuid': uid}, update_dict,
                                  upsert=False)
            return None
        except Exception as e:
            LOG.error('Error occurred while performing database operation.', e)
            return False

    async def get_document_count_by_filter(self, collection_name, filter_dict):
        collection = self.db[collection_name]
        count = await collection.count_documents(filter=filter_dict)
        return count

    async def soft_delete_document_by_uuid(self, collection_name, uid):
        """Soft delete the project into DB means it will be marked as deleted(-1) but not deleted from the DB
        :param collection_name: Name of the collection
        :param uid: uuid to look for
        :return: returns None"""

        await self.update_document_by_uuid(collection_name, uid, {'active': Status.DELETED.value})

    async def delete_document_by_uuid(self, collection_name, uid):
        collection = self.db[collection_name]
        query = {"uuid": uid}
        result = collection.delete_one(query)
        var = result.deleted_count == 1
        return bool(var)

    async def get_cloud_by_org_id(self, org_id: str) -> str:
        doc = await self.get_document_by_uuid(Constants.MongoCollection.ORGANIZATION, org_id)
        return doc['default_cloud']

    @staticmethod
    def populate_db_model(cloud_res, name: str = None, description: str = None, project_id: str = None,
                          **kwargs):
        """This method is used to populate the db model from cloud response.
        :param cloud_res: Cloud response.
        :param name: name of the object.
        :param description: description of the object.
        :param project_id: project id
        :param kwargs: other params
        :return: db model"""

        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['project_id'] = project_id

        return MongoAPI.__populate_db_model_from_response(cloud_res, **kwargs)

    @staticmethod
    def __populate_db_model_from_response(response, **kwargs):
        """This method is used to populate the db model from cloud response.
        :param response: cloud response
        :param kwargs: other params
        :return: db model"""
        response = dict(response)
        for key, value in kwargs.items():
            if value:
                response[key] = value
        return response

    async def get_document_by_id_or_name(self,
                                         collection_name: str,
                                         uid: str,
                                         name: str,
                                         project_id: str = None,
                                         cloud: str = None,
                                         org_id: str = None,
                                         projection_dict={},
                                         exclude_org: bool = False,
                                         exclude_project: bool = False,
                                         filter_dict: Dict = None,
                                         raise_exception: bool = True):
        """
        This method is used to get the document by id or name.
        :param collection_name: Name of the collection
        :param uid: uuid to look for
        :param project_id: Project id
        :param cloud: Cloud name to look for, if not provided, it will be fetched from ccp_context.get_cloud()
        :param org_id: Organization name to look for, if not provided, it will be fetched from ccp_context.get_org()
        :param projection_dict: Projection dictionary
        :param exclude_org: True if we want to exclude the org_id from the filter
        :param exclude_project: True if we want to exclude the project_id from the filter
        :param raise_exception: Raise exception if document not found
        :param filter_dict: Filter dictionary
        :return: returns document as dict or None. The dict will have the keys: uuid, cloud, org_id, project_id,
                cloud_meta, reference_id, created_at, updated_at, created_by, updated_by
        """
        _filter_dict = self.populate_default_filter_dict(cloud=cloud, org_id=org_id, project_id=project_id,
                                                         exclude_org=exclude_org, exclude_project=exclude_project)

        _filter_dict.update({"$or": [{"uuid": uid}, {"name": name}]})

        projection_dict.update({
            '_id': 0})
        if filter_dict:
            _filter_dict.update(filter_dict)
        result = await self.get_document_by_projection_and_filter(collection_name, _filter_dict, projection_dict)
        # If no document is found, return None else return the first document
        if result:
            return result[0]
        elif raise_exception:
            raise CCPNotFoundException(
                message=f"Document with uuid {uid} or {name} not found")
        return None

    async def get_document_by_reference_id(self, collection_name, reference_id):
        """
        This method is used to get the document by reference id.
        :param collection_name:
        :param reference_id: cloud reference id of the document
        :return:document object of db
        """
        collection_documents = await self.get_document_by_projection_and_filter(collection_name,
                                                                                {'reference_id': reference_id})
        if collection_documents:
            return collection_documents[0]
