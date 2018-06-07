import unittest
import xml.etree.ElementTree as ET

import svd.element

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<writeConstraint />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.write_constraint(None, node)

    def test_write_as_read(self):
        xml = '''
        <writeConstraint>
            <writeAsRead>true</writeAsRead>
        </writeConstraint>'''

        node = ET.fromstring(xml)
        test = svd.element.write_constraint(None, node)

        self.assertTrue(test.write_as_read)

    def test_use_enumerated_values(self):
        xml = '''
        <writeConstraint>
            <useEnumeratedValues>true</useEnumeratedValues>
        </writeConstraint>'''

        node = ET.fromstring(xml)
        test = svd.element.write_constraint(None, node)

        self.assertTrue(test.use_enumerated_values)

    def test_range(self):
        xml = '''
        <writeConstraint>
            <range>
                <minimum>2</minimum>
                <maximum>4</maximum>
            </range>
        </writeConstraint>'''

        node = ET.fromstring(xml)
        test = svd.element.write_constraint(None, node)

        self.assertEqual(test.range_minimum, 2)
        self.assertEqual(test.range_maximum, 4)
