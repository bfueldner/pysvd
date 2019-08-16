import unittest
import xml.etree.ElementTree as ET

import svd.element

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<field />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.enumerated_values(None, node)

    def test_bit_range_offset(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <bitOffset>4</bitOffset>
        </field>'''

        node = ET.fromstring(xml)
        test = svd.element.field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bit_offset, 4)
        self.assertEqual(test.bit_width, 1)

    def test_bit_range_offset_width(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <bitOffset>5</bitOffset>
            <bitWidth>3</bitWidth>
        </field>'''

        node = ET.fromstring(xml)
        test = svd.element.field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bit_offset, 5)
        self.assertEqual(test.bit_width, 3)

    def test_bit_range_lsb_msb(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <lsb>16</lsb>
            <msb>31</msb>
        </field>'''

        node = ET.fromstring(xml)
        test = svd.element.field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bit_offset, 16)
        self.assertEqual(test.bit_width, 16)

    def test_bit_range_pattern(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <bitRange>[7:4]</bitRange>
        </field>'''

        node = ET.fromstring(xml)
        test = svd.element.field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bit_offset, 4)
        self.assertEqual(test.bit_width, 4)

    def test_attributes(self):
        xml = '''
        <field>
            <name>TimerCtrl0_IntSel</name>
            <description>Select interrupt line that is triggered by timer overflow.</description>
            <bitOffset>1</bitOffset>
            <bitWidth>3</bitWidth>
            <access>read-write</access>
            <resetValue>0x0</resetValue>
            <modifiedWriteValues>oneToSet</modifiedWriteValues>
            <writeConstraint>
                <range>
                    <minimum>0</minimum>
                    <maximum>5</maximum>
                </range>
            </writeConstraint>
            <readAction>clear</readAction>
        </field>'''

        node = ET.fromstring(xml)
        test = svd.element.field(None, node)

        self.assertEqual(test.name, "TimerCtrl0_IntSel")
        self.assertEqual(test.description, "Select interrupt line that is triggered by timer overflow.")
        self.assertEqual(test.bit_offset, 1)
        self.assertEqual(test.bit_width, 3)

        self.assertEqual(test.access, svd.type.access.read_write)
        self.assertEqual(test.reset_value, 0)

        x = '''

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
        '''
    def test_derived(self):
        self.assertTrue(False)
