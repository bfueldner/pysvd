import unittest
import xml.etree.ElementTree as ET

import pysvd


class TestTreeComplete(unittest.TestCase):

    def test_attributes(self):

        node = ET.parse("test/example.svd").getroot()
        test = pysvd.element.Device(node)

        self.assertEqual(test.schema_version, '1.1')

        self.assertEqual(test.vendor, 'ARM Ltd.')
        self.assertEqual(test.vendor_id, 'ARM')
        self.assertEqual(test.name, 'ARM_Example')
        self.assertEqual(test.series, 'ARMCM3')
        self.assertEqual(test.version, '1.2')
        self.assertEqual(test.description, 'ARM 32-bit Cortex-M3 Microcontroller based device, CPU clock up to 80MHz, etc.')

        self.assertEqual(test.cpu.name, pysvd.type.cpuName.CM3)
        self.assertEqual(test.cpu.revision, 'r1p0')
        self.assertEqual(test.cpu.endian, pysvd.type.endian.little)
        self.assertTrue(test.cpu.mpu_present)
        self.assertFalse(test.cpu.fpu_present)
        self.assertEqual(test.cpu.nvic_prio_bits, 3)
        self.assertFalse(test.cpu.vendor_systick_config)

        self.assertEqual(test.address_unit_bits, 8)
        self.assertEqual(test.width, 32)
        self.assertEqual(test.size, 32)
        self.assertEqual(test.access, pysvd.type.access.read_write)
        self.assertEqual(test.reset_value, 0)
        self.assertEqual(test.reset_mask, 0xffffffff)

        self.assertEqual(len(test.peripheral), 3)
        self.assertFalse(test.peripheral[0].derived)
        self.assertTrue(test.peripheral[1].derived)
        self.assertTrue(test.peripheral[2].derived)

        for peripheral in test.peripheral:
            self.assertEqual(peripheral.group_name, "TIMER")
            self.assertEqual(peripheral.address_block.offset, 0)
            self.assertEqual(peripheral.address_block.size, 0x100)
            self.assertEqual(peripheral.address_block.usage, pysvd.type.usage.registers)
