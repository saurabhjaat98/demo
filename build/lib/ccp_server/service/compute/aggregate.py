###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, Feb 2023       #
###############################################################################
from typing import Dict
from typing import List

from ccp_server.service.providers import Provider
from ccp_server.util.logger import log


class AggregateService(Provider):

    @log
    async def list_aggregates(self, query_str: str, page: int, size: int, sort_by: List[str], sort_desc: bool
                              ) -> List[Dict]:
        """This method is used to fetch the data of aggregates from Cloud.
        :return: List of aggregates.
        """
        return await self.connect.aggregate.list_aggregates()

    @log
    async def get_aggregate(self, name_or_id) -> any:
        """
        This method is used to fetch the data of aggregate from Cloud
        :param name_or_id: name or id of the aggregate
        :param filters: filters
        :return: aggregate data
        """
        return await self.connect.aggregate.get_aggregate(name_or_id)
