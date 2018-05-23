import unittest
import xml.etree.ElementTree as ET

import svd.node

class case(unittest.TestCase):
    xml = '''
    <node value=" text " />
    '''

    def test_value(self):
        node = ET.fromstring(self.xml)
        test = svd.node.attribute(node, 'value')

        self.assertEqual(test, 'text')

    def test_none(self):
        node = ET.fromstring(self.xml)
        test = svd.node.attribute(node, 'unknown')

        self.assertIsNone(test)

    def test_exception(self):
        node = ET.fromstring(self.xml)
        with self.assertRaises(SyntaxError):
            test = svd.node.attribute(node, 'unknown', True)
