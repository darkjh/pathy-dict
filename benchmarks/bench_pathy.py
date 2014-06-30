import time
import json
import os
import unittest

from pathy import *


_FIXTURE_FILE_PATH = os.path.join(
    os.getcwd(), 'fixtures', 'fixtures.json')


def _load_fixture_dicts():
    f = open(_FIXTURE_FILE_PATH)
    return [json.loads(doc_str) for doc_str in f.readlines()]


class BenchPathy(unittest.TestCase):
    def setUp(self):
        self.fixture = _load_fixture_dicts()

    def test_bench_path_in_dict(self):
        _dict = self.fixture[0]
        path1 = 'metadata.title.duplicates.nb'

        before = time.time()
        for i in xrange(0, 10000):
            path_in_dict(path1, _dict)
        after = time.time()

        used = after - before
        avg = used / 10000

        print used
        print avg

    def test_bench_update_path_in_dict(self):
        _dict = self.fixture[0]
        path1 = 'metadata.title.duplicates.urls'
        l = [1, 2, 3, 4]

        before = time.time()
        for i in xrange(0, 10000):
            update_path_in_dict(path1, l, _dict)
        after = time.time()

        used = after - before
        avg = used / 10000

        print used
        print avg