###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Aman kadhala <aman@coredge.io>, Mar 2023                         #
###############################################################################
import os
import unittest
from unittest.mock import patch

from ccp_server.api.v1.admin.flavor import FlavorService
from tests.test_base import TestBase


class TestFlavor(TestBase):

    @patch('ccp_server.api.v1.admin.flavor.FlavorService.list_flavors')
    def test_list_flavor(self, flavor_mock):
        """Test the call flow for FlavorService.list_flavor()."""

        # Given
        flavor_mock.return_value.ok = True

        # When
        response = FlavorService.list_flavors()

        # Then
        assert response is not None
        flavor_mock.assert_called_once()

    @patch('ccp_server.api.v1.admin.flavor.FlavorService.list_flavors')
    def test_list_flavor_response(self, flavor_mock):
        """Test the response for FlavorService.list_flavor()."""

        # Given
        flavors = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_flavor.json'))
        flavor_mock.return_value.ok = True
        flavor_mock.return_value.json.return_value = flavors

        # When
        response = FlavorService.list_flavors()

        # Then
        self.assertListEqual(flavors, response.json())
        flavor_mock.assert_called_once()

    @patch('ccp_server.api.v1.admin.flavor.FlavorService.get_flavor')
    def test_get_flavor(self, flavor_mock):
        """Test the call flow for FlavorService.get_flavor()."""

        # Given
        flavor_mock.return_value.ok = True

        # When
        response = FlavorService.get_flavor(self.generate_uuid4())

        # Then
        assert response is not None
        flavor_mock.assert_called_once()

    @patch('ccp_server.api.v1.admin.flavor.FlavorService.get_flavor')
    def test_get_flavor_response(self, flavor_mock):
        """Test the flavor response for FlavorService.get_flavor()."""

        # Given
        mock_flavor_id = self.generate_uuid4()
        flavor_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_flavor.json'))
        flavor_keys = ["uuid", "name", "description", "cloud", "reference_id", "created_by", "created_at", "cloud_meta",
                       "active", "vcpus", "ram", "disk", "ephemeral", "swap", "rxtx_factor"]
        flavor_mock.return_value.ok = True
        flavor_mock.return_value.json.return_value = flavor_response

        # When
        response = FlavorService.get_flavor(mock_flavor_id)

        # Then
        self.assertListEqual(flavor_keys, list(
            response.json().keys()))
        flavor_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
