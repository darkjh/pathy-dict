import unittest

from pathy import *


class TestPathy(unittest.TestCase):
    def test_update_path(self):
        # all empty
        _dict = {}
        _path = 'a.b.c'
        _value = 1

        expected = {'a': {'b': {'c': 1}}}
        update_path_in_dict(_path, _value, _dict)
        self.assertDictEqual(expected, _dict)

        # add a sub-path to existing dict
        _dict = {'a': {'d': 2}}
        _path = 'a.b.c'
        _value = 1

        expected = {'a': {'b': {'c': 1}, 'd': 2}}
        update_path_in_dict(_path, _value, _dict)
        self.assertDictEqual(expected, _dict)

        # override existing value
        _dict = {'a': {'b': {'c': 2}}}
        _path = 'a.b.c'
        _value = 10

        expected = {'a': {'b': {'c': 10}}}
        update_path_in_dict(_path, _value, _dict)
        self.assertDictEqual(expected, _dict)

        # add value among existing values
        _dict = {'a': {'b': {'d': 100, 'f': 20}}}
        _path = 'a.b.c'
        _value = 1

        expected = {'a': {'b': {'c': 1, 'd': 100, 'f': 20}}}
        update_path_in_dict(_path, _value, _dict)
        self.assertDictEqual(expected, _dict)

        # top-level update
        _dict = {'a': 1}
        _path = 'a'
        _value = 2

        expected = {'a': 2}
        update_path_in_dict(_path, _value, _dict)
        self.assertDictEqual(expected, _dict)

        # won't update a non-dict element
        _dict = {'a': 1}
        _path = 'a.b'
        _value = 2

        expected = {'a': 1}  # not {'a': {'b': 2}}
        update_path_in_dict(_path, _value, _dict)
        self.assertDictEqual(expected, _dict)

    def test_flatten(self):
        _dict = {'a': {'b': {'d': 100, 'f': 20}}}
        expected = {'a.b.d': 100, 'a.b.f': 20}
        self.assertDictEqual(flatten_dict(_dict), expected)

        _dict = {'a.b.c': 100}
        self.assertDictEqual(flatten_dict(_dict), _dict)

    def test_deep_dict(self):
        _dict = {'a.b.d': 100, 'a.b.f': 20}
        expected = {'a': {'b': {'d': 100, 'f': 20}}}
        self.assertDictEqual(deep_dict(_dict), expected)

    def test_update_dict(self):
        _dict = {'a': {'b': {'c': 1}}, 'k': 3}
        update = {'a': {'e': 2}, 'k': 5}
        expected = {'a': {'e': 2, 'b': {'c': 1}}, 'k': 5}

        update_dict(_dict, update)
        self.assertDictEqual(_dict, expected)

    def test_delete_path(self):
        # normal case
        _dict = {'a': {'b': {'c': 1, 'd': [1, 2]}}}
        path = 'a.b.c'
        expected = {'a': {'b': {'d': [1, 2]}}}
        delete_path_in_dict(path, _dict)
        self.assertEqual(_dict, expected)

        # length 1 path
        _dict = {'a': {'b': {'c': 1, 'd': [1, 2]}}}
        path = 'a'
        expected = {}
        delete_path_in_dict(path, _dict)
        self.assertEqual(_dict, expected)

        # `path` does not exist
        _dict = {'a': {'b': {'c': 1, 'd': [1, 2]}}}
        path = 'd.k'
        expected = {'a': {'b': {'c': 1, 'd': [1, 2]}}}
        delete_path_in_dict(path, _dict)
        self.assertDictEqual(_dict, expected)

    def test_clean_dict(self):
        # basic cleaning
        _dict = {'a': {}, 'b': 1}
        clean_dict(_dict)
        self.assertEqual(_dict, {'b': 1})

        _dict = {'a': [], 'b': 1}
        clean_dict(_dict)
        self.assertEqual(_dict, {'b': 1})

        _dict = {'a': None, 'b': 1}
        clean_dict(_dict)
        self.assertEqual(_dict, {'b': 1})

        # deeper cleaning
        _dict = {'a': {'b': {'c': [], 'd': 1}}}
        clean_dict(_dict)
        self.assertEqual(_dict, {'a': {'b': {'d': 1}}})