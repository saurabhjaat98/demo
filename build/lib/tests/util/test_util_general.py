###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Saurabh Choudhary <saurabhchoudhary@coredge.io>, march 2023      #
###############################################################################
from ccp_server.util.exceptions import InvalidTypeException
from ccp_server.util.general import flatten_dict
from ccp_server.util.general import remove_key_from_dict
from tests.test_base import TestBase


class TestRemoveKeyFromDict(TestBase):
    test_dict = {'a': 1, 'b': {'c': 2, 'd': 3},
                 'e': [{'f': 4}, {'a': 5}, {'b': {'a': 6}}]}

    def test_remove_key(self):
        remove_key_from_dict('a', self.test_dict)
        self.assertNotIn('a', self.test_dict)

    def test_remove_nested_key(self):
        remove_key_from_dict('c', self.test_dict)
        self.assertNotIn('c', self.test_dict['b'])

    def test_invalid_type(self):
        self.assertRaises(InvalidTypeException,
                          remove_key_from_dict, 123, self.test_dict)

    def test_remove_key_from_list(self):
        remove_key_from_dict('a', self.test_dict)
        self.assertNotIn('a', self.test_dict['e'][1])


class TestFlattenDict(TestBase):
    def test_flatten_dict(self):
        input_dict = {
            'a': 1, 'b': {'c': 2, 'd': {'e': 3, 'f': {'g': 4}}}, 'e': [8, 9, {'a': 5}]
        }
        expected_dict = {
            'a': 1,
            'b.c': 2,
            'b.d.e': 3,
            'b.d.f.g': 4,
            'e.0': 8,
            'e.1': 9,
            'e.2.a': 5
        }
        result = flatten_dict(input_dict)
        self.assertDictEqual(result, expected_dict)

    def test_flatten_dict_with_empty_data(self):
        input_dict = {}
        expected_dict = {}
        result = flatten_dict(input_dict)
        self.assertDictEqual(result, expected_dict)

    def test_dict_with_duplicate_keys(self):
        input_dict = {'a': 1, 'b': {'a': 2, 'c': {'a': 3}}}
        expected_dict = {
            'a': 1,
            'b.a': 2,
            'b.c.a': 3
        }

        result = flatten_dict(input_dict)
        self.assertDictEqual(result, expected_dict)
