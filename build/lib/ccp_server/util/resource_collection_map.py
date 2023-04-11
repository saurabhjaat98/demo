###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from ccp_server.util.constants import Constants

openstack_map = {'Flavor': [Constants.MongoCollection.FLAVOR, 'get_flavor'],
                 'FloatingIP': ['FloatingIP', 'get_floating_ip'],
                 'Image': ['Image', 'get_image'],
                 'KeyPair': [Constants.MongoCollection.KEYPAIR, 'get_keypair'],
                 'Net': [Constants.MongoCollection.NETWORK, 'get_network'],
                 'Project': [Constants.MongoCollection.PROJECT, 'get_project'],
                 'Router': ['Router', 'get_router'],
                 'Server': [Constants.MongoCollection.INSTANCE, 'get_server'],
                 'SecurityGroup': [Constants.MongoCollection.SECURITY_GROUP, 'get_security_group'],
                 'SecurityGroupRule': ['SecurityGroupRule', 'get_security_group_rule'],
                 'Subnet': [Constants.MongoCollection.SUBNET, 'get_subnet'],
                 'Volume': ['Volume', 'get_volume']
                 }
