import unittest
import xml.etree.ElementTree as ET

import svd.element
import svd.type

class case(unittest.TestCase):

    def test_exception(self):
        xml = '''<cpu />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            test = svd.element.cpu(None, node)

    def test_attributes(self):
        xml = '''
        <cpu>
            <name>CM7</name>
            <revision>r0p0</revision>
            <endian>little</endian>
            <mpuPresent>true</mpuPresent>

        <!-- has double precision FPU -->
            <fpuPresent>true</fpuPresent>
            <fpuDP>true</fpuDP>

        <!-- has instruction and data cache -->
            <icachePresent>true</icachePresent>
            <dcachePresent>true</dcachePresent>

        <!-- has no instruction nor data tighly coupled memory -->
            <itcmPresent>false</itcmPresent>
            <dtcmPresent>false</dtcmPresent>
            <nvicPrioBits>4</nvicPrioBits>
            <vendorSystickConfig>false</vendorSystickConfig>
        </cpu>'''
        node = ET.fromstring(xml)
        test = svd.element.cpu(None, node)

        self.assertEqual(test.name, svd.type.cpuName.CM7)
        self.assertEqual(test.revision, "r0p0")
        self.assertEqual(test.endian, svd.type.endian.little)
        self.assertTrue(test.mpu_present)
        self.assertTrue(test.fpu_present)
        self.assertTrue(test.fpu_dp)
        self.assertTrue(test.icache_present)
        self.assertTrue(test.dcache_present)
        self.assertFalse(test.itcm_present)
        self.assertFalse(test.dtcm_present)
        self.assertEqual(test.nvic_prio_bits, 4)
        self.assertFalse(test.vendor_systick_config)

        self.assertTrue(test.vtor_present)

        with self.assertRaises(AttributeError):
            self.assertIsNotNone(test.sau_num_regions)
