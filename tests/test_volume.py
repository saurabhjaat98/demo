###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Aman kadhala <aman@coredge.io>, Mar 2023                         #
###############################################################################
import os
import unittest
from unittest.mock import patch

from ccp_server.api.v1.volume import VolumeService
from tests.test_base import TestBase


class TestVolume(TestBase):
    @patch('ccp_server.api.v1.volume.VolumeService.create_volume')
    def test_create_volume(self, volume_mock):
        """Test the call flow for VolumeService.create_volume()."""

        # Given
        volume_mock.return_value.ok = True

        # When
        response = VolumeService.create_volume()

        # Then
        assert response is not None
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.create_volume')
    def test_create_volume_response(self, volume_mock):
        """Test the response for VolumeService.create_volume()."""

        # Given
        volume_response = {
            "id": self.generate_uuid4()
        }
        volume_mock.return_value.ok = True
        volume_mock.return_value.json.return_value = volume_response

        # When
        response = VolumeService.create_volume()

        # Then
        self.assertDictEqual(volume_response, response.json())
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.list_volumes_by_project_id')
    def test_list_volumes_by_project_id(self, volume_mock):
        """Test the call flow for VolumeService.list_volumes_by_project_id()."""

        # Given
        volume_mock.return_value.ok = True

        # When
        response = VolumeService.list_volumes_by_project_id()

        # Then
        assert response is not None
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.list_volumes_by_project_id')
    def test_list_volumes_by_project_id_response(self, volume_mock):
        """Test the response for VolumeService.list_volumes_by_project_id()."""

        # Given
        volumes = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_volume.json'))
        volume_mock.return_value.ok = True
        volume_mock.return_value.json.return_value = volumes

        # When
        response = VolumeService.list_volumes_by_project_id()

        # Then
        self.assertListEqual(volumes, response.json())
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.list_all_volumes')
    def test_list_all_volumes(self, volume_mock):
        """Test the call flow for VolumeService.list_all_volumes()."""

        # Given
        volume_mock.return_value.ok = True

        # When
        response = VolumeService.list_all_volumes()

        # Then
        assert response is not None
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.list_all_volumes')
    def test_list_all_volumes_response(self, volume_mock):
        """Test the response for VolumeService.list_all_volumes()."""

        # Given
        volumes = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_volume.json'))
        volume_mock.return_value.ok = True
        volume_mock.return_value.json.return_value = volumes

        # When
        response = VolumeService.list_all_volumes()

        # Then
        self.assertListEqual(volumes, response.json())
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.get_volume')
    def test_get_volume(self, volume_mock):
        """Test the call flow for VolumeService.get_volume()."""

        # Given
        volume_mock.return_value.ok = True

        # When
        response = VolumeService.get_volume(self.generate_uuid4())

        # Then
        assert response is not None
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.get_volume')
    def test_get_volume_response(self, volume_mock):
        """Test the volume response for VolumeService.get_volume()."""

        # Given
        mock_volume_id = self.generate_uuid4()
        volume_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_volume.json'))
        volume_keys = ["name", "id", "description", "status",
                       "size", "availability_zone", "cloud_meta"]
        volume_mock.return_value.ok = True
        volume_mock.return_value.json.return_value = volume_response

        # When
        response = VolumeService.get_volume(mock_volume_id)

        # Then
        self.assertListEqual(volume_keys, list(response.json().keys()))
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.delete_volume')
    def test_delete_volume(self, volume_mock):
        """ Test the call flow for VolumeService.delete_volume()."""

        # Given
        volume_mock.return_value.no_content = True

        # When
        response = VolumeService.delete_volume(self.generate_uuid4())

        # Then
        assert response is not None
        volume_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume.VolumeService.update_volume')
    def test_volume_update(self, volume_mock):
        """Test the call flow for VolumeService.update_volume()."""

        # Given
        mock_volume_id = self.generate_uuid4()
        volume_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'update_volume.json'))
        volume_keys = ["name", "description"]
        volume_mock.return_value.ok = True
        volume_mock.return_value.json.return_value = volume_response

        # When
        response = VolumeService.update_volume(
            mock_volume_id, name="new_volume_name", description="new_description")

        # Then
        self.assertListEqual(volume_keys, list(response.json().keys()))
        volume_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
