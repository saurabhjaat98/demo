###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Aman kadhala <aman@coredge.io>, Mar 2023                         #
###############################################################################
import os
import unittest
from unittest.mock import patch

from ccp_server.api.v1.volume_snapshot import VolumeSnapshotService
from tests.test_base import TestBase


class TestVolumeSnapshot(TestBase):
    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.create_volume_snapshot')
    def test_create_volume_snapshot(self, volume_snapshot_mock):
        """Test the call flow for VolumeSnapshotService.create_volume_snapshot()."""

        # Given
        volume_snapshot_mock.return_value.ok = True

        # When
        response = VolumeSnapshotService.create_volume_snapshot()

        # Then
        assert response is not None
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.create_volume_snapshot')
    def test_create_volume_response(self, volume_snapshot_mock):
        """Test the response for VolumeSnapshotService.create_volume_snapshot()."""

        # Given
        volume_snapshot_response = {
            "id": self.generate_uuid4()
        }
        volume_snapshot_mock.return_value.ok = True
        volume_snapshot_mock.return_value.json.return_value = volume_snapshot_response

        # When
        response = VolumeSnapshotService.create_volume_snapshot()

        # Then
        self.assertDictEqual(volume_snapshot_response, response.json())
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.list_all_volume_snapshots')
    def test_list_all_volume_snapshots(self, volume_snapshot_mock):
        """Test the call flow for VolumeSnapshotService.list_all_volume_snapshots()."""

        # Given
        volume_snapshot_mock.return_value.ok = True

        # When
        response = VolumeSnapshotService.list_all_volume_snapshots()

        # Then
        assert response is not None
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.list_all_volume_snapshots')
    def test_list_all_volume_snapshots_response(self, volume_snapshot_mock):
        """Test the response for VolumeSnapshotService.list_all_volume_snapshots()."""

        # Given
        volumes_snapshot = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_volume_snapshots.json'))
        volume_snapshot_mock.return_value.ok = True
        volume_snapshot_mock.return_value.json.return_value = volumes_snapshot

        # When
        response = VolumeSnapshotService.list_all_volume_snapshots()

        # Then
        self.assertListEqual(volumes_snapshot, response.json())
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.list_volume_snapshots_from_volume')
    def test_list_volume_snapshots_from_volume(self, volume_snapshot_mock):
        """Test the call flow for VolumeSnapshotService.list_volume_snapshots_from_volume()."""

        # Given
        volume_snapshot_mock.return_value.ok = True

        # When
        response = VolumeSnapshotService.list_volume_snapshots_from_volume()

        # Then
        assert response is not None
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.list_volume_snapshots_from_volume')
    def test_list_volume_snapshots_from_volume_response(self, volume_snapshot_mock):
        """Test the response for VolumeSnapshotService.list_volume_snapshots_from_volume()."""

        # Given
        volumes_snapshot = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_volume_snapshots_from_volume.json'))
        volume_snapshot_mock.return_value.ok = True
        volume_snapshot_mock.return_value.json.return_value = volumes_snapshot

        # When
        response = VolumeSnapshotService.list_volume_snapshots_from_volume()

        # Then
        self.assertListEqual(volumes_snapshot, response.json())
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.list_volume_snapshots_from_project')
    def test_list_volume_snapshots_from_project(self, volume_snapshot_mock):
        """Test the call flow for VolumeSnapshotService.list_volume_snapshots_from_project()."""

        # Given
        volume_snapshot_mock.return_value.ok = True

        # When
        response = VolumeSnapshotService.list_volume_snapshots_from_project()

        # Then
        assert response is not None
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.list_volume_snapshots_from_project')
    def test_list_volume_snapshots_from_project_response(self, volume_snapshot_mock):
        """Test the response for VolumeSnapshotService.list_volume_snapshots_from_project()."""

        # Given
        volumes_snapshot = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_volume_snapshots_from_project.json'))
        volume_snapshot_mock.return_value.ok = True
        volume_snapshot_mock.return_value.json.return_value = volumes_snapshot

        # When
        response = VolumeSnapshotService.list_volume_snapshots_from_project()

        # Then
        self.assertListEqual(volumes_snapshot, response.json())
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.get_volume_snapshot')
    def test_get_volume_snapshot(self, volume_snapshot_mock):
        """Test the call flow for VolumeSnapshotService.get_volume_snapshot()."""

        # Given
        volume_snapshot_mock.return_value.ok = True

        # When
        response = VolumeSnapshotService.get_volume_snapshot(
            self.generate_uuid4())

        # Then
        assert response is not None
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.get_volume_snapshot')
    def test_get_volume_snapshot_response(self, volume_snapshot_mock):
        """Test the volume_snapshot response for VolumeSnapshotService.get_volume_snapshot()."""

        # Given
        mock_volume_snapshot_id = self.generate_uuid4()
        volume_snapshot_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_volume_snapshot.json'))
        volume_keys = ["name", "id", "description", "volume_id", "status",
                       "size", "cloud_meta"]
        volume_snapshot_mock.return_value.ok = True
        volume_snapshot_mock.return_value.json.return_value = volume_snapshot_response

        # When
        response = VolumeSnapshotService.get_volume_snapshot(
            mock_volume_snapshot_id)

        # Then
        self.assertListEqual(volume_keys, list(
            response.json().keys()))
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.delete_volume_snapshot')
    def test_delete_volume_snapshot(self, volume_snapshot_mock):
        """ Test the call flow for VolumeSnapshotService.delete_volume_snapshot()."""

        # Given
        volume_snapshot_mock.return_value.no_content = True

        # When
        response = VolumeSnapshotService.delete_volume_snapshot(
            self.generate_uuid4())

        # Then
        assert response is not None
        volume_snapshot_mock.assert_called_once()

    @patch('ccp_server.api.v1.volume_snapshot.VolumeSnapshotService.update_volume_snapshot')
    def test_volume_snapshot_update(self, volume_snapshot_mock):
        """Test the call flow for VolumeSnapshotService.update_volume_snapshot()."""

        # Given
        mock_volume_id = self.generate_uuid4()
        volume_snapshot_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'update_volume_snapshot.json'))
        volume_snapshot_keys = ["name", "description"]
        volume_snapshot_mock.return_value.ok = True
        volume_snapshot_mock.return_value.json.return_value = volume_snapshot_response

        # When
        response = VolumeSnapshotService.update_volume_snapshot(mock_volume_id, name="new_volume_snapshot_name",
                                                                description="new_description")

        # Then
        self.assertListEqual(volume_snapshot_keys, list(
            response.json().keys()))
        volume_snapshot_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
