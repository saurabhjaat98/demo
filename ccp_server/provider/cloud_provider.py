###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from abc import ABC

from ccp_server.provider.services import Aggregate
from ccp_server.provider.services import Bucket
from ccp_server.provider.services import CloudUtils
from ccp_server.provider.services import Cluster
from ccp_server.provider.services import ClusterTemplate
from ccp_server.provider.services import Compute
from ccp_server.provider.services import Connection
from ccp_server.provider.services import Flavor
from ccp_server.provider.services import FloatingIP
from ccp_server.provider.services import Hypervisor
from ccp_server.provider.services import Image
from ccp_server.provider.services import Keypair
from ccp_server.provider.services import Network
from ccp_server.provider.services import Port
from ccp_server.provider.services import Project
from ccp_server.provider.services import Router
from ccp_server.provider.services import SecurityGroup
from ccp_server.provider.services import SecurityGroupRule
from ccp_server.provider.services import StorageUser
from ccp_server.provider.services import Subnet
from ccp_server.provider.services import User
from ccp_server.provider.services import Volume
from ccp_server.provider.services import VolumeSnapshot


class CloudProvider(ABC):
    connection: Connection

    project: Project

    user: User

    compute: Compute

    flavor: Flavor

    cloud_utils: CloudUtils

    network: Network

    subnet: Subnet

    image: Image

    aggregate: Aggregate

    hypervisor: Hypervisor

    security_group: SecurityGroup

    floating_ip: FloatingIP

    port: Port

    bucket: Bucket

    security_group_rule: SecurityGroupRule

    router: Router

    volume: Volume

    volume_snapshot: VolumeSnapshot

    keypair: Keypair

    storageuser: StorageUser

    cluster: Cluster

    cluster_template: ClusterTemplate
