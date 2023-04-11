###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.exceptions import CCPNotFoundException
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class KeyPairService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.KEYPAIR

    @log
    async def create_keypair(self, request):
        """
        Create a new keypair with the given name and public key
        :param request: Contains Name of the keypair and the public key
        :param project_id: Project id
        :return: id of the keypair
        """

        cloud = ccp_context.get_cloud()
        user = ccp_context.get_logged_in_user()
        mongo_response = await self.db.get_document_by_projection_and_filter(self.collection,
                                                                             {"name": request.name,
                                                                              'created_by': user,
                                                                              'cloud': cloud})
        if mongo_response:
            raise CCPBadRequestException(
                message=f"KeyPair with name {request.name} already exists")
        keypair_name = Utils.generate_unique_str()
        cloud_response = await self.connect.compute.keypair.create_keypair(keypair_name, request)
        """ Save Keypair in DB"""
        db_model = MongoAPI.populate_db_model(
            cloud_response, name=request.name)
        return await self.db.write_document_with_default_details(self.collection,
                                                                 db_model)

    @log
    async def list_keypairs(self, pageable: Pageable = None, use_db: StrictBool = True):
        """
        List all keypairs
        :return: List of keypairs
        """
        if use_db:
            user = ccp_context.get_logged_in_user()
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                created_by=user
            )
        else:
            mapper_res = await self.connect.compute.keypair.list_keypairs()
            return mapper_res, len(mapper_res)

    @log
    async def delete_keypair(self, keypair_id: str):
        """
        Delete a keypair
        :param keypair_id: id of the keypair
        :returns: True if delete succeeded, False otherwise.
        """
        user = ccp_context.get_logged_in_user()
        db_response = await self.db.get_document_by_projection_and_filter(self.collection,
                                                                          {'uuid': keypair_id,
                                                                           'created_by': user}
                                                                          )
        if not db_response:
            raise CCPNotFoundException(
                message=f'Keypair with id {keypair_id} not found')
        name = db_response[0]['reference_id']
        """
            Delete the keypair from mongo
        """
        if await self.connect.compute.keypair.delete_keypair(name=name):
            """
                Delete the keypair from mongo if keypair is deleted from cloud
            """
            await self.db.soft_delete_document_by_uuid(self.collection, keypair_id)
