###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
###############################################################################
import json
import unittest
import uuid

from ccp_server.util.logger import KGLogger

log = KGLogger(__name__)
KC_MOCK = 'ccp_server.kc.connection.KeycloakAdminClient.connect'


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @staticmethod
    def generate_uuid4() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def read_json(file_path: str) -> dict:
        with open(file_path) as file:
            try:
                return json.load(file)
            except Exception as exc:
                raise Exception(exc)
