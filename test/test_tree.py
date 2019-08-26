import unittest
import xml.etree.ElementTree as ET

import pysvd


class TestTreeComplete(unittest.TestCase):

    # def setup()
    # use setup to parse file and separate tests to check deriveFrom, derive  Attribute and dim functionallity

    # TODO: Replace attribute names by names from XSD!!!

    def test_attributes(self):

        node = ET.parse("test/example.svd").getroot()
        test = pysvd.element.Device(node)

        self.assertEqual(test.schemaVersion, '1.1')

        self.assertEqual(test.vendor, 'ARM Ltd.')
        self.assertEqual(test.vendorID, 'ARM')
        self.assertEqual(test.name, 'ARM_Example')
        self.assertEqual(test.series, 'ARMCM3')
        self.assertEqual(test.version, '1.2')
        self.assertEqual(test.description, 'ARM 32-bit Cortex-M3 Microcontroller based device, CPU clock up to 80MHz, etc.')

        self.assertEqual(test.cpu.name, pysvd.type.cpuName.CM3)
        self.assertEqual(test.cpu.revision, 'r1p0')
        self.assertEqual(test.cpu.endian, pysvd.type.endian.little)
        self.assertTrue(test.cpu.mpuPresent)
        self.assertFalse(test.cpu.fpuPresent)
        self.assertEqual(test.cpu.nvicPrioBits, 3)
        self.assertFalse(test.cpu.vendorSystickConfig)

        self.assertEqual(test.addressUnitBits, 8)
        self.assertEqual(test.width, 32)
        self.assertEqual(test.size, 32)
        self.assertEqual(test.access, pysvd.type.access.read_write)
        self.assertEqual(test.resetValue, 0)
        self.assertEqual(test.resetMask, 0xffffffff)

        self.assertEqual(len(test.peripheral), 3)
        self.assertFalse(test.peripheral[0].derived)
        self.assertTrue(test.peripheral[1].derived)
        self.assertTrue(test.peripheral[2].derived)

        for peripheral in test.peripheral:
            self.assertEqual(peripheral.groupName, "TIMER")
            self.assertEqual(peripheral.addressBlock.offset, 0)
            self.assertEqual(peripheral.addressBlock.size, 0x100)
            self.assertEqual(peripheral.addressBlock.usage, pysvd.type.addressBlockUsage.registers)
            self.assertEqual(peripheral.resetValue, 0)

            self.assertEqual(len(peripheral.register), 8)
            print(peripheral.name)
