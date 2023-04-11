###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from ccp_server.provider import services
from ccp_server.util.logger import log


class CloudUtils(services.CloudUtils):
    """
    CloudUtils class to provide common methods for all cloud providers
    """

    def __init__(self, connection: services.Connection):
        self.conn = connection

    @log
    async def list_availability_zones(self):
        """
        List all availability zones of a cloud.
        Returns: List of availability zones
        """
        return self.conn.connect().list_availability_zone_names()
