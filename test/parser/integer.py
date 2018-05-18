import unittest
import xml.etree.ElementTree as ET

import svd.parser

class decimal(unittest.TestCase):
    xml = '''
    <node><integer>
        4711
    </integer></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer')

        self.assertEqual(test, 4711)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer', True)

        self.assertEqual(test, 4711)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.integer(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False, 815)

        self.assertEqual(test, 815)

class hexadecimal(unittest.TestCase):
    xml = '''
    <node><integer>
        0x1234
    </integer></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer')

        self.assertEqual(test, 0x1234)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer', True)

        self.assertEqual(test, 0x1234)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.integer(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False, 0xABCD)

        self.assertEqual(test, 0xABCD)

class binary1(unittest.TestCase):
    xml = '''
    <node><integer>
        0b110xx011
    </integer></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer')

        self.assertEqual(test, 195)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer', True)

        self.assertEqual(test, 195)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.integer(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False, 16)

        self.assertEqual(test, 16)

class binary2(unittest.TestCase):
    xml = '''
    <node><integer>
        #110xx011
    </integer></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer')

        self.assertEqual(test, 195)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'integer', True)

        self.assertEqual(test, 195)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.integer(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False, 16)

        self.assertEqual(test, 16)

class exception(unittest.TestCase):
    xml = '''
    <node><integer>
        text
    </integer></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(ValueError):
            test = svd.parser.integer(node, 'integer')

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(ValueError):
            test = svd.parser.integer(node, 'integer', True)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.integer(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.integer(node, 'unknown', False, 16)

        self.assertEqual(test, 16)
