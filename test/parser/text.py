import unittest
import xml.etree.ElementTree as ET

import svd.parser

class value(unittest.TestCase):
    xml = '''
    <node><text>
        Text
    </text></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.text(node, 'text')

        self.assertEqual(test, 'Text')

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.text(node, 'text', True)

        self.assertEqual(test, 'Text')

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.text(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.text(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.text(node, 'unknown', False, 'value')

        self.assertEqual(test, 'value')
