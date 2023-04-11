###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Saurabh Choudhary <saurabhchoudhary@coredge.io>, march 2023      #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.networks.port import PortService
from tests.test_base import TestBase


class TestPort(TestBase):
    @patch('ccp_server.api.v1.networks.port.PortService.create_port')
    def test_create_port(self, port_mock):
        """Test the call flow for PortService.create_port()."""

        # Given
        port_mock.return_value.ok = True

        # When
        response = PortService.create_port()

        # Then
        assert response is not None
        port_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.port.PortService.create_port')
    def test_create_port_response(self, port_mock):
        """Test the response for SubnetService.create_port()."""

        # Given
        port_response = {
            "id": self.generate_uuid4()
        }
        port_mock.return_value.ok = True
        port_mock.return_value.json.return_value = port_response

        # When
        response = PortService.create_port()

        # Then
        self.assertDictEqual(port_response, response.json())
        port_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.port.PortService.delete_port')
    def test_delete_port(self, port_mock):
        """Test the call flow for PortService.delete_port()."""

        # Given
        port_mock.return_value.no_content = True

        # When
        response = PortService.delete_port(self.generate_uuid4())

        # Then
        assert response is not None
        port_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.port.PortService.get_port')
    def test_get_port(self, port_mock):
        """Test the call flow for PortService.get_port()."""

        # Given
        port_mock.return_value.ok = True

        # When
        response = PortService.get_port(self.generate_uuid4())

        # Then
        assert response is not None
        port_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.port.PortService.get_port')
    def test_get_port_response(self, port_mock):
        """Test the subnet response for PortService.get_port()."""

        # Given
        mock_port_id = self.generate_uuid4()
        subnet_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_port.json'))
        port_keys = ["uuid", "name", "network_id", "admin_state_up", "status",
                     "created_at", "updated_at", "fixed_ips", "mac_address", "project_id", 'cloud_meta']

        port_mock.return_value.ok = True
        port_mock.return_value.json.return_value = subnet_response

        # When
        response = PortService.get_port(mock_port_id)

        # Then
        self.assertListEqual(port_keys, list(response.json().keys()))
        port_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.port.PortService.list_ports_by_network_id')
    def test_list_ports_by_network_id(self, port_mock):
        """Test the call flow for PortService.list_ports_by_network_id()."""

        # Given
        port_mock.return_value.ok = True

        # When
        response = PortService.list_ports_by_network_id()

        # Then
        assert response is not None
        port_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.port.PortService.list_ports_by_network_id')
    def test_list_ports_by_network_id_response(self, port_mock):
        """Test the response for PortService.list_ports_by_network_id()."""

        # Given
        ports = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_ports_by_network_id.json'))

        port_mock.return_value.ok = True
        port_mock.return_value.json.return_value = ports

        # When
        response = PortService.list_ports_by_network_id()

        # Then
        self.assertListEqual(ports, response.json())
        port_mock.assert_called_once()
