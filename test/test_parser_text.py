import unittest
import xml.etree.ElementTree as ET

import parser

class test_parser_text(unittest.TestCase):
    xml = '''
    <node><text>
        Text
    </text></node>'''

    def test_text_no_param(self):
        node = ET.fromstring(self.xml)
        test = parser.text(node, 'text')

        self.assertEqual(test, 'Text')

    def test_text_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = parser.text(node, 'text', True)

        self.assertEqual(test, 'Text')

    def test_text_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            parser.text(node, 'description', True)

    def test_text_default_none(self):
        node = ET.fromstring(self.xml)
        test = parser.text(node, 'description', False)

        self.assertIsNone(test)

    def test_text_default_value(self):
        node = ET.fromstring(self.xml)
        test = parser.text(node, 'description', False, 'value')

        self.assertEqual(test, 'value')

if __name__ == "__main__":
    unittest.main()
