import unittest

import svd.parser
import svd.type

class value(unittest.TestCase):

    def test_default_none(self):
        test = svd.parser.enum(svd.type.access, None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = svd.parser.enum(svd.type.access, None, svd.type.access.read_only)

        self.assertEqual(test, svd.type.access.read_only)

    def test_enum(self):
        test = svd.parser.enum(svd.type.access, 'read-write')

        self.assertEqual(test, svd.type.access.read_write)

    def test_exception(self):
        with self.assertRaises(KeyError):
            test = svd.parser.enum(svd.type.access, 'unknown')
