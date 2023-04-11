###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from ccp_server.provider.cloud_provider import CloudProvider
from ccp_server.provider.openstack.cloud_utils import CloudUtils
from ccp_server.provider.openstack.clusters.cluster import Cluster
from ccp_server.provider.openstack.clusters.cluster_template import ClusterTemplate
from ccp_server.provider.openstack.compute import Compute
from ccp_server.provider.openstack.compute.aggregate import Aggregate
from ccp_server.provider.openstack.compute.hypervisor import Hypervisor
from ccp_server.provider.openstack.connection import OpenstackConnection
from ccp_server.provider.openstack.flavor import Flavor
from ccp_server.provider.openstack.image import Image
from ccp_server.provider.openstack.network.floating_ip import FloatingIP
from ccp_server.provider.openstack.network.network import Network
from ccp_server.provider.openstack.network.port import Port
from ccp_server.provider.openstack.network.router import Router
from ccp_server.provider.openstack.network.security_group import SecurityGroup
from ccp_server.provider.openstack.network.security_group_rule import SecurityGroupRule
from ccp_server.provider.openstack.network.subnet import Subnet
from ccp_server.provider.openstack.project import Project
from ccp_server.provider.openstack.storage.bucket import Bucket
from ccp_server.provider.openstack.storage.storageuser import StorageUser
from ccp_server.provider.openstack.user import User
from ccp_server.provider.openstack.volume import Volume
from ccp_server.provider.openstack.volume_snapshot import VolumeSnapshot


class Openstack(CloudProvider):
    connection: OpenstackConnection = OpenstackConnection()

    project: Project = Project(connection)

    user: User = User(connection)

    compute: Compute = Compute()

    flavor: Flavor = Flavor(connection)

    cloud_utils = CloudUtils = CloudUtils(connection)

    network: Network = Network(connection)

    aggregate: Aggregate = Aggregate(connection)

    image: Image = Image(connection)

    hypervisor: Hypervisor = Hypervisor(connection)

    volume: Volume = Volume(connection)

    security_group: SecurityGroup = SecurityGroup(connection)

    subnet: Subnet = Subnet(connection)

    floating_ip: FloatingIP = FloatingIP(connection)

    port: Port = Port(connection)

    bucket: Bucket = Bucket(connection)

    security_group_rule: SecurityGroupRule = SecurityGroupRule(connection)

    router: Router = Router(connection)

    volume_snapshot: VolumeSnapshot = VolumeSnapshot(connection)

    storageuser: StorageUser = StorageUser(connection)

    cluster: Cluster = Cluster(connection)

    cluster_template: ClusterTemplate = ClusterTemplate(connection)
