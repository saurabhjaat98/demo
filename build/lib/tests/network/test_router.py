###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Saurabh Choudhary <saurabhchoudhary@coredge.io>, march 2023      #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.networks.router import RouterService
from tests.test_base import TestBase


class TestRouter(TestBase):
    @patch('ccp_server.api.v1.networks.router.RouterService.create_router')
    def test_create_router(self, router_mock):
        """Test the call flow for RouterService.create_router()."""

        # Given
        router_mock.return_value.ok = True

        # When
        response = RouterService.create_router()

        # Then
        assert response is not None
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.create_router')
    def test_create_router_response(self, router_mock):
        """Test the response for RouterService.create_router()."""

        # Given
        router_response = {
            "id": self.generate_uuid4()
        }
        router_mock.return_value.ok = True
        router_mock.return_value.json.return_value = router_response

        # When
        response = RouterService.create_router()

        # Then
        self.assertDictEqual(router_response, response.json())
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.delete_router')
    def test_delete_router(self, router_mock):
        """Test the call flow for RouterService.delete_router()."""

        # Given
        router_mock.return_value.no_content = True

        # When
        response = RouterService.delete_router(self.generate_uuid4())

        # Then
        assert response is not None
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.get_router')
    def test_get_router(self, router_mock):
        """Test the call flow for RouterService.get_router()."""

        # Given
        router_mock.return_value.ok = True

        # When
        response = RouterService.get_router(self.generate_uuid4())

        # Then
        assert response is not None
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.get_router')
    def test_get_router_response(self, router_mock):
        """Test the subnet response for RouterService.get_router()."""

        # Given
        mock_router_id = self.generate_uuid4()
        subnet_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_router.json'))
        router_keys = ["uuid", "name", 'admin_state_up', 'status', 'created_at', 'updated_at', 'external_gateway_info',
                       'description', 'availability_zones', 'cloud_meta']

        router_mock.return_value.ok = True
        router_mock.return_value.json.return_value = subnet_response

        # When
        response = RouterService.get_router(mock_router_id)

        # Then
        self.assertListEqual(router_keys, list(response.json().keys()))
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.list_routers_by_project_id')
    def test_list_router(self, router_mock):
        """Test the call flow for RouterService.list_routers_by_project_id()."""

        # Given
        router_mock.return_value.ok = True

        # When
        response = RouterService.list_routers_by_project_id()

        # Then
        assert response is not None
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.list_routers_by_project_id')
    def test_list_routers_by_project_id_response(self, router_mock):
        """Test the response for RouterService.list_routers_by_project_id()."""

        # Given
        routers = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_routers_by_project_id.json'))

        router_mock.return_value.ok = True
        router_mock.return_value.json.return_value = routers

        # When
        response = RouterService.list_routers_by_project_id()

        # Then
        self.assertListEqual(routers, response.json())
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.list_all_routers')
    def test_list_all_router(self, router_mock):
        """Test the call flow for RouterService.list_all_routers()."""

        # Given
        router_mock.return_value.ok = True

        # When
        response = RouterService.list_all_routers()

        # Then
        assert response is not None
        router_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.router.RouterService.list_all_routers')
    def test_list_all_routers_response(self, router_mock):
        """Test the response for RouterService.list_all_routers()."""

        # Given
        routers = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_routers.json'))

        router_mock.return_value.ok = True
        router_mock.return_value.json.return_value = routers

        # When
        response = RouterService.list_all_routers()

        # Then
        self.assertListEqual(routers, response.json())
        router_mock.assert_called_once()
