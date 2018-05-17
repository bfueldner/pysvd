import unittest
import xml.etree.ElementTree as ET

import parser

class test_parser_integer(unittest.TestCase):
    xml = '''
    <node><integer>
        4711
    </integer></node>'''

    def test_integer_no_param(self):
        node = ET.fromstring(self.xml)
        test = parser.integer(node, 'integer')

        self.assertEqual(test, 4711)

    def test_integer_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = parser.integer(node, 'integer', True)

        self.assertEqual(test, 4711)

    def test_integer_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            parser.integer(node, 'hexadecimal', True)

    def test_integer_default_none(self):
        node = ET.fromstring(self.xml)
        test = parser.integer(node, 'hexadecimal', False)

        self.assertIsNone(test)

    def test_integer_default_value(self):
        node = ET.fromstring(self.xml)
        test = parser.integer(node, 'hexadecimal', False, 815)

        self.assertEqual(test, 815)

if __name__ == "__main__":
    unittest.main()
