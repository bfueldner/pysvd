import unittest
import xml.etree.ElementTree as ET

import svd.element
import svd.type

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<interrupt />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.interrupt(None, node)

    def test_attributes(self):
        xml = '''
        <interrupt>
            <name>TIM0_INT</name>
            <value>34</value>
            <description>Timer0 Interrupt</description>
        </interrupt>'''
        node = ET.fromstring(xml)
        test = svd.element.interrupt(None, node)

        self.assertEqual(test.name, 'TIM0_INT')
        self.assertEqual(test.description, 'Timer0 Interrupt')
        self.assertEqual(test.value, 34)
