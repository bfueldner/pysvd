import unittest
import xml.etree.ElementTree as ET

from model import register
from model import registers
import type

class test_register_derive(unittest.TestCase):

    def setUp(self):
        self.node = ET.parse("res/" + __name__ + ".svd").getroot()

    def test_register_count(self):
        regs = registers(None, self.node)
        self.assertEqual(len(regs.register), 2)

    def test_register_timer_ctrl0(self):
        regs = registers(None, self.node)
        self.assertEqual(regs.register[0].name, "TimerCtrl0")
        self.assertEqual(regs.register[0].description, "Timer Control Register")
        self.assertEqual(regs.register[0].address_offset, 0x00)

        self.assertEqual(regs.register[0].access, type.access.read_write)
        self.assertEqual(regs.register[0].reset_value, 0x00008001)
        self.assertEqual(regs.register[0].reset_mask, 0x0000ffff)
        self.assertEqual(regs.register[0].size, 32)

        with self.assertRaises(AttributeError):
            x = regs.register[0].protection

    def test_register_timer_ctrl1(self):
        regs = registers(None, self.node)
        self.assertEqual(regs.register[1].name, "TimerCtrl1")
        self.assertEqual(regs.register[1].description, "Derived Timer")
        self.assertEqual(regs.register[1].address_offset, 0x04)

        self.assertEqual(regs.register[1].access, type.access.read_write)
        self.assertEqual(regs.register[1].reset_value, 0x00008001)
        self.assertEqual(regs.register[1].reset_mask, 0x0000ffff)
        self.assertEqual(regs.register[1].size, 32)

        with self.assertRaises(AttributeError):
            x = regs.register[1].protection

if __name__ == "__main__":
    unittest.main()
