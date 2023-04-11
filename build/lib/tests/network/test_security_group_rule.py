###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Saurabh Choudhary <saurabhchoudhary@coredge.io>, march 2023      #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.networks.security_group_rule import SecurityGroupRuleService
from tests.test_base import TestBase


class TestSecurityGroupRule(TestBase):
    @patch('ccp_server.api.v1.networks.security_group_rule.SecurityGroupRuleService.create_security_group_rule')
    def test_create_security_group_rule(self, security_group_rule_mock):
        """Test the call flow for SecurityGroupRuleService.create_security_group_rule()."""

        # Given
        security_group_rule_mock.return_value.ok = True

        # When
        response = SecurityGroupRuleService.create_security_group_rule()

        # Then
        assert response is not None
        security_group_rule_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group_rule.SecurityGroupRuleService.create_security_group_rule')
    def test_create_security_group_rule_response(self, security_group_rule_mock):
        """Test the response for SecurityGroupRuleService.create_security_group_rule()."""

        # Given
        security_group_rule_response = {
            "id": self.generate_uuid4()
        }
        security_group_rule_mock.return_value.ok = True
        security_group_rule_mock.return_value.json.return_value = security_group_rule_response

        # When
        response = SecurityGroupRuleService.create_security_group_rule()

        # Then
        self.assertDictEqual(security_group_rule_response, response.json())
        security_group_rule_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group_rule.SecurityGroupRuleService.delete_security_group_rule')
    def test_delete_security_group_rule(self, security_group_rule_mock):
        """Test the call flow for SecurityGroupRuleService.delete_security_group_rule()."""

        # Given
        security_group_rule_mock.return_value.no_content = True

        # When
        response = SecurityGroupRuleService.delete_security_group_rule(
            self.generate_uuid4())

        # Then
        assert response is not None
        security_group_rule_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group_rule.SecurityGroupRuleService.get_security_group_rule')
    def test_get_security_group_rule(self, security_group_rule_mock):
        """Test the call flow for SecurityGroupRuleService.get_security_group_rule()."""

        # Given
        security_group_rule_mock.return_value.ok = True

        # When
        response = SecurityGroupRuleService.get_security_group_rule(
            self.generate_uuid4())

        # Then
        assert response is not None
        security_group_rule_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group_rule.SecurityGroupRuleService.get_security_group_rule')
    def test_get_security_group_rule_response(self, security_group_rule_mock):
        """Test the security_group_rule response for SecurityGroupRuleService.get_security_group_rule()."""

        # Given
        mock_security_group_rule_id = self.generate_uuid4()
        security_group_rule_response = self.read_json(os.path.join(os.path.dirname(__file__), 'data',
                                                                   'get_security_group_rule.json'))

        security_group_rule_keys = ['uuid', 'tenant_id', 'security_group_id', 'project_id',
                                    'created_at', 'updated_at', 'ethertype', 'direction', 'cloud_meta']

        security_group_rule_mock.return_value.ok = True
        security_group_rule_mock.return_value.json.return_value = security_group_rule_response

        # When
        response = SecurityGroupRuleService.get_security_group_rule(
            mock_security_group_rule_id)

        # Then
        self.assertListEqual(security_group_rule_keys,
                             list(response.json().keys()))
        security_group_rule_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group_rule.SecurityGroupRuleService.list_security_group_rules')
    def test_list_security_group_rules(self, security_group_rule_mock):
        """Test the call flow for SecurityGroupRuleService.list_security_group_rules()."""

        # Given
        security_group_rule_mock.return_value.ok = True

        # When
        response = SecurityGroupRuleService.list_security_group_rules()

        # Then
        assert response is not None
        security_group_rule_mock.assert_called_once()

    @patch('ccp_server.api.v1.networks.security_group_rule.SecurityGroupRuleService.list_security_group_rules')
    def test_list_security_group_rules_response(self, security_group_rule_mock):
        """Test the response for SecurityGroupRuleService.list_security_group_rules()."""

        # Given
        security_group_rules = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_security_group_rules.json'))

        security_group_rule_mock.return_value.ok = True
        security_group_rule_mock.return_value.json.return_value = security_group_rules

        # When
        response = SecurityGroupRuleService.list_security_group_rules()

        # Then
        self.assertListEqual(security_group_rules, response.json())
        security_group_rule_mock.assert_called_once()
