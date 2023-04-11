###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.networks.network import NetworkService
from tests.test_base import KC_MOCK
from tests.test_base import TestBase


class TestNetwork(TestBase):

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.network.NetworkService.list_networks_by_project_id')
    def test_list_networks_by_project_id(self, network_mock, kc_mock):
        """Test the call flow for NetworkService.list_networks_by_project_id()."""

        # Given
        network_mock.return_value.ok = True

        # When
        response = NetworkService.list_networks_by_project_id()

        # Then
        assert response is not None
        network_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.network.NetworkService.list_networks_by_project_id')
    def test_list_networks_by_project_id_response(self, network_mock, kc_mock):
        """Test the response for NetworkService.list_networks_by_project_id()."""

        # Given
        networks = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_networks_by_project_id.json'))

        network_mock.return_value.ok = True
        network_mock.return_value.json.return_value = networks

        # When
        response = NetworkService.list_networks_by_project_id()

        # Then
        self.assertListEqual(networks, response.json())
        network_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.network.NetworkService.get_network')
    def test_get_network(self, network_mock, kc_mock):
        """Test the call flow for get_network()."""

        # Given
        network_mock.return_value.ok = True

        # When
        response = NetworkService.get_network(self.generate_uuid4())

        # Then
        assert response is not None
        network_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.network.NetworkService.get_network')
    def test_get_network_response(self, network_mock, kc_mock):
        """Test the network response for NetworkService.get_network()."""

        # Given
        mock_network_id = self.generate_uuid4()
        network_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_network.json'))
        network_keys = ["uuid", "name", "cloud", "reference_id", "created_by", "created_at", "created_at_str",
                        "cloud_meta", "active", "admin_state_up", "shared"]

        network_mock.return_value.ok = True
        network_mock.return_value.json.return_value = network_response

        # When
        response = NetworkService.get_network(mock_network_id)

        # Then
        self.assertListEqual(network_keys, list(response.json().keys()))
        network_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.network.NetworkService.delete_network')
    def test_delete_network(self, network_mock, kc_mock):
        """Test the call flow for NetworkService.delete_network()."""

        # Given
        network_mock.return_value.no_content = True

        # When
        response = NetworkService.delete_network(self.generate_uuid4())

        # Then
        assert response is not None
        network_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.network.NetworkService.create_network')
    def test_create_network(self, network_mock, kc_mock):
        """Test the call flow for NetworkService.create_network()."""

        # Given
        network_mock.return_value.ok = True

        # when
        response = NetworkService.create_network()

        # Then
        assert response is not None
        network_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.network.NetworkService.create_network')
    def test_create_network_response(self, network_mock, kc_mock):
        """Test the response for NetworkService.create_network()."""

        # Given
        network_response = {
            "id": self.generate_uuid4()
        }
        network_mock.return_value.ok = True
        network_mock.return_value.json.return_value = network_response

        # When
        response = NetworkService.create_network()

        # Then
        self.assertDictEqual(network_response, response.json())
        network_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.network.NetworkService.list_all_networks')
    def test_list_all_networks(self, network_mock):
        """Test the call flow for NetworkService.list_all_networks()."""

        # Given
        network_mock.return_value.ok = True

        # When
        response = NetworkService.list_all_networks()

        # Then
        assert response is not None
        network_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.network.NetworkService.list_all_networks')
    def test_list_all_network_response(self, network_mock):
        """Test the response for NetworkService.list_all_networks()."""

        # Given
        networks = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_networks.json'))

        network_mock.return_value.ok = True
        network_mock.return_value.json.return_value = networks

        # When
        response = NetworkService.list_all_networks()

        # Then
        self.assertListEqual(networks, response.json())
        network_mock.assert_called_once()
