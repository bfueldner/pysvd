import unittest
import xml.etree.ElementTree as ET

from model import cpu
import type

class test_cpu(unittest.TestCase):
    def test_exception(self):
        svd = '''<cpu />'''
        node = ET.fromstring(svd)
        with self.assertRaises(SyntaxError):
            test = cpu(None, node)

    def test_attributes_default(self):
        svd = '''
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
        node = ET.fromstring(svd)
        test = cpu(None, node)

        self.assertEqual(test.name, type.cpu_name.cm7)
        self.assertEqual(test.revision, "r0p0")
        self.assertEqual(test.endian, type.endian.little)
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

if __name__ == "__main__":
    unittest.main()
