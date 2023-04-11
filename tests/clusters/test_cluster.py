###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Apr 2023    #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.clusters.cluster import ClusterService
from tests.test_base import TestBase


class TestCluster(TestBase):

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.create_cluster')
    def test_create_cluster(self, cluster_mock):
        """Test the call flow for ClusterService.create_cluster()."""

        # Given
        cluster_mock.return_value.ok = True

        # When
        response = ClusterService.create_cluster()

        # Then
        assert response is not None
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.create_cluster')
    def test_create_cluster_response(self, cluster_mock):
        """Test the response for ClusterService.create_cluster()."""

        # Given
        cluster_response = {
            "id": self.generate_uuid4()
        }
        cluster_mock.return_value.ok = True
        cluster_mock.return_value.json.return_value = cluster_response

        # When
        response = ClusterService.create_cluster()

        # Then
        self.assertDictEqual(cluster_response, response.json())
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.delete_cluster')
    def test_delete_cluster(self, cluster_mock):
        """Test the call flow for ClusterService.delete_cluster()."""

        # Given
        cluster_mock.return_value.no_content = True

        # When
        response = ClusterService.delete_cluster(self.generate_uuid4())

        # Then
        assert response is not None
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.get_cluster')
    def test_get_cluster(self, cluster_mock):
        """Test the call flow for ClusterService.get_cluster()."""

        # Given
        cluster_mock.return_value.ok = True

        # When
        response = ClusterService.get_cluster(self.generate_uuid4())

        # Then
        assert response is not None
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.get_cluster')
    def test_get_cluster_response(self, cluster_mock):
        """Test the cluster response for ClusterService.get_cluster()."""

        # Given
        mock_cluster_id = self.generate_uuid4()
        cluster_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_cluster.json'))
        cluster_keys = ["uuid", 'created_by', "name", 'cloud', 'org_id', 'project_id', 'reference_id', 'active',
                        'cluster_template_id', 'master_count', 'master_flavor_id', 'node_count', 'flavor_id',
                        'cloud_meta']

        cluster_mock.return_value.ok = True
        cluster_mock.return_value.json.return_value = cluster_response

        # When
        response = ClusterService.get_cluster(
            mock_cluster_id)

        # Then
        self.assertListEqual(cluster_keys, list(response.json().keys()))
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.list_clusters_by_project')
    def test_list_cluster_by_project(self, cluster_mock):
        """Test the call flow for ClusterService.list_clusters_by_project()."""

        # Given
        cluster_mock.return_value.ok = True

        # When
        response = ClusterService.list_clusters_by_project()

        # Then
        assert response is not None
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.list_clusters_by_project')
    def test_list_clusters_by_project_response(self, cluster_mock):
        """Test the response for ClusterService.list_clusters_by_project()."""

        # Given
        clusters = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_clusters_by_project.json'))

        cluster_mock.return_value.ok = True
        cluster_mock.return_value.json.return_value = clusters

        # When
        response = ClusterService.list_clusters_by_project()

        # Then
        self.assertListEqual(clusters, response.json())
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.list_all_clusters')
    def test_list_all_clusters(self, cluster_mock):
        """Test the call flow for ClusterService.list_all_clusters()."""

        # Given
        cluster_mock.return_value.ok = True

        # When
        response = ClusterService.list_all_clusters()

        # Then
        assert response is not None
        cluster_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster.ClusterService.list_all_clusters')
    def test_list_all_clusters_response(self, cluster_mock):
        """Test the response for ClusterService.list_all_clusters()."""

        # Given
        clusters = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_clusters.json'))

        cluster_mock.return_value.ok = True
        cluster_mock.return_value.json.return_value = clusters

        # When
        response = ClusterService.list_all_clusters()

        # Then
        self.assertListEqual(clusters, response.json())
        cluster_mock.assert_called_once()
