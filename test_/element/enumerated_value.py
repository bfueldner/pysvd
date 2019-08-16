import unittest
import xml.etree.ElementTree as ET

import svd.element

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<enumeratedValue />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.enumerated_value(None, node)

    def test_minimal(self):
        xml = '''
        <enumeratedValue>
            <value>0</value>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = svd.element.enumerated_value(None, node)

        self.assertEqual(test.value, 0)

    def test_attributes_value(self):
        xml = '''
        <enumeratedValue>
            <name>disabled</name>
            <description>The clock source clk0 is turned off.</description>
            <value>0</value>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = svd.element.enumerated_value(None, node)

        self.assertEqual(test.name, "disabled")
        self.assertEqual(test.description, "The clock source clk0 is turned off.")
        self.assertEqual(test.value, 0)

        with self.assertRaises(AttributeError):
            self.assertIsNone(test.is_default)

    def test_attributes_is_default(self):
        xml = '''
        <enumeratedValue>
            <name>reserved</name>
            <description>Reserved values. Do not use.</description>
            <isDefault>true</isDefault>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = svd.element.enumerated_value(None, node)

        self.assertEqual(test.name, "reserved")
        self.assertEqual(test.description, "Reserved values. Do not use.")
        self.assertTrue(test.is_default)

        with self.assertRaises(AttributeError):
            self.assertIsNone(test.value)
