###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from ccp_server.provider import services
from ccp_server.provider.openstack.compute.instance import Instance
from ccp_server.provider.openstack.compute.keypair import KeyPair
from ccp_server.provider.openstack.connection import OpenstackConnection


class Compute(services.Compute):
    connection: OpenstackConnection = OpenstackConnection()

    keypair: KeyPair = KeyPair(connection)

    instance: Instance = Instance(connection)
