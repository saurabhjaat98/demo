###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Aman kadhala <aman@coredge.io>, Mar 2023                         #
###############################################################################
import os
import unittest
from unittest.mock import patch

from ccp_server.api.v1.user import UserService
from tests.test_base import TestBase


class TestUser(TestBase):

    @patch('ccp_server.api.v1.user.UserService.create_user')
    def test_create_user(self, user_mock):
        """Test the call flow for UserService.create_user()."""

        # Given
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.create_user()

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.create_user')
    def test_create_user_response(self, user_mock):
        """Test the response for UserService.create_user()."""

        # Given
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.create_user()

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user')
    def test_get_user(self, user_mock):
        """Test the call flow for UserService.get_user() from keycloak."""

        # Given
        user_mock.return_value.ok = True

        # When
        response = UserService.get_user("test_user")

        # Then
        assert response is not None
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user')
    def test_get_user_response(self, user_mock):
        """Test the response for UserService.get_user() from keycloak."""

        # Given
        user_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_user.json'))
        user_keys = ["email", "first_name", "last_name", "username", "email_verified", "created_at",
                     "secret_key", "profile_completed", "mobile_number", "access_key", "roles"]
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = user_response

        # When
        response = UserService.get_user("test_user")

        # Then
        self.assertListEqual(user_keys, list(
            response.json().keys()))
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user_from_cloud')
    def test_get_user_from_cloud(self, user_mock):
        """Test the call flow for UserService.get_user_from_cloud()."""

        # Given
        user_mock.return_value.ok = True

        # When
        response = UserService.get_user_from_cloud("test_user")

        # Then
        assert response is not None
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user_from_cloud')
    def test_get_user_from_cloud_response(self, user_mock):
        """Test the call flow for UserService.get_user_from_cloud()."""

        # Given
        user_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_user_cloud.json'))
        user_keys = ["email", "description", "id", "name", "domain_id", "enabled", "default_project_id",
                     "password_expires_at", "links", "location"]
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = user_response

        # When
        response = UserService.get_user_from_cloud("test_user")

        # Then
        self.assertListEqual(user_keys, list(
            response.json().keys()))
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.update_user')
    def test_update_user(self, user_mock):
        """Test the call flow for UserService.update_user() in keycloak."""

        # Given
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.update_user("test_user")

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.delete_user')
    def test_delete_user(self, user_mock):
        """Test the call flow for UserService.delete_user()."""

        # Given
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.delete_user("test_user")

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.grant_roles')
    def test_grant_roles(self, user_mock):
        """ Test the call flow for UserService.grant_roles() """

        # Given
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.grant_roles("test_role", ['test_user_role'])

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.revoke_roles')
    def test_revoke_roles(self, user_mock):
        """ Test the call flow for UserService.revoke_roles() """

        # Given
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.revoke_roles("test_revoke", ['test_user_role'])

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_users')
    def test_get_users(self, user_mock):
        """Test the call flow for UserService.get_users() list of users from Keycloak."""

        # Given
        user_mock.return_value.ok = True

        # When
        response = UserService.get_users()

        # Then
        assert response is not None
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_users')
    def test_get_users_response(self, user_mock):
        """Test the response for UserService.get_user() list of users from Keycloak"""

        # Given
        user_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_users.json'))
        user_keys = ["email", "first_name", "last_name", "username", "email_verified", "created_at",
                     "secret_key", "mobile_number", "profile_completed", "access_key"]
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = user_response

        # When
        response = UserService.get_users()

        # Then
        self.assertListEqual(user_keys, list(
            response.json().keys()))
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.update_email_action')
    def test_update_email_action(self, user_mock):
        """Test the call flow for UserService.update_email_action()."""

        # Given
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.update_email_action(
            "test_user", ["test_action"])

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user_orgs')
    def test_get_user_orgs(self, user_mock):
        """ Test the call flow for UserService.get_user_orgs() list of groups from Keycloak."""

        # Given
        user_mock.return_value.ok = True

        # When
        response = UserService.get_user_orgs("test_user")

        # Then
        assert response is not None
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user_orgs')
    def test_get_user_orgs_response(self, user_mock):
        """" Test the response for UserService.get_user_orgs() list of groups from Keycloak"""

        # Given
        user_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_user_orgs.json'))
        user_keys = ["uuid", "name", "description", "cloud", "external_id", "default_cloud",
                     "tan_number", "gst_number", "cloud_meta"]
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = user_response

        # When
        response = UserService.get_user_orgs('test_user_orgs')

        # Then
        self.assertListEqual(user_keys, list(
            response.json().keys()))
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user_projects')
    def test_get_user_projects(self, user_mock):
        """Test the call flow for UserService.get_user_projects()."""

        # Given
        user_mock.return_value.ok = True

        # When
        response = UserService.get_user_projects("test_user")

        # Then
        assert response is not None
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_user_projects')
    def test_get_user_projects_response(self, user_mock):
        """Test the response for UserService.get_user_projects()."""

        # Given
        user_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_user_projects.json'))
        user_keys = ["uuid", "name", "description", "cloud", "org_id", "active", "created_at", "created_by",
                     "updated_at", "enable", "external_id", "default"]
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = user_response

        # When
        response = UserService.get_user_projects("test_user")

        # Then
        self.assertListEqual(user_keys, list(
            response.json().keys()))
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_logged_in_user_projects')
    def test_get_logged_in_user_projects(self, user_mock):
        """ Test the call flow for UserService.get_logged_in_user_projects(). """

        # Given
        user_mock.return_value.ok = True

        # When
        response = UserService.get_logged_in_user_projects()

        # Then
        assert response is not None
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.get_logged_in_user_projects')
    def test_get_logged_in_user_projects_response(self, user_mock):
        """" Test the response for UserService.get_logged_in_user_projects()"""

        # Given
        user_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_logged_in_user_projects.json'))
        user_keys = ["uuid", "name", "description", "cloud", "org_id", "created_at", "created_by",
                     "updated_at", "active", "enable", "external_id"]
        user_mock.return_value.ok = True
        user_mock.return_value.json.return_value = user_response

        # When
        response = UserService.get_logged_in_user_projects()

        # Then
        self.assertListEqual(user_keys, list(
            response.json().keys()))
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.generate_access_token')
    def test_generate_access_token(self, user_mock):
        """Test the call flow for UserService.generate_access_token()."""

        # Given
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.generate_access_token("test_token")

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()

    @patch('ccp_server.api.v1.user.UserService.logout')
    def test_logout(self, user_mock):
        """Test the call flow for UserService.logout()."""

        # Given
        user_mock.return_value.json.return_value = None

        # When
        response = UserService.logout()

        # Then
        self.assertIsNone(response.json())
        user_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
