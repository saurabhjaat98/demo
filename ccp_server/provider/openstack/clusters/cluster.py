###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Apr 2023    #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class Cluster(services.Cluster):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.CLUSTER

    @log
    async def create_cluster(self, project_id: str, cluster: models.Cluster):
        try:
            cloud_response = self.conn.connect().create_coe_cluster(
                **cluster.dict(exclude_unset=True))
            return await mapper(data=cloud_response, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Cluster'), e.status_code, e.details)

    @log
    async def list_all_clusters(self):
        cloud_response = self.conn.connect().list_coe_clusters()
        return await mapper(data=cloud_response, resource_name=self.collection)

    @log
    async def delete_cluster(self, cluster_id: str):
        try:
            if not self.conn.connect().delete_coe_cluster(cluster_id):
                raise CCPOpenStackException("Failed To Delete Cluster")
        except Exception as e:
            raise CCPOpenStackException(f' {e.details or e.message}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
