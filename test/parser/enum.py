import unittest
import xml.etree.ElementTree as ET

import svd.parser
import svd.type

class value(unittest.TestCase):
    xml = '''
    <node><enum>
        read-write
    </enum></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.enum(svd.type.access, node, 'enum')

        self.assertEqual(test, svd.type.access.read_write)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.enum(svd.type.access, node, 'enum', True)

        self.assertEqual(test, svd.type.access.read_write)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.enum(svd.type.access, node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.enum(svd.type.access, node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.enum(svd.type.access, node, 'unknown', False, svd.type.access.read_only)

        self.assertEqual(test, svd.type.access.read_only)

class exception(unittest.TestCase):
    xml = '''
    <node><enum>
        text
    </enum></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(KeyError):
            test = svd.parser.enum(svd.type.access, node, 'enum')

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(KeyError):
            test = svd.parser.enum(svd.type.access, node, 'enum', True)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.enum(svd.type.access, node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.enum(svd.type.access, node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.enum(svd.type.access, node, 'unknown', False, svd.type.access.read_only)

        self.assertEqual(test, svd.type.access.read_only)
