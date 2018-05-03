import unittest

from model import register
from model import registers

from type import accessType

import xml.etree.ElementTree as ET

svd = '''
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

class test_register_derive(unittest.TestCase):

    def setUp(self):
        self.node = ET.fromstring(svd)

    def test_register_count(self):
        regs = registers(None, self.node)
        self.assertEqual(len(regs.register), 2)

    def test_register_timer_ctrl0(self):
        regs = registers(None, self.node)
        self.assertEqual(regs.register[0].name, "TimerCtrl0")
        self.assertEqual(regs.register[0].description, "Timer Control Register")
        self.assertEqual(regs.register[0].address_offset, 0x00)

        self.assertEqual(regs.register[0].access, accessType.read_write)
        self.assertEqual(regs.register[0].reset_value, 0x00008001)
        self.assertEqual(regs.register[0].reset_mask, 0x0000ffff)
        self.assertEqual(regs.register[0].size, 32)

        with self.assertRaises(AttributeError):
            x = regs.register[0].data_type

    def test_register_timer_ctrl1(self):
        regs = registers(None, self.node)
        self.assertEqual(regs.register[1].name, "TimerCtrl1")
        self.assertEqual(regs.register[1].description, "Derived Timer")
        self.assertEqual(regs.register[1].address_offset, 0x04)

        self.assertEqual(regs.register[1].access, accessType.read_write)
        self.assertEqual(regs.register[1].reset_value, 0x00008001)
        self.assertEqual(regs.register[1].reset_mask, 0x0000ffff)
        self.assertEqual(regs.register[1].size, 32)

        with self.assertRaises(AttributeError):
            x = regs.register[1].data_type

if __name__ == "__main__":
    unittest.main()

    test = '''regs.find("TimerCtrl0").name
    regs.find("TimerCtrl1").name

    for reg in regs.register:
        print("{} /* {} */".format(reg.name, reg.description))
        print("Address offset: 0x{:08X}".format(reg.address_offset))
        print("Size: {:d}".format(reg.size))
        print("Access: {}".format(reg.access))
        print("Protection: {}".format(reg.protection))
        print("Reset value: 0x{:08X}".format(reg.reset_value))
        print("Reset mask: 0x{:08X}".format(reg.reset_mask))
        print("\n")'''
