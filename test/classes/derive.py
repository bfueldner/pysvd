import unittest
import xml.etree.ElementTree as ET

import svd.classes

class root(svd.classes.base):

    def __init__(self, node):
        svd.classes.base.__init__(self, node)
        self.register = []

    def find(self, name):
        for register in self.register:
            if register.name == name:
                return register
        return None

class register(svd.classes.derive):

    def __init__(self, parent, node):
        svd.classes.derive.__init__(self, parent, node)

        attr = {}
        attr['name'] = svd.parser.text(svd.node.element(node, 'name', True))
        attr['description'] = svd.parser.text(svd.node.element(node, 'description', True))
        attr['address_offset'] = svd.parser.integer(svd.node.element(node, 'addressOffset'))
        attr['size'] = svd.parser.integer(svd.node.element(node, 'size'))
        self.add_attributes(attr)

class case(unittest.TestCase):

    def test_one_level(self):
        xml = '''
        <registers>
            <register>
                <name>TimerCtrl0</name>
                <description>Timer Control Register</description>
                <addressOffset>0x0</addressOffset>
                <access>read-write</access>
                <resetValue>0x00008001</resetValue>
                <resetMask>0x0000ffff</resetMask>
                <size>32</size>
            </register>
            <register derivedFrom="TimerCtrl0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
                <addressOffset>0x4</addressOffset>
            </register>
        </registers>
        '''
        node = ET.fromstring(xml)
        test = root(None)
        test.name = "root"
        register.add_elements(test, test.register, node, 'register')

        self.assertEqual(len(test.register), 2)

        self.assertEqual(type(test.register[0]), register)
        self.assertEqual(test.register[0].name, "TimerCtrl0")
        self.assertEqual(test.register[0].description, "Timer Control Register")
        self.assertEqual(test.register[0].address_offset, 0)
        self.assertEqual(test.register[0].size, 32)
        self.assertFalse(test.register[0].derived)

        self.assertEqual(type(test.register[1]), register)
        self.assertEqual(test.register[1].name, "TimerCtrl1")
        self.assertEqual(test.register[1].description, "Derived Timer")
        self.assertEqual(test.register[1].address_offset, 4)
        self.assertEqual(test.register[1].size, 32)
        self.assertTrue(test.register[1].derived)
