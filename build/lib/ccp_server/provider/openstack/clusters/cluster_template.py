###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class ClusterTemplate(services.ClusterTemplate):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.CLUSTER_TEMPLATE

    @log
    async def create_cluster_template(self, project_id: str, cluster_template: models.ClusterTemplate):
        try:
            cloud_response = self.conn.connect().create_cluster_template(
                name=cluster_template.name,
                image_id=cluster_template.image_id,
                keypair_id=cluster_template.keypair_id,
                coe=cluster_template.coe,
                public=cluster_template.public,
                hidden=cluster_template.hidden,
                registry_enabled=cluster_template.registry_enabled,
                tls_disabled=cluster_template.tls_disabled,
                flavor_id=cluster_template.flavor_id,
                master_flavor_id=cluster_template.master_flavor_id,
                volume_driver=cluster_template.volume_driver,
                docker_storage_driver=cluster_template.docker_storage_driver,
                docker_volume_size=cluster_template.docker_volume_size,
                network_driver=cluster_template.network_driver,
                http_proxy=cluster_template.http_proxy,
                https_proxy=cluster_template.https_proxy,
                no_proxy=cluster_template.no_proxy,
                external_network_id=cluster_template.external_network_id,
                fixed_network=cluster_template.fixed_subnet,
                fixed_subnet=cluster_template.fixed_subnet,
                dns_nameserver=cluster_template.dns_nameserver,
                master_lb_enabled=cluster_template.master_lb_enabled,
                floating_ip_enabled=cluster_template.floating_ip_enabled,
                labels=cluster_template.labels
            )
            return await mapper(data=cloud_response, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Cluster template'), e.status_code, e.details)

    @log
    async def list_all_cluster_templates(self):
        cloud_response = self.conn.connect().list_cluster_templates()
        return await mapper(data=cloud_response, resource_name=self.collection)

    @log
    async def delete_cluster_template(self, cluster_template_id: str):
        try:
            if not self.conn.connect().delete_cluster_template(cluster_template_id):
                raise CCPOpenStackException(
                    "Failed To Delete Cluster Template")
        except Exception as e:
            raise CCPOpenStackException(f' {e.details or e.message}',
                                        status_code=e.status_code or e.http_status, detail=e.details)
