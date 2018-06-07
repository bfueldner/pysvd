import unittest
import xml.etree.ElementTree as ET

import svd.element

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<enumeratedValues />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.enumerated_values(None, node)

    def test_minimal(self):
        xml = '''
        <enumeratedValues>
            <enumeratedValue>
                <value>0</value>
            </enumeratedValue>
        </enumeratedValues>'''

        node = ET.fromstring(xml)
        test = svd.element.enumerated_values(None, node)

        self.assertEqual(test.usage, svd.type.enum_usage.read_write)
        self.assertEqual(len(test.enumerated_value), 1)

        self.assertEqual(test.enumerated_value[0].value, 0)

    def test_attributes(self):
        xml = '''
        <enumeratedValues>
            <name>TimerIntSelect</name>
            <headerEnumName>TimerIntSelectEnum</headerEnumName>
            <usage>read-write</usage>
            <enumeratedValue>
                <name>disabled</name>
                <description>The clock source clk0 is turned off.</description>
                <value>0</value>
            </enumeratedValue>
            <enumeratedValue>
                <name>enabled</name>
                <description>The clock source clk1 is running.</description>
                <value>1</value>
            </enumeratedValue>
            <enumeratedValue>
                <name>reserved</name>
                <description>Reserved values. Do not use.</description>
                <isDefault>true</isDefault>
            </enumeratedValue>
        </enumeratedValues>'''

        node = ET.fromstring(xml)
        test = svd.element.enumerated_values(None, node)

        self.assertEqual(test.name, "TimerIntSelect")
        self.assertEqual(test.header_enum_name, "TimerIntSelectEnum")
        self.assertEqual(test.usage, svd.type.enum_usage.read_write)
        self.assertEqual(len(test.enumerated_value), 3)

        self.assertEqual(test.enumerated_value[0].name, "disabled")
        self.assertEqual(test.enumerated_value[0].description, "The clock source clk0 is turned off.")
        self.assertEqual(test.enumerated_value[0].value, 0)

        self.assertEqual(test.enumerated_value[1].name, "enabled")
        self.assertEqual(test.enumerated_value[1].description, "The clock source clk1 is running.")
        self.assertEqual(test.enumerated_value[1].value, 1)

        self.assertEqual(test.enumerated_value[2].name, "reserved")
        self.assertEqual(test.enumerated_value[2].description, "Reserved values. Do not use.")
        self.assertTrue(test.enumerated_value[2].is_default)

    def test_derived(self):
        self.assertTrue(False)
