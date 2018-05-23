import unittest

import svd.parser

class value(unittest.TestCase):

    def test_default_none(self):
        test = svd.parser.integer(None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = svd.parser.integer(None, 16)

        self.assertEqual(test, 16)

    def test_decimal(self):
        test = svd.parser.integer('4711')

        self.assertEqual(test, 4711)

    def test_hexadecimal(self):
        test = svd.parser.integer('0x1234')

        self.assertEqual(test, 0x1234)

    def test_binary_0b(self):
        test = svd.parser.integer('0b110xx011')

        self.assertEqual(test, 195)

    def test_binary_hash(self):
        test = svd.parser.integer('#110xx011')

        self.assertEqual(test, 195)

    def test_exception(self):
        with self.assertRaises(ValueError):
            test = svd.parser.integer('text')
