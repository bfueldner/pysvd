import unittest
import xml.etree.ElementTree as ET

import svd.element
import svd.type

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<addressBlock />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.address_block(None, node)

    def test_attributes(self):
        xml = '''
        <addressBlock>
            <offset>0x0</offset>
            <size>0x400</size>
            <usage>registers</usage>
            <protection>s</protection>
        </addressBlock>'''
        node = ET.fromstring(xml)
        test = svd.element.address_block(None, node)

        self.assertEqual(test.offset, 0)
        self.assertEqual(test.size, 0x400)
        self.assertEqual(test.usage, svd.type.usage.registers)
        self.assertEqual(test.protection, svd.type.protection.secure_callable)
