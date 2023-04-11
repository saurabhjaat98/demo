###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from typing import Dict
from typing import List
from typing import Tuple

from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.enums import InstanceActionEnum
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils

LOG = KGLogger(__name__)


class InstanceService(Provider):
    collection = Constants.MongoCollection.INSTANCE

    @log
    async def create_instance(self, project_id: str, request):
        """
        Create a new instance with the given name and the server details
        :param project_id: str
        :param request: Contains Name of the instance and the public key
        returns: The created compute ``Server`` object
        """
        await self.db.check_document_by_name(self.collection,
                                             name=request.name,
                                             project_id=project_id,
                                             raise_exception=True
                                             )

        LOG.info(
            f"Checking that the network exists in the same project: {request.network}")
        network_obj = await self.db.get_document_by_ids(Constants.MongoCollection.NETWORK,
                                                        uid=request.network,
                                                        project_id=project_id)
        request.network = network_obj['reference_id']
        if request.instance_username:
            request.userdata = f'''#cloud-config
                    users:
                      - name: {request.instance_username}
                        password: {request.instance_password}
                    '''
        db_instance_name = request.name
        request.name = Utils.generate_unique_str()

        """Creating instance in cloud"""
        LOG.info(
            f"Creating the instance {request.name} in cloud with network_id: {request.network}")
        cloud_response = await self.connect.compute.instance.create_instance(request)

        """Saving instance in the mongo"""
        LOG.info(f"Saving the instance {request.name} in the Database")
        db_model = MongoAPI.populate_db_model(cloud_response, name=db_instance_name, description=request.description,
                                              project_id=project_id, tags=request.tags)
        return await self.db.write_document_with_default_details(self.collection,
                                                                 db_model)

    @log
    async def delete_instance(self, project_id: str, instance_id: str):
        """
        Delete an instance
        :param instance_id: id of the instance
        :param project_id: id of the project
        :return: None
        """
        db_response = await self.db.get_document_by_ids(self.collection,
                                                        uid=instance_id,
                                                        project_id=project_id,
                                                        raise_exception=True
                                                        )
        await self.connect.compute.instance.delete_instance(instance_id=db_response['reference_id'])
        await self.db.soft_delete_document_by_uuid(self.collection,
                                                   uid=instance_id
                                                   )

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_instances(self, pageable: Pageable = None, use_db: StrictBool = True) -> Tuple[List[Dict], int]:
        """
        List all instances
        :param pageable: Pageable object
        :param use_db: Use db or not.
        :return: List of instances
        """
        if use_db:
            return await self.db.get_document_list_by_ids(self.collection,
                                                          pageable=pageable,
                                                          exclude_project=True
                                                          )
        else:
            return await self.connect.compute.instance.list_all_instances()

    @log
    async def list_instances_by_project_id(self, pageable: Pageable = None, project_id: str = None):
        """
        List all instances
        :param pageable: Pageable object
        :param project_id: project id
        :return: List of instances
        """
        return await self.db.get_document_list_by_ids(self.collection,
                                                      pageable=pageable,
                                                      project_id=project_id,
                                                      )

    @log
    async def update_instance(self, project_id, instance_id, request):
        """
        Update an instance
        :param instance_id: id of the instance
        :param name: name of the instance
        :param description: description of the instance
        :param project_id: id of the project
        :return: None
        """

        """ check if Instance exsit in db and part of this project"""
        await self.db.get_document_by_ids(
            collection_name=Constants.MongoCollection.INSTANCE,
            uid=instance_id,
            project_id=project_id,
            raise_exception=True)

        await self.db.update_document_by_uuid(Constants.MongoCollection.INSTANCE,
                                              uid=instance_id,
                                              data_dict=request.dict(include={'name', 'description', 'tags'}))

    @log
    async def instance_action(self, project_id: str, instance_id: str, action: InstanceActionEnum, actions_schema):
        """
        Perform an action on an instance
        :param instance_id: id of the instance
        :param action: action to perform
        :param actions_schema: actions schema
        :param project_id: id of the project
        :return: None
        """
        vm_state_dict = {InstanceActionEnum.STOP: 'stopped',
                         InstanceActionEnum.START: 'active',
                         InstanceActionEnum.REBOOT: 'rebooting',
                         InstanceActionEnum.REBUILD: 'rebuilding',
                         InstanceActionEnum.RESIZE: 'resizing',
                         InstanceActionEnum.RESUME: 'resuming',
                         InstanceActionEnum.PAUSE: 'paused',
                         InstanceActionEnum.UNPAUSE: 'unpause',
                         }

        db_response = await self.db.get_document_by_ids(self.collection,
                                                        uid=instance_id,
                                                        project_id=project_id,
                                                        raise_exception=True
                                                        )
        await self.connect.compute.instance.instance_action(instance_id=db_response['reference_id'],
                                                            action=action, action_schema=actions_schema)

        await self.db.update_document_by_uuid(Constants.MongoCollection.INSTANCE,
                                              uid=instance_id,
                                              data_dict={'status': action, 'vm_state': vm_state_dict[action]})
