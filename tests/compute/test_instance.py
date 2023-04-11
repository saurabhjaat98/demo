###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Mar 2023    #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.compute.instance import InstanceService
from tests.test_base import KC_MOCK
from tests.test_base import TestBase


class TestInstance(TestBase):

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.list_all_instances')
    def test_list_all_instances(self, instance_mock, kc_mock):
        """Test the call flow for InstanceService.list_all_instances()."""

        # Given
        instance_mock.return_value.ok = True

        # When
        response = InstanceService.list_all_instances()

        # Then
        assert response is not None
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.list_all_instances')
    def test_list_all_instances_response(self, instance_mock, kc_mock):
        """Test the response for InstanceService.list_all_instances()."""

        # Given
        instances = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_instances.json'))

        instance_mock.return_value.ok = True
        instance_mock.return_value.json.return_value = instances

        # When
        response = InstanceService.list_all_instances()
        # Then
        self.assertListEqual(instances, response.json())
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.list_instances_by_project_id')
    def test_list_instances_by_project_id(self, instance_mock, kc_mock):
        """Test the call flow for InstanceService.list_instances_by_project_id()."""

        # Given
        instance_mock.return_value.ok = True

        # When
        response = InstanceService.list_instances_by_project_id()

        # Then
        assert response is not None
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.list_instances_by_project_id')
    def test_list_instances_response(self, instance_mock, kc_mock):
        """Test the response for InstanceService.list_instances_by_project_id()."""

        # Given
        instances = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_instances_by_project_id.json'))

        instance_mock.return_value.ok = True
        instance_mock.return_value.json.return_value = instances

        # When
        response = InstanceService.list_instances_by_project_id()
        # Then
        self.assertListEqual(instances, response.json())
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.delete_instance')
    def test_delete_instance(self, instance_mock, kc_mock):
        """Test the call flow for InstanceService.delete_instance()."""

        # Given
        instance_mock.return_value.no_content = True

        # When
        response = InstanceService.delete_instance(self.generate_uuid4())

        # Then
        assert response is not None
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.create_instance')
    def test_create_instance(self, instance_mock, kc_mock):
        """Test the call flow for InstanceService.create_instance()."""
        self.skipTest("Instance creation response failed to store in database")

        # Given
        instance_mock.return_value.ok = True

        # When
        response = InstanceService.create_instance()

        # Then
        assert response is not None
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.create_instance')
    def test_create_instance_response(self, instance_mock, kc_mock):
        """Test the response for InstanceService.create_instance()."""
        self.skipTest("Instance creation response failed to store in database")

        # Given
        instance_response = {
            "id": self.generate_uuid4()
        }
        instance_mock.return_value.ok = True
        instance_mock.return_value.json.return_value = instance_response

        # When
        response = InstanceService.create_instance()

        # Then
        self.assertDictEqual(instance_response, response.json())
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.update_instance')
    def test_update_instance(self, instance_mock, kc_mock):
        """Test the call flow for InstanceService.update_instance()."""
        self.skipTest("Instance response failed to store in database")

        # Given
        instance_mock.return_value.ok = True

        # When
        response = InstanceService.update_instance()

        # Then
        assert response is not None
        instance_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.compute.instance.InstanceService.update_instance')
    def test_update_instance_response(self, instance_mock, kc_mock):
        """Test the response for InstanceService.update_instance()."""
        self.skipTest("Instance response failed to store in database")

        # Given
        instance_mock.return_value.no_content = True
        instance_mock.return_value.json.return_value = None

        # When
        response = InstanceService.update_instance(instance_id=self.generate_uuid4(), name='new_instance_name',
                                                   description='test')

        # Then
        assert response.json() is None
        instance_mock.assert_called_once()
