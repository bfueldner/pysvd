import unittest
import xml.etree.ElementTree as ET

import svd.parser

class false_integer(unittest.TestCase):
    xml = '''
    <node><boolean>
        0
    </boolean></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean')

        self.assertEqual(test, False)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean', True)

        self.assertEqual(test, False)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.boolean(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False, False)

        self.assertEqual(test, False)

class false_text(unittest.TestCase):
    xml = '''
    <node><boolean>
        fAlSe
    </boolean></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean')

        self.assertEqual(test, False)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean', True)

        self.assertEqual(test, False)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.boolean(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False, False)

        self.assertEqual(test, False)

class true_integer(unittest.TestCase):
    xml = '''
    <node><boolean>
        1
    </boolean></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean')

        self.assertEqual(test, True)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean', True)

        self.assertEqual(test, True)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.boolean(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False, True)

        self.assertEqual(test, True)

class true_text(unittest.TestCase):
    xml = '''
    <node><boolean>
        TrUe
    </boolean></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean')

        self.assertEqual(test, True)

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'boolean', True)

        self.assertEqual(test, True)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.boolean(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False, True)

        self.assertEqual(test, True)

class exception(unittest.TestCase):
    xml = '''
    <node><boolean>
        text
    </boolean></node>'''

    def test_no_param(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(ValueError):
            test = svd.parser.boolean(node, 'boolean')

    def test_mandatory_present(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(ValueError):
            test = svd.parser.boolean(node, 'boolean', True)

    def test_mandatory_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            svd.parser.boolean(node, 'unknown', True)

    def test_default_none(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False)

        self.assertIsNone(test)

    def test_default_value(self):
        node = ET.fromstring(self.xml)
        test = svd.parser.boolean(node, 'unknown', False, True)

        self.assertEqual(test, True)
