###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from typing import Dict
from typing import List
from typing import Tuple

from pydantic.types import StrictBool

from ccp_server.db.mongo import MongoAPI
from ccp_server.decorators.common import has_role
from ccp_server.provider import models as provider_models
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils


class RouterService(Provider):
    def __init__(self):
        self.collection = Constants.MongoCollection.ROUTER

    @log
    async def create_router(self, project_id: str, router: schemas.Router) -> str:
        """This method is used to create a router in cloud and mongo."""

        """Check for router name if already exist"""
        await self.db.check_document_by_name(
            collection_name=self.collection,
            name=router.name,
            project_id=project_id,
            raise_exception=True)

        """ Cloud project ID """
        db_response = await self.db.get_document_by_uuid(Constants.MongoCollection.PROJECT, uid=project_id,
                                                         raise_exception=True)

        router_model: provider_models.Router = provider_models.Router(
            name=Utils.generate_unique_str(),
            admin_state_up=router.admin_state_up,
            ext_gateway_net_id=router.ext_gateway_net_id,
            enable_snat=router.enable_snat,
            ext_fixed_ips=router.ext_fixed_ips,
            project_id=db_response['reference_id'],
            availability_zone_hints=router.availability_zone_hints
        )

        """Save the router in the OpenStack"""
        cloud_response = await self.connect.router.create_router(router_model)

        """Save the router in the mongo db"""
        db_model = MongoAPI.populate_db_model(cloud_response, name=router.name,
                                              project_id=project_id)
        return await self.db.write_document_with_default_details(self.collection, db_model)

    @log
    async def list_routers_by_project_id(self, pageable: Pageable, project_id: str = None) -> Tuple[List[Dict], int]:
        """ Fetch all the routers in mongo.
        :param pageable: Pageable object
        :param project_id: project id.
        :return: List of networks.
        """
        # TODO : Add filter specific for logged in user
        return await self.db.get_document_list_by_ids(
            collection_name=self.collection,
            pageable=pageable,
            project_id=project_id
        )

    @log
    @has_role(Constants.CCPRole.SUPER_ADMIN, Constants.CCPRole.ORG_ADMIN)
    async def list_all_routers(self, pageable: Pageable, use_db: StrictBool = True):
        """ Fetch all the routers in cloud and mongo.
        :param pageable: Pageable object
        :param use_db: If true it will fetch the result from Mongo, else from cloud
        :return: List of networks.
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection,
                pageable=pageable,
                exclude_project=True
            )
        else:
            mapper_res = await self.connect.router.list_all_routers()
            return mapper_res, len(mapper_res)

    @log
    async def get_router(self, project_id: str, router_id: str) -> Dict:
        """
        :param: router_id -> str
        :return: Dict
        """
        return await self.db.get_document_by_ids(collection_name=self.collection,
                                                 uid=router_id,
                                                 project_id=project_id,
                                                 raise_exception=True)

    @log
    async def delete_router(self, project_id: str, router_id: str) -> None:
        """This method is used to delete the router from mongo.
        :param router_id: id of the router
        :param project_id: id of the project
        :return: None
        """

        """ DB Response """
        router_db_res = await self.db.get_document_by_ids(collection_name=self.collection,
                                                          uid=router_id,
                                                          project_id=project_id,
                                                          raise_exception=True)
        await self.connect.router.delete_router(router_db_res['reference_id'])

        await self.db.soft_delete_document_by_uuid(self.collection, router_id)
