import unittest

import svd.parser

class value(unittest.TestCase):

    def test_no_param(self):
        test = svd.parser.text('Text')

        self.assertEqual(test, 'Text')

    def test_default_none(self):
        test = svd.parser.text(None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = svd.parser.text(None, 'value')

        self.assertEqual(test, 'value')
