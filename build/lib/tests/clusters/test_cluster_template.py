###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Rajkumar Srinivasan <rajkumarsrinivasan@coredge.io>, Apr 2023    #
###############################################################################
import os
from unittest.mock import patch

from ccp_server.api.v1.clusters.cluster_template import ClusterTemplateService
from tests.test_base import TestBase


class TestClusterTemplate(TestBase):

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.create_cluster_template')
    def test_create_cluster_template(self, cluster_template_mock):
        """Test the call flow for ClusterTemplateService.create_cluster_template()."""

        # Given
        cluster_template_mock.return_value.ok = True

        # When
        response = ClusterTemplateService.create_cluster_template()

        # Then
        assert response is not None
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.create_cluster_template')
    def test_create_cluster_template_response(self, cluster_template_mock):
        """Test the response for ClusterTemplateService.create_cluster_template()."""

        # Given
        cluster_template_response = {
            "id": self.generate_uuid4()
        }
        cluster_template_mock.return_value.ok = True
        cluster_template_mock.return_value.json.return_value = cluster_template_response

        # When
        response = ClusterTemplateService.create_cluster_template()

        # Then
        self.assertDictEqual(cluster_template_response, response.json())
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.delete_cluster_template')
    def test_delete_cluster_template(self, cluster_template_mock):
        """Test the call flow for ClusterTemplateService.delete_cluster_template()."""

        # Given
        cluster_template_mock.return_value.no_content = True

        # When
        response = ClusterTemplateService.delete_cluster_template(
            self.generate_uuid4())

        # Then
        assert response is not None
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.get_cluster_template')
    def test_get_cluster_template(self, cluster_template_mock):
        """Test the call flow for ClusterTemplateService.get_cluster_template()."""

        # Given
        cluster_template_mock.return_value.ok = True

        # When
        response = ClusterTemplateService.get_cluster_template(
            self.generate_uuid4())

        # Then
        assert response is not None
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.get_cluster_template')
    def test_get_cluster_template_response(self, cluster_template_mock):
        """Test the cluster template response for ClusterTemplateService.get_cluster_template()."""

        # Given
        mock_cluster_template_id = self.generate_uuid4()
        cluster_template_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_cluster_template.json'))
        cluster_template_keys = ["uuid", 'created_at', 'created_by', "name", 'cloud', 'org_id', 'project_id',
                                 'reference_id', 'active', 'image_id', 'keypair_id', 'coe', 'cloud_meta', 'public',
                                 'hidden', 'registry_enabled', 'tls_disabled', 'flavor_id', 'master_flavor_id',
                                 'volume_driver', 'docker_storage_driver', 'docker_volume_size', 'network_driver',
                                 'external_network_id', 'fixed_network', 'fixed_subnet', 'master_lb_enabled',
                                 'floating_ip_enabled']

        cluster_template_mock.return_value.ok = True
        cluster_template_mock.return_value.json.return_value = cluster_template_response

        # When
        response = ClusterTemplateService.get_cluster_template(
            mock_cluster_template_id)

        # Then
        self.assertListEqual(cluster_template_keys,
                             list(response.json().keys()))
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.list_cluster_templates_by_project')
    def test_list_cluster_template_by_project(self, cluster_template_mock):
        """Test the call flow for ClusterTemplateService.list_cluster_templates_by_project()."""

        # Given
        cluster_template_mock.return_value.ok = True

        # When
        response = ClusterTemplateService.list_cluster_templates_by_project()

        # Then
        assert response is not None
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.list_cluster_templates_by_project')
    def test_list_cluster_templates_by_project_response(self, cluster_template_mock):
        """Test the response for ClusterTemplateService.list_cluster_templates_by_project()."""

        # Given
        cluster_templates = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_cluster_templates_by_project.json'))

        cluster_template_mock.return_value.ok = True
        cluster_template_mock.return_value.json.return_value = cluster_templates

        # When
        response = ClusterTemplateService.list_cluster_templates_by_project()

        # Then
        self.assertListEqual(cluster_templates, response.json())
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.list_all_cluster_templates')
    def test_list_all_cluster_templates(self, cluster_template_mock):
        """Test the call flow for ClusterTemplateService.list_all_cluster_templates()."""

        # Given
        cluster_template_mock.return_value.ok = True

        # When
        response = ClusterTemplateService.list_all_cluster_templates()

        # Then
        assert response is not None
        cluster_template_mock.assert_called_once()

    @patch('ccp_server.api.v1.clusters.cluster_template.ClusterTemplateService.list_all_cluster_templates')
    def test_list_all_cluster_templates_response(self, cluster_template_mock):
        """Test the response for ClusterTemplateService.list_all_cluster_templates()."""

        # Given
        cluster_templates = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_all_cluster_templates.json'))

        cluster_template_mock.return_value.ok = True
        cluster_template_mock.return_value.json.return_value = cluster_templates

        # When
        response = ClusterTemplateService.list_all_cluster_templates()

        # Then
        self.assertListEqual(cluster_templates, response.json())
        cluster_template_mock.assert_called_once()
