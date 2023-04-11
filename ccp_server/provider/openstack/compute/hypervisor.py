###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
###############################################################################
from ccp_server.provider import services
from ccp_server.util.logger import log


class Hypervisor(services.Hypervisor):

    def __init__(self, connection: services.Connection):
        self.conn = connection

    @log
    async def list_hypervisors(self) -> list:
        """This method is used to fetch the list all hypervisors
                :return: list of hypervisors
        """
        return self.conn.connect().list_hypervisors()
