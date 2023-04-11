###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
# Modified by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List
from typing import Tuple

from pydantic.types import StrictBool

from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log


class FlavorService(Provider):
    """This method is used to create a flavor in cloud and mongo."""

    def __init__(self):
        self.collection = Constants.MongoCollection.FLAVOR

    @log
    async def list_flavors(self, pageable: Pageable = None,
                           use_db: StrictBool = True) -> Tuple[List[Dict], int]:
        """This method is used to fetch the data of flavors from mongo.
        :param pageable: Pageable object.
        :param use_db: If true it will fetch the result from Mongo, else from cloud
        :return: List of flavors.
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection, exclude_org=True,
                pageable=pageable)
        else:
            mapper_response = await self.connect.flavor.list_flavors()
            return mapper_response, len(mapper_response)

    @log
    async def get_flavor(self, flavor_id: str) -> any:
        """This method is used to fetch the data of flavors from mongo by using flavor_id
        :param flavor_id: id of the flavor
        :return: returns the flavor data or None
        """

        return await self.db.get_document_by_ids(self.collection, flavor_id, exclude_org=True)
