###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
###############################################################################
from ccp_server.util import env_variables as env
from tests.test_base import TestBase


class TestEnvVariables(TestBase):

    def test_mongo_environment_variables(self):
        default_username = 'root'
        default_password = 'password'
        default_host = 'localhost'
        default_port = '27017'
        default_url = 'mongodb://root:password@localhost:27017'

        self.assertEqual(default_username, env.MONGO_USERNAME)
        self.assertEqual(default_password, env.MONGO_PASSWORD)
        self.assertEqual(default_host, env.MONGO_HOST)
        self.assertEqual(default_port, env.MONGO_PORT)
        self.assertEqual(default_url, env.MONGO_DB_URL)
