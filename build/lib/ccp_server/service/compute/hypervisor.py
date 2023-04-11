###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
###############################################################################
from typing import Dict
from typing import List

from ccp_server.service.providers import Provider
from ccp_server.util.logger import log


class HypervisorService(Provider):
    @log
    async def list_hypervisors(self, query_str: str, page: int, size: int, sort_by: List[str], sort_desc: bool
                               ) -> List[Dict]:
        """This method is used to fetch the data of hypervisors from Cloud.
        :return: List of hypervisors.
        """
        return await self.connect.hypervisor.list_hypervisors()
