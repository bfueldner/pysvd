import unittest
import xml.etree.ElementTree as ET

from model import field
from model import fields
import type

class test_fields(unittest.TestCase):

    def setUp(self):
        self.node = ET.parse("res/" + __name__ + ".svd").getroot()

    def test_fields(self):
        flds = fields(None, self.node)
        self.assertEqual(len(flds.field), 2)

    def test_field_timerctrl0(self):
        flds = fields(None, self.node)
        fld = flds.field[0]

        self.assertEqual(fld.name, "TimerCtrl0_IntSel")
        self.assertEqual(fld.description, "Select interrupt line that is triggered by timer overflow.")
        self.assertEqual(fld.bit_offset, 1)
        self.assertEqual(fld.bit_width, 3)

        self.assertEqual(fld.access, type.access.read_write)
        self.assertEqual(fld.modified_write_values, type.modified_write_values.one_to_set)

        self.assertEqual(fld.read_action, type.read_action.clear)

        with self.assertRaises(AttributeError):
            x = fld.reset_mask

class test_bit_range(unittest.TestCase):
    def test_exception(self):
        svd = '''
        <field>
            <name>bitRangeException</name>
        </field>'''
        node = ET.fromstring(svd)
        with self.assertRaises(ValueError):
            test = field(None, node)

    def test_offset_width_style(self):
        svd = '''
        <field>
            <name>bitRangeOffsetWidthStyle</name>
            <bitOffset>4</bitOffset>
            <bitWidth>8</bitWidth>
        </field>'''
        node = ET.fromstring(svd)
        test = field(None, node)

        self.assertEqual(test.bit_offset, 4)
        self.assertEqual(test.bit_width, 8)

    def test_lsb_msb_style(self):
        svd = '''
        <field>
            <name>bitRangeLsbMsbStyle</name>
            <lsb>8</lsb>
            <msb>15</msb>
        </field>'''
        node = ET.fromstring(svd)
        test = field(None, node)

        self.assertEqual(test.bit_offset, 8)
        self.assertEqual(test.bit_width, 8)

    def test_pattern(self):
        svd = '''
        <field>
            <name>bitRangePattern</name>
            <bitRange>[23:4]</bitRange>
        </field>'''
        node = ET.fromstring(svd)
        test = field(None, node)

        self.assertEqual(test.bit_offset, 4)
        self.assertEqual(test.bit_width, 20)

if __name__ == "__main__":
    unittest.main()
