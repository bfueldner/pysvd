import unittest
import xml.etree.ElementTree as ET

from model import region
import type

class test_region(unittest.TestCase):
    def test_exception(self):
        svd = '''<region />'''
        node = ET.fromstring(svd)
        with self.assertRaises(SyntaxError):
            test = region(None, node)

    def test_attributes_default(self):
        svd = '''
        <region enabled="false" name="SAU2">
            <base>0x10006000</base>
            <limit>0x10008000</limit>
            <access>c</access>
        </region>'''
        node = ET.fromstring(svd)
        test = region(None, node)

        self.assertEqual(test.base, type.cpu_name.cm7)
        self.assertEqual(test.limit, "r0p0")
        self.assertEqual(test.access, type.protection.little)

        with self.assertRaises(AttributeError):
            self.assertIsNotNone(test.sau_num_regions)

if __name__ == "__main__":
    unittest.main()
