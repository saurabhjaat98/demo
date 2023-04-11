###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Manik Sidana <manik@coredge.io>, Mar 2023                        #
###############################################################################
import unittest
from unittest.mock import patch

from ccp_server.api.v1.admin.aggregate import AggregateService
from tests.test_base import KC_MOCK
from tests.test_base import TestBase


class TestAggregate(TestBase):

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.admin.aggregate.AggregateService.list_aggregates')
    def test_list_aggregates(self, aggregate_mock, kc_mock):
        """Test the call flow for AggregateService.list_aggregates()."""
        # When
        AggregateService.list_aggregates()
        # Then
        aggregate_mock.assert_called_once()

    @patch(KC_MOCK)
    @patch('ccp_server.api.v1.admin.aggregate.AggregateService.get_aggregate')
    def test_get_aggregate(self, aggregate_mock, kc_mock):
        """Test the call flow for AggregateService.get_aggregate()"""
        # Given
        mock_agg_id = '7e5c2cc1-4085-4f16-8fc5-93021ccbefa7'
        # When
        AggregateService.get_aggregate(mock_agg_id)
        # Then
        aggregate_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
