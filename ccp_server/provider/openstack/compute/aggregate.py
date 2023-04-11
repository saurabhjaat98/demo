###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
###############################################################################
from ccp_server.provider import services
from ccp_server.util.logger import log


class Aggregate(services.Aggregate):

    def __init__(self, connection: services.Connection):
        self.conn = connection

    @log
    async def list_aggregates(self) -> list:
        """This method is used to fetch the list all aggregates
        :return: list of aggregates
        """
        return self.conn.connect().list_aggregates()

    @log
    async def get_aggregate(self, name_or_id):
        """
        This method is used to fetch the data of aggregate from Openstack
        :param name_or_id: name or id of the aggregate
        :param filters: filters
        :return: aggregate data
        """
        return self.conn.connect().get_aggregate(name_or_id)
