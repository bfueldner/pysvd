import unittest

import svd.parser

class value(unittest.TestCase):

    def test_default_none(self):
        test = svd.parser.boolean(None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = svd.parser.boolean(None, False)

        self.assertEqual(test, False)

    def test_false_value(self):
        test = svd.parser.boolean('0')

        self.assertEqual(test, False)

    def test_false_text(self):
        test = svd.parser.boolean('FaLsE')

        self.assertEqual(test, False)

    def test_true_value(self):
        test = svd.parser.boolean('1')

        self.assertEqual(test, True)

    def test_true_text(self):
        test = svd.parser.boolean('tRuE')

        self.assertEqual(test, True)

    def test_exception(self):
        with self.assertRaises(ValueError):
            test = svd.parser.boolean('text')
