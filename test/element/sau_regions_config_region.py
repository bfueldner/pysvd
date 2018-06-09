import unittest
import xml.etree.ElementTree as ET

import svd.element
import svd.type

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<region />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.sau_regions_config_region(None, node)

    def test_attributes(self):
        xml = '''
        <region enabled="false" name="SAU2">
            <base>0x10006000</base>
            <limit>0x10008000</limit>
            <access>c</access>
        </region>'''
        node = ET.fromstring(xml)
        test = svd.element.sau_regions_config_region(None, node)

        self.assertEqual(test.base, 0x10006000)
        self.assertEqual(test.limit, 0x10008000)
        self.assertEqual(test.access, svd.type.region_access.secure_callable)

        self.assertEqual(test.name, "SAU2")
        self.assertFalse(test.enabled)