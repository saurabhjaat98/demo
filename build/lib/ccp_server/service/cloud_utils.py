###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from ccp_server.service.providers import Provider
from ccp_server.util.logger import log


class CloudUtilService(Provider):
    """
    CloudUtilService class to provide common methods for all cloud providers
    """

    @log
    async def list_availability_zones(self):
        """
        List all availability zones of a cloud.
        Returns: List of availability zones
        """

        return await self.connect.cloud_utils.list_availability_zones()
