import unittest
import xml.etree.ElementTree as ET
import pysvd


class TestNodeElement(unittest.TestCase):
    xml = '''
    <node><value>
        text
    </value></node>'''

    def test_value(self):
        node = ET.fromstring(self.xml)
        test = pysvd.node.Element(node, 'value')

        self.assertEqual(test, 'text')

    def test_none(self):
        node = ET.fromstring(self.xml)
        test = pysvd.node.Element(node, 'unknown')

        self.assertIsNone(test)

    def test_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            pysvd.node.Element(node, 'unknown', True)


class TestNodeAttribute(unittest.TestCase):
    xml = '''
    <node value=" text " />
    '''

    def test_value(self):
        node = ET.fromstring(self.xml)
        test = pysvd.node.Attribute(node, 'value')

        self.assertEqual(test, 'text')

    def test_none(self):
        node = ET.fromstring(self.xml)
        test = pysvd.node.Attribute(node, 'unknown')

        self.assertIsNone(test)

    def test_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            pysvd.node.Attribute(node, 'unknown', True)
