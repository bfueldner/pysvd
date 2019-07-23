import unittest
import xml.etree.ElementTree as ET

import svd.classes

class root(svd.classes.base):

    def __init__(self, node):
        super().__init__(node)

        self.name = "root"
        self.register = []
        register.add_elements(self, self.register, node, 'register')

    def find(self, name):
        for register in self.register:
            if register.name == name:
                return register
        return None

class register(svd.classes.derive):

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = svd.parser.text(svd.node.element(node, 'name', True))
        attr['description'] = svd.parser.text(svd.node.element(node, 'description', True))
        attr['address_offset'] = svd.parser.integer(svd.node.element(node, 'addressOffset'))
        attr['size'] = svd.parser.integer(svd.node.element(node, 'size'))
        self.add_attributes(attr)

        self.field = []
        field.add_elements(self, self.field, node, 'field')

    def find(self, name):
        for field in self.field:
            if field.name == name:
                return field
        return None

class field(svd.classes.derive):

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = svd.parser.text(svd.node.element(node, 'name', True))
        attr['description'] = svd.parser.text(svd.node.element(node, 'description', True))
        attr['access'] = svd.parser.enum(svd.type.access, svd.node.element(node, 'access'))
        self.add_attributes(attr)

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''
        <registers>
            <register>
                <name>TimerCtrl0</name>
                <description>Timer Control Register</description>
            </register>
            <register derivedFrom="UartCtrl0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
            </register>
        </registers>'''

        node = ET.fromstring(xml)
        with self.assertRaises(KeyError):
            root(node)

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
        </registers>'''

        node = ET.fromstring(xml)
        test = root(node)

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

    def test_two_level(self):
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
                <field>
                    <name>BitField0</name>
                    <description>Bit field 0</description>
                    <access>read-write</access>
                </field>
            </register>
            <register derivedFrom="TimerCtrl0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
                <addressOffset>0x4</addressOffset>
                <field derivedFrom="TimerCtrl0.BitField0">
                    <name>BitField1</name>
                    <description>Bit field 1</description>
                </field>
            </register>
        </registers>'''

        node = ET.fromstring(xml)
        test = root(node)

        self.assertEqual(len(test.register), 2)

        self.assertEqual(type(test.register[0]), register)
        self.assertEqual(test.register[0].name, "TimerCtrl0")
        self.assertEqual(test.register[0].description, "Timer Control Register")
        self.assertEqual(test.register[0].address_offset, 0)
        self.assertEqual(test.register[0].size, 32)
        self.assertFalse(test.register[0].derived)

        self.assertEqual(len(test.register[0].field), 1)

        self.assertEqual(test.register[0].field[0].name, "BitField0")
        self.assertEqual(test.register[0].field[0].description, "Bit field 0")
        self.assertEqual(test.register[0].field[0].access, svd.type.access.read_write)
        self.assertFalse(test.register[0].field[0].derived)

        self.assertEqual(type(test.register[1]), register)
        self.assertEqual(test.register[1].name, "TimerCtrl1")
        self.assertEqual(test.register[1].description, "Derived Timer")
        self.assertEqual(test.register[1].address_offset, 4)
        self.assertEqual(test.register[1].size, 32)
        self.assertTrue(test.register[1].derived)

        self.assertEqual(len(test.register[1].field), 1)

        self.assertEqual(test.register[1].field[0].name, "BitField1")
        self.assertEqual(test.register[1].field[0].description, "Bit field 1")
        self.assertEqual(test.register[1].field[0].access, svd.type.access.read_write)
        self.assertTrue(test.register[1].field[0].derived)
