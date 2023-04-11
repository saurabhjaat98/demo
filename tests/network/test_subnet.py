###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.networks.subnet import SubnetService
from tests.test_base import KC_MOCK
from tests.test_base import TestBase


class TestSubnet(TestBase):

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.subnet.SubnetService.list_subnets_by_network_id')
    def test_list_subnets_by_network_id(self, subnet_mock, kc_mock):
        """Test the call flow for SubnetService.list_subnets_by_network_id()."""

        # Given
        subnet_mock.return_value.ok = True

        # When
        response = SubnetService.list_subnets_by_network_id()

        # Then
        assert response is not None
        subnet_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.subnet.SubnetService.list_subnets_by_network_id')
    def test_list_subnets_by_network_id_response(self, subnet_mock, kc_mock):
        """Test the response for SubnetService.list_subnets_by_network_id()."""

        # Given
        subnets = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_subnets_by_network_id.json'))

        subnet_mock.return_value.ok = True
        subnet_mock.return_value.json.return_value = subnets

        # When
        response = SubnetService.list_subnets_by_network_id()

        # Then
        self.assertListEqual(subnets, response.json())
        subnet_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.subnet.SubnetService.get_subnet')
    def test_get_subnet(self, subnet_mock, kc_mock):
        """Test the call flow for SubnetService.get_subnet()."""

        # Given
        subnet_mock.return_value.ok = True

        # When
        response = SubnetService.get_subnet(self.generate_uuid4())

        # Then
        assert response is not None
        subnet_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.subnet.SubnetService.get_subnet')
    def test_get_subnet_response(self, subnet_mock, kc_mock):
        """Test the subnet response for SubnetService.get_subnet()."""

        # Given
        mock_subnet_id = self.generate_uuid4()
        subnet_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_subnet.json'))
        subnet_keys = ["uuid", "name", "cloud", "reference_id", "created_at", "created_at_str",
                       "cloud_meta", "active", "network_id", "cidr", "ip_version", "enable_dhcp", "gateway_ip",
                       "disable_gateway_ip", "allocation_pools", "dns_nameservers", "host_routes"]

        subnet_mock.return_value.ok = True
        subnet_mock.return_value.json.return_value = subnet_response

        # When
        response = SubnetService.get_subnet(mock_subnet_id)

        # Then
        self.assertListEqual(subnet_keys, list(response.json().keys()))
        subnet_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.subnet.SubnetService.delete_subnet')
    def test_delete_subnet(self, subnet_mock, kc_mock):
        """Test the call flow for SubnetService.delete_subnet()."""

        # Given
        subnet_mock.return_value.no_content = True

        # When
        response = SubnetService.delete_subnet(self.generate_uuid4())

        # Then
        assert response is not None
        subnet_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.subnet.SubnetService.create_subnet')
    def test_create_subnet(self, subnet_mock, kc_mock):
        """Test the call flow for SubnetService.create_subnet()."""

        # Given
        subnet_mock.return_value.ok = True

        # When
        response = SubnetService.create_subnet()

        # Then
        assert response is not None
        subnet_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.subnet.SubnetService.create_subnet')
    def test_create_subnet_response(self, subnet_mock, kc_mock):
        """Test the response for SubnetService.create_subnet()."""

        # Given
        subnet_response = {
            "id": self.generate_uuid4()
        }
        subnet_mock.return_value.ok = True
        subnet_mock.return_value.json.return_value = subnet_response

        # When
        response = SubnetService.create_subnet()

        # Then
        self.assertDictEqual(subnet_response, response.json())
        subnet_mock.assert_called_once()
