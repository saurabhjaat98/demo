###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.networks.floating_ip import FloatingIPService
from tests.test_base import KC_MOCK
from tests.test_base import TestBase


class TestFloatingIP(TestBase):

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.list_floating_ips')
    def test_list_floating_ips(self, floating_ip_mock, kc_mock):
        """Test the call flow for FloatingIPService.list_floating_ips()."""

        # Given
        floating_ip_mock.return_value.ok = True

        # When
        response = FloatingIPService.list_floating_ips()

        # Then
        assert response is not None
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.list_floating_ips')
    def test_list_floating_ips_response(self, floating_ip_mock, kc_mock):
        """Test the response for FloatingIPService.list_floating_ips()."""

        # Given
        floating_ips = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_floating_ips.json'))

        floating_ip_mock.return_value.ok = True
        floating_ip_mock.return_value.json.return_value = floating_ips

        # When
        response = FloatingIPService.list_floating_ips()

        # Then
        self.assertListEqual(floating_ips, response.json())
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.list_all_floating_ips')
    def test_list_all_floating_ips(self, floating_ip_mock, kc_mock):
        """Test the call flow for FloatingIPService.list_all_floating_ips()."""

        # Given
        floating_ip_mock.return_value.ok = True

        # When
        response = FloatingIPService.list_all_floating_ips()

        # Then
        assert response is not None
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.list_all_floating_ips')
    def test_list_all_floating_ips_response(self, floating_ip_mock, kc_mock):
        """Test the response for FloatingIPService.list_all_floating_ips()."""

        # Given
        floating_ips = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_floating_ips.json'))

        floating_ip_mock.return_value.ok = True
        floating_ip_mock.return_value.json.return_value = floating_ips

        # When
        response = FloatingIPService.list_all_floating_ips()

        # Then
        self.assertListEqual(floating_ips, response.json())
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.get_floating_ip')
    def test_get_floating_ip(self, floating_ip_mock, kc_mock):
        """Test the call flow for FloatingIPService.get_floating_ip()."""

        # Given
        floating_ip_mock.return_value.ok = True

        # When
        response = FloatingIPService.get_floating_ip(self.generate_uuid4())

        # Then
        assert response is not None
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.get_floating_ip')
    def test_get_floating_ip_response(self, floating_ip_mock, kc_mock):
        """Test the floating IP response for get_floating_ip()."""

        # Given
        mock_floating_ip_id = self.generate_uuid4()
        floating_ip_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_floating_ip.json'))
        floating_ip_keys = ["uuid", "cloud", "reference_id", "created_by", "created_at", "created_at_str",
                            "cloud_meta", "active", "network_id"]

        floating_ip_mock.return_value.ok = True
        floating_ip_mock.return_value.json.return_value = floating_ip_response

        # When
        response = FloatingIPService.get_floating_ip(mock_floating_ip_id)

        # Then
        self.assertListEqual(floating_ip_keys, list(response.json().keys()))
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.delete_floating_ip')
    def test_delete_floating_ip(self, floating_ip_mock, kc_mock):
        """Test the call flow for FloatingIPService.delete_floating_ip()."""

        # Given
        floating_ip_mock.return_value.no_content = True

        # When
        response = FloatingIPService.delete_floating_ip(self.generate_uuid4())

        # Then
        assert response is not None
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.create_floating_ip')
    def test_create_floating_ip(self, floating_ip_mock, kc_mock):
        """Test the call flow for FloatingIPService.create_floating_ip()."""

        # Given
        floating_ip_mock.return_value.ok = True

        # When
        response = FloatingIPService.create_floating_ip()

        # Then
        assert response is not None
        floating_ip_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.networks.floating_ip.FloatingIPService.create_floating_ip')
    def test_create_floating_ip_response(self, floating_ip_mock, kc_mock):
        """Test the response for FloatingIPService.create_floating_ip()."""

        # Given
        floating_ip_response = {
            "id": self.generate_uuid4()
        }
        floating_ip_mock.return_value.ok = True
        floating_ip_mock.return_value.json.return_value = floating_ip_response

        # When
        response = FloatingIPService.create_floating_ip()

        # Then
        self.assertDictEqual(floating_ip_response, response.json())
        floating_ip_mock.assert_called_once()
