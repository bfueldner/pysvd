import unittest
import xml.etree.ElementTree as ET

import svd.element
import svd.type

class case(unittest.TestCase):

    def test_empty(self):
        xml = '''<sauRegionsConfig />'''
        node = ET.fromstring(xml)
        test = svd.element.sau_region_config(None, node)

        self.assertEqual(len(test.region), 0)

    def test_attributes(self):
        xml = '''
        <sauRegionsConfig>
            <region name="SAU1">
                <base>0x10001000</base>
                <limit>0x10005000</limit>
                <access>n</access>
            </region>
            <region enabled="false" name="SAU2">
                <base>0x10006000</base>
                <limit>0x10008000</limit>
                <access>c</access>
            </region>
        </sauRegionsConfig>'''
        node = ET.fromstring(xml)
        test = svd.element.sau_region_config(None, node)

        self.assertEqual(len(test.region), 2)

        self.assertTrue(test.region[0].enabled)
        self.assertEqual(test.region[0].name, 'SAU1')
        self.assertEqual(test.region[0].base, 0x10001000)
        self.assertEqual(test.region[0].limit, 0x10005000)
        self.assertEqual(test.region[0].access, svd.type.region_access.non_secure)

        self.assertFalse(test.region[1].enabled)
        self.assertEqual(test.region[1].name, 'SAU2')
        self.assertEqual(test.region[1].base, 0x10006000)
        self.assertEqual(test.region[1].limit, 0x10008000)
        self.assertEqual(test.region[1].access, svd.type.region_access.secure_callable)
