import unittest
import xml.etree.ElementTree as ET

import svd.element
import svd.type

class case(unittest.TestCase):

    def test_complete(self):
        xml = '''
        <device schemaVersion="1.3" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xs:noNamespaceSchemaLocation="CMSIS-SVD.xsd">
            <vendor>ARM Ltd.</vendor>
            <vendorID>ARM</vendorID>
            <name>ARM_Cortex_M4</name>
            <series>ARMCM4</series>
            <version>0.1</version>
            <description>Arm Cortex-M4 based Microcontroller demonstration device</description>
            <licenseText>
                Arm Limited (Arm) is supplying this software for use with Cortex-M \n
                processor based microcontrollers.  This file can be freely distributed \n
                within development tools that are supporting such Arm based processors. \n
                \n
                THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED \n
                OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF \n
                MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. \n
                ARM SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR \n
                CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
            </licenseText>

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

                <sauRegionsConfig>
                    <region name="SAU1">
                        <base>0x10001000</base>
                        <limit>0x10005000</limit>
                        <access>n</access>
                    </region>
                    <region enabled="false" name="SAU2">
                        <base>0x10006000</base>
                        <limit>0x10008000</limit>
                        <access>c</access>
                    </region>
                </sauRegionsConfig>
            </cpu>

            <headerSystemFilename>system_ARMCM4</headerSystemFilename>
            <headerDefinitionsPrefix>ARM_</headerDefinitionsPrefix>
            <addressUnitBits>8</addressUnitBits>
            <width>32</width>
            <size>32</size>
            <access>read-write</access>
            <resetValue>0</resetValue>
            <resetMask>0xffffffff</resetMask>
            <peripherals>

            </peripherals>
        </device>'''
        node = ET.fromstring(xml)
        test = svd.element.device(node)

        self.assertEqual(test.schema_version, '1.3')

        self.assertEqual(test.vendor, 'ARM Ltd.')
        self.assertEqual(test.vendor_id, 'ARM')
        self.assertEqual(test.name, 'ARM_Cortex_M4')
        self.assertEqual(test.series, 'ARMCM4')
        self.assertEqual(test.version, '0.1')
        self.assertEqual(test.description, 'Arm Cortex-M4 based Microcontroller demonstration device')

        self.assertEqual(test.cpu.name, 'CM7')
        self.assertEqual(test.cpu.revision, 'r0p0')
        self.assertEqual(test.cpu.endian, svd.type.endian.little)
        self.assertTrue(test.cpu.mpu_present)
        self.assertTrue(test.cpu.fpu_present)
        self.assertTrue(test.cpu.fpu_dp)
        self.assertTrue(test.cpu.icache_present)
        self.assertTrue(test.cpu.dcache_present)
        self.assertFalse(test.cpu.itcm_present)
        self.assertFalse(test.cpu.dtcm_present)
        self.assertEqual(test.cpu.nvic_prio_bits, 4)
        self.assertFalse(test.cpu.vendor_systick_config)

        self.assertEqual(test.header_system_filename, 'system_ARMCM4')
        self.assertEqual(test.header_definitions_prefix, 'ARM_')
        self.assertEqual(test.address_unit_bits, 8)
        self.assertEqual(test.width, 32)

        self.assertEqual(test.size, 32)
        self.assertEqual(test.access, svd.type.access.read_write)
        self.assertEqual(test.reset_value, 0)
        self.assertEqual(test.reset_mask, 0xffffffff)

        self.assertEqual(len(test.peripheral), 0)
