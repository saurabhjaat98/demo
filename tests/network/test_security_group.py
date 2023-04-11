###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Saurabh Choudhary <saurabhchoudhary@coredge.io>, march 2023      #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.networks.security_group import SecurityGroupService
from tests.test_base import TestBase


class TestSecurityGroup(TestBase):
    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.create_security_group')
    def test_create_security_group(self, security_group_mock):
        """Test the call flow for SecurityGroupService.create_security_group()."""

        # Given
        security_group_mock.return_value.ok = True

        # When
        response = SecurityGroupService.create_security_group()

        # Then
        assert response is not None
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.create_security_group')
    def test_create_security_group_response(self, security_group_mock):
        """Test the response for SecurityGroupService.create_security_group()."""

        # Given
        security_group_response = {
            "id": self.generate_uuid4()
        }
        security_group_mock.return_value.ok = True
        security_group_mock.return_value.json.return_value = security_group_response

        # When
        response = SecurityGroupService.create_security_group()

        # Then
        self.assertDictEqual(security_group_response, response.json())
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.delete_security_group')
    def test_delete_security_group(self, security_group_mock):
        """Test the call flow for SecurityGroupService.delete_security_group()."""

        # Given
        security_group_mock.return_value.no_content = True

        # When
        response = SecurityGroupService.delete_security_group(
            self.generate_uuid4())

        # Then
        assert response is not None
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.get_security_group')
    def test_get_security_group(self, security_group_mock):
        """Test the call flow for SecurityGroupService.get_security_group()."""

        # Given
        security_group_mock.return_value.ok = True

        # When
        response = SecurityGroupService.get_security_group(
            self.generate_uuid4())

        # Then
        assert response is not None
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.get_security_group')
    def test_get_security_group_response(self, security_group_mock):
        """Test the security_group response for SecurityGroupService.get_security_group()."""

        # Given
        mock_security_group_id = self.generate_uuid4()
        subnet_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_security_group.json'))
        security_group_keys = ['uuid', 'name', 'tenant_id', 'description', 'created_at', 'updated_at', 'project_id',
                               'cloud_meta']

        security_group_mock.return_value.ok = True
        security_group_mock.return_value.json.return_value = subnet_response

        # When
        response = SecurityGroupService.get_security_group(
            mock_security_group_id)

        # Then
        self.assertListEqual(security_group_keys, list(response.json().keys()))
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.list_all_security_groups')
    def test_list_all_security_group(self, security_group_mock):
        """Test the call flow for SecurityGroupService.list_all_security_groups()."""

        # Given
        security_group_mock.return_value.ok = True

        # When
        response = SecurityGroupService.list_all_security_groups()

        # Then
        assert response is not None
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.list_all_security_groups')
    def test_list_all_security_groups_response(self, security_group_mock):
        """Test the response for SecurityGroupService.list_all_security_groups()."""

        # Given
        security_groups = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_security_groups.json'))

        security_group_mock.return_value.ok = True
        security_group_mock.return_value.json.return_value = security_groups

        # When
        response = SecurityGroupService.list_all_security_groups()

        # Then
        self.assertListEqual(security_groups, response.json())
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.list_security_groups_by_project_id')
    def test_list_security_groups_by_project_id(self, security_group_mock):
        """Test the call flow for SecurityGroupService.list_security_groups_by_project_id()."""

        # Given
        security_group_mock.return_value.ok = True

        # When
        response = SecurityGroupService.list_security_groups_by_project_id()

        # Then
        assert response is not None
        security_group_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group.SecurityGroupService.list_security_groups_by_project_id')
    def test_list_security_groups_by_project_id_response(self, security_group_mock):
        """Test the response for SecurityGroupService.list_security_groups_by_project_id()."""

        # Given
        security_groups = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_security_groups_by_project_id.json'))

        security_group_mock.return_value.ok = True
        security_group_mock.return_value.json.return_value = security_groups

        # When
        response = SecurityGroupService.list_security_groups_by_project_id()
        # Then
        self.assertListEqual(security_groups, response.json())
        security_group_mock.assert_called_once()
