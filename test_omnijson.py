#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest as unittest

import omnijson as json


class OmniSuite(unittest.TestCase):

    def setUp(self):
        self._good_json_string = '{"yo": "dawg"}'
        self._good_json_result = {'yo': 'dawg'}
        self._bad_json_string = '{"yo": dawg"}'

    def test_load_json(self):
        a = json.loads(self._good_json_string)
        self.assertEqual(a, self._good_json_result)

    def test_dump_json(self):
        a = json.dumps(self._good_json_result)
        self.assertEqual(a, self._good_json_string)

    def test_load_bad_json(self):
        self.assertRaises(
            json.JSONError,
            json.loads,
            self._bad_json_string
        )


if __name__ == '__main__':
    print(sys.platform, sys.version)
    print('omnijson %s' % json.__version__)
    print('omnijson engine %s' % json.core.engine)
    unittest.main()
