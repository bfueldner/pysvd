import unittest
import xml.etree.ElementTree as ET

from model import enumerated_value

class test_enumerated_value(unittest.TestCase):
    def test_exception(self):
        svd = '''<enumerated_value />'''
        node = ET.fromstring(svd)
        with self.assertRaises(SyntaxError):
            test = enumerated_value(None, node)

    def test_attributes_default(self):
        svd = '''
        <enumerated_value>
            <name>Name</name>
            <description>Description</description>
            <isDefault>1</isDefault>
        </enumerated_value>'''
        node = ET.fromstring(svd)
        test = enumerated_value(None, node)

        self.assertEqual(test.name, "Name")
        self.assertEqual(test.description, "Description")
        self.assertEqual(test.is_default, True)

    def test_value_decimal(self):
        svd = '''
        <enumerated_value>
            <value>1</value>
        </enumerated_value>'''
        node = ET.fromstring(svd)
        test = enumerated_value(None, node)

        self.assertEqual(test.value, 1)

    def test_value_hex(self):
        svd = '''
        <enumerated_value>
            <value>0x10</value>
        </enumerated_value>'''
        node = ET.fromstring(svd)
        test = enumerated_value(None, node)

        self.assertEqual(test.value, 16)

    def test_value_binary1(self):
        svd = '''
        <enumerated_value>
            <value>0b1000</value>
        </enumerated_value>'''
        node = ET.fromstring(svd)
        test = enumerated_value(None, node)

        self.assertEqual(test.value, 8)

    def test_value_binary2(self):
        svd = '''
        <enumerated_value>
            <value>#1000</value>
        </enumerated_value>'''
        node = ET.fromstring(svd)
        test = enumerated_value(None, node)

        self.assertEqual(test.value, 8)

    def test_value_binary1_do_not_care(self):
        svd = '''
        <enumerated_value>
            <value>0bx1x1</value>
        </enumerated_value>'''
        node = ET.fromstring(svd)
        test = enumerated_value(None, node)

        self.assertEqual(test.value, 5)

    def test_value_binary2_do_not_care(self):
        svd = '''
        <enumerated_value>
            <value>#x1x1</value>
        </enumerated_value>'''
        node = ET.fromstring(svd)
        test = enumerated_value(None, node)

        self.assertEqual(test.value, 5)

if __name__ == "__main__":
    unittest.main()
