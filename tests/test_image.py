###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Aman kadhala <aman@coredge.io>, Mar 2023                         #
###############################################################################
import os
import unittest
from unittest.mock import patch

from ccp_server.api.v1.image import ImageService
from tests.test_base import TestBase


class TestImage(TestBase):

    @patch('ccp_server.api.v1.image.ImageService.list_images')
    def test_list_image(self, image_mock):
        """Test the call flow for ImageService.list_images()."""

        # Given
        image_mock.return_value.ok = True

        # When
        response = ImageService.list_images()

        # Then
        assert response is not None
        image_mock.assert_called_once()

    @patch('ccp_server.api.v1.image.ImageService.list_images')
    def test_list_image_response(self, image_mock):
        """Test the response for ImageService.list_images()."""

        # Given
        images = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'list_image.json'))
        image_mock.return_value.ok = True
        image_mock.return_value.json.return_value = images

        # When
        response = ImageService.list_images()

        # Then
        self.assertListEqual(images, response.json())
        image_mock.assert_called_once()

    @patch('ccp_server.api.v1.image.ImageService.get_image')
    def test_get_image(self, image_mock):
        """Test the call flow for ImageService.get_image()."""

        # Given
        image_mock.return_value.ok = True

        # When
        response = ImageService.get_image()

        # Then
        assert response is not None
        image_mock.assert_called_once()

    @patch('ccp_server.api.v1.image.ImageService.get_image')
    def test_get_images_response(self, image_mock):
        """Test the response for ImageService.get_image()."""

        # Given
        mock_image_id = self.generate_uuid4()
        image_response = self.read_json(os.path.join(
            os.path.dirname(__file__), 'data', 'get_image.json'))
        image_keys = ["name", "id", "disk_format", "container_format", "visibility", "size", "status", "owner",
                      "cloud_meta"]
        image_mock.return_value.ok = True
        image_mock.return_value.json.return_value = image_response

        # When
        response = ImageService.get_image(mock_image_id)

        # Then
        self.assertListEqual(image_keys, list(response.json().keys()))
        image_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
