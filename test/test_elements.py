import unittest
import xml.etree.ElementTree as ET

import pysvd


class TestElementDevice(unittest.TestCase):

    def test_required_exception(self):
        xml = '''<device />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Device(node)

    def test_peripherals_exception(self):
        xml = '''
        <device schemaVersion="1.3" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xs:noNamespaceSchemaLocation="CMSIS-SVD.xsd">
            <name>ARM_Cortex_M4</name>
            <version>0.1</version>
            <description>Arm Cortex-M4 based Microcontroller demonstration device</description>
            <addressUnitBits>8</addressUnitBits>
            <width>32</width>
        </device>'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Device(node)

    def test_peripheral_minimal_exception(self):
        xml = '''
        <device schemaVersion="1.3" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xs:noNamespaceSchemaLocation="CMSIS-SVD.xsd">
            <name>ARM_Cortex_M4</name>
            <version>0.1</version>
            <description>Arm Cortex-M4 based Microcontroller demonstration device</description>
            <addressUnitBits>8</addressUnitBits>
            <width>32</width>
            <peripherals />
        </device>'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Device(node)

    def test_attributes(self):
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

            <headerSystemFilename>system_ARMCM4</headerSystemFilename>
            <headerDefinitionsPrefix>ARM_</headerDefinitionsPrefix>
            <addressUnitBits>8</addressUnitBits>
            <width>32</width>
            <size>32</size>
            <access>read-write</access>
            <resetValue>0</resetValue>
            <resetMask>0xffffffff</resetMask>
            <peripherals>
                <peripheral>
                    <dim>2</dim>
                    <dimIncrement>0x200</dimIncrement>
                    <name>Timer%s</name>
                    <version>1.0</version>
                    <description>Timer %s is a standard timer ... </description>
                    <baseAddress>0x40002000</baseAddress>
                    <addressBlock>
                        <offset>0x0</offset>
                        <size>0x400</size>
                        <usage>registers</usage>
                        <protection>s</protection>
                    </addressBlock>
                    <interrupt>
                        <name>TIM0_INT</name>
                        <value>34</value>
                    </interrupt>
                </peripheral>
            </peripherals>
        </device>'''
        node = ET.fromstring(xml)
        test = pysvd.element.Device(node)

        self.assertEqual(test.schemaVersion, '1.3')

        self.assertEqual(test.vendor, 'ARM Ltd.')
        self.assertEqual(test.vendorID, 'ARM')
        self.assertEqual(test.name, 'ARM_Cortex_M4')
        self.assertEqual(test.series, 'ARMCM4')
        self.assertEqual(test.version, '0.1')
        self.assertEqual(test.description, 'Arm Cortex-M4 based Microcontroller demonstration device')
        self.assertEqual(test.headerSystemFilename, 'system_ARMCM4')
        self.assertEqual(test.headerDefinitionsPrefix, 'ARM_')
        self.assertEqual(test.addressUnitBits, 8)
        self.assertEqual(test.width, 32)
        self.assertEqual(test.size, 32)
        self.assertEqual(test.access, pysvd.type.access.read_write)
        self.assertEqual(test.resetValue, 0)
        self.assertEqual(test.resetMask, 0xffffffff)

        peripheral_index = 0
        self.assertEqual(len(test.peripherals), 2)
        for peripheral in test.peripherals:
            if peripheral_index == 0:
                self.assertEqual(peripheral.name, "Timer0")
                self.assertEqual(peripheral.description, "Timer 0 is a standard timer ...")
                self.assertEqual(peripheral.baseAddress, 0x40002000)

            elif peripheral_index == 1:
                self.assertEqual(peripheral.name, "Timer1")
                self.assertEqual(peripheral.description, "Timer 1 is a standard timer ...")
                self.assertEqual(peripheral.baseAddress, 0x40002200)

            self.assertEqual(peripheral.version, "1.0")

            self.assertEqual(len(peripheral.addressBlocks), 1)
            self.assertEqual(peripheral.addressBlocks[0].offset, 0)
            self.assertEqual(peripheral.addressBlocks[0].size, 0x400)
            self.assertEqual(peripheral.addressBlocks[0].usage, pysvd.type.addressBlockUsage.registers)
            self.assertEqual(peripheral.addressBlocks[0].protection, pysvd.type.protection.secure)

            self.assertEqual(len(peripheral.interrupts), 1)
            self.assertEqual(peripheral.interrupts[0].name, "TIM0_INT")
            self.assertEqual(peripheral.interrupts[0].value, 34)

            peripheral_index += 1

        self.assertIsNotNone(test.find("Timer0"))
        self.assertIsNotNone(test.find("Timer1"))
        self.assertIsNone(test.find("Timer2"))


class TestElementCpu(unittest.TestCase):

    def test_exception(self):
        xml = '''<cpu />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Cpu(None, node)

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

            <sauRegionsConfig>
                <region name="SAU1">
                    <base>0x10001000</base>
                    <limit>0x10005000</limit>
                    <access>n</access>
                </region>
            </sauRegionsConfig>
        </cpu>'''
        node = ET.fromstring(xml)
        test = pysvd.element.Cpu(None, node)

        self.assertEqual(test.name, pysvd.type.cpuName.CM7)
        self.assertEqual(test.revision, "r0p0")
        self.assertEqual(test.endian, pysvd.type.endian.little)
        self.assertTrue(test.mpuPresent)
        self.assertTrue(test.fpuPresent)
        self.assertTrue(test.fpuDP)
        self.assertTrue(test.icachePresent)
        self.assertTrue(test.dcachePresent)
        self.assertFalse(test.itcmPresent)
        self.assertFalse(test.dtcmPresent)
        self.assertEqual(test.nvicPrioBits, 4)
        self.assertFalse(test.vendorSystickConfig)
        self.assertTrue(test.vtorPresent)

        self.assertEqual(len(test.sauRegionsConfig.regions), 1)
        self.assertTrue(test.sauRegionsConfig.regions[0].enabled)
        self.assertEqual(test.sauRegionsConfig.regions[0].name, 'SAU1')
        self.assertEqual(test.sauRegionsConfig.regions[0].base, 0x10001000)
        self.assertEqual(test.sauRegionsConfig.regions[0].limit, 0x10005000)
        self.assertEqual(test.sauRegionsConfig.regions[0].access, pysvd.type.sauAccess.non_secure)


class TestElementSauRegionsConfig(unittest.TestCase):

    def test_empty(self):
        xml = '''<sauRegionsConfig />'''
        node = ET.fromstring(xml)
        test = pysvd.element.SauRegionConfig(None, node)

        self.assertEqual(len(test.regions), 0)

    def test_attributes(self):
        xml = '''
        <sauRegionsConfig enabled="true" protectionWhenDisabled="n">
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
        </sauRegionsConfig>'''
        node = ET.fromstring(xml)
        test = pysvd.element.SauRegionConfig(None, node)

        self.assertTrue(test.enabled)
        self.assertEqual(test.protectionWhenDisabled, pysvd.type.protection.non_secure)

        self.assertEqual(len(test.regions), 2)
        self.assertTrue(test.regions[0].enabled)
        self.assertEqual(test.regions[0].name, 'SAU1')
        self.assertEqual(test.regions[0].base, 0x10001000)
        self.assertEqual(test.regions[0].limit, 0x10005000)
        self.assertEqual(test.regions[0].access, pysvd.type.sauAccess.non_secure)
        self.assertFalse(test.regions[1].enabled)
        self.assertEqual(test.regions[1].name, 'SAU2')
        self.assertEqual(test.regions[1].base, 0x10006000)
        self.assertEqual(test.regions[1].limit, 0x10008000)
        self.assertEqual(test.regions[1].access, pysvd.type.sauAccess.non_secure_callable_secure)


class TestElementSauRegionsConfigRegion(unittest.TestCase):

    def test_exception(self):
        xml = '''<region />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.SauRegionsConfigRegion(None, node)

    def test_attributes(self):
        xml = '''
        <region enabled="false" name="SAU2">
            <base>0x10006000</base>
            <limit>0x10008000</limit>
            <access>c</access>
        </region>'''
        node = ET.fromstring(xml)
        test = pysvd.element.SauRegionsConfigRegion(None, node)

        self.assertEqual(test.base, 0x10006000)
        self.assertEqual(test.limit, 0x10008000)
        self.assertEqual(test.access, pysvd.type.sauAccess.non_secure_callable_secure)

        self.assertEqual(test.name, "SAU2")
        self.assertFalse(test.enabled)


class TestElementPeripheral(unittest.TestCase):

    def test_required_exception(self):
        xml = '''<peripheral />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Peripheral(None, node)

    def test_register_cluster_exception(self):
        xml = '''
        <peripheral>
            <name>Timer1</name>
            <baseAddress>0x40002000</baseAddress>
            <registers />
        </peripheral>'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Peripheral(None, node)

    def test_attributes(self):
        xml = '''
        <peripheral>
            <name>Timer1</name>
            <version>1.0</version>
            <description>Timer 1 is a standard timer ... </description>
            <baseAddress>0x40002000</baseAddress>
            <addressBlock>
                <offset>0x0</offset>
                <size>0x400</size>
                <usage>registers</usage>
                <protection>s</protection>
            </addressBlock>
            <addressBlock>
                <offset>0x400</offset>
                <size>0x800</size>
                <usage>registers</usage>
            </addressBlock>
            <interrupt>
                <name>TIM0_INT</name>
                <value>34</value>
            </interrupt>
            <interrupt>
                <name>TIM1_INT</name>
                <value>35</value>
            </interrupt>
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
                <register>
                    <dim>2</dim>
                    <dimIncrement>4</dimIncrement>
                    <name>Value%s</name>
                    <addressOffset>0x8</addressOffset>
                </register>
                <cluster>
                    <dim>2</dim>
                    <dimIncrement>0x8</dimIncrement>
                    <name>Mode%s</name>
                    <addressOffset>0x10</addressOffset>
                </cluster>
            </registers>
        </peripheral>'''
        node = ET.fromstring(xml)
        test = pysvd.element.Peripheral(None, node)

        self.assertEqual(test.name, "Timer1")
        self.assertEqual(test.version, "1.0")
        self.assertEqual(test.description, "Timer 1 is a standard timer ...")
        self.assertEqual(test.baseAddress, 0x40002000)

        self.assertEqual(len(test.addressBlocks), 2)
        self.assertEqual(test.addressBlocks[0].offset, 0)
        self.assertEqual(test.addressBlocks[0].size, 0x400)
        self.assertEqual(test.addressBlocks[0].usage, pysvd.type.addressBlockUsage.registers)
        self.assertEqual(test.addressBlocks[0].protection, pysvd.type.protection.secure)
        self.assertEqual(test.addressBlocks[1].offset, 0x400)
        self.assertEqual(test.addressBlocks[1].size, 0x800)
        self.assertEqual(test.addressBlocks[1].usage, pysvd.type.addressBlockUsage.registers)

        self.assertEqual(len(test.interrupts), 2)
        self.assertEqual(test.interrupts[0].name, "TIM0_INT")
        self.assertEqual(test.interrupts[0].value, 34)
        self.assertEqual(test.interrupts[1].name, "TIM1_INT")
        self.assertEqual(test.interrupts[1].value, 35)

        self.assertEqual(len(test.registers), 4)
        self.assertEqual(test.registers[0].name, "TimerCtrl0")
        self.assertEqual(test.registers[0].description, "Timer Control Register")
        self.assertEqual(test.registers[0].addressOffset, 0)
        self.assertEqual(test.registers[0].access, pysvd.type.access.read_write)
        self.assertEqual(test.registers[0].resetValue, 0x00008001)
        self.assertEqual(test.registers[0].resetMask, 0x0000ffff)
        self.assertEqual(test.registers[0].size, 32)
        self.assertEqual(test.registers[1].name, "TimerCtrl1")
        self.assertEqual(test.registers[1].description, "Derived Timer")
        self.assertEqual(test.registers[1].addressOffset, 4)
        self.assertEqual(test.registers[1].access, pysvd.type.access.read_write)
        self.assertEqual(test.registers[1].resetValue, 0x00008001)
        self.assertEqual(test.registers[1].resetMask, 0x0000ffff)
        self.assertEqual(test.registers[1].size, 32)
        self.assertEqual(test.registers[2].name, "Value0")
        self.assertEqual(test.registers[2].addressOffset, 8)
        self.assertEqual(test.registers[3].name, "Value1")
        self.assertEqual(test.registers[3].addressOffset, 12)

        self.assertEqual(len(test.clusters), 2)
        self.assertEqual(test.clusters[0].name, "Mode0")
        self.assertEqual(test.clusters[0].addressOffset, 0x10)
        self.assertEqual(test.clusters[1].name, "Mode1")
        self.assertEqual(test.clusters[1].addressOffset, 0x18)

        self.assertIsNotNone(test.find("Mode0"))
        self.assertIsNotNone(test.find("Mode1"))
        self.assertIsNotNone(test.find("TimerCtrl0"))
        self.assertIsNotNone(test.find("TimerCtrl1"))
        self.assertIsNone(test.find("TimerCtrl2"))


class TestElementAddressBlock(unittest.TestCase):

    def test_exception(self):
        xml = '''<addressBlock />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.AddressBlock(None, node)

    def test_attributes(self):
        xml = '''
        <addressBlock>
            <offset>0x0</offset>
            <size>0x400</size>
            <usage>registers</usage>
            <protection>s</protection>
        </addressBlock>
        '''
        node = ET.fromstring(xml)
        test = pysvd.element.AddressBlock(None, node)

        self.assertEqual(test.offset, 0)
        self.assertEqual(test.size, 0x400)
        self.assertEqual(test.usage, pysvd.type.addressBlockUsage.registers)
        self.assertEqual(test.protection, pysvd.type.protection.secure)


class TestElementInterrupt(unittest.TestCase):

    def test_exception(self):
        xml = '''<interrupt />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Interrupt(None, node)

    def test_attributes(self):
        xml = '''
        <interrupt>
            <name>TIM0_INT</name>
            <value>34</value>
            <description>Timer0 Interrupt</description>
        </interrupt>
        '''
        node = ET.fromstring(xml)
        test = pysvd.element.Interrupt(None, node)

        self.assertEqual(test.name, 'TIM0_INT')
        self.assertEqual(test.description, 'Timer0 Interrupt')
        self.assertEqual(test.value, 34)


class TestElementCluster(unittest.TestCase):

    def test_exception(self):
        xml = '''<cluster />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Register(None, node)

    def test_attributes(self):
        xml = '''
        <registers>
            <name>Timer1</name>
            <addressOffset>0x1000</addressOffset>
            <cluster>
                <name>MODE0</name>
                <addressOffset>0x0</addressOffset>
                <register>
                    <name>CTRL</name>
                    <addressOffset>0x00</addressOffset>
                </register>
                <register>
                    <name>READREQ</name>
                    <addressOffset>0x02</addressOffset>
                </register>
                <cluster>
                    <name>SUBMODE</name>
                    <addressOffset>0x10</addressOffset>
                </cluster>
            </cluster>
        </registers>'''
        node = ET.fromstring(xml)
        test = pysvd.element.Cluster(None, node)

        self.assertEqual(len(test.clusters), 1)
        self.assertEqual(test.clusters[0].name, "MODE0")
        self.assertEqual(test.clusters[0].addressOffset, 0)

        cluster = test.clusters[0]
        self.assertEqual(len(cluster.registers), 2)
        self.assertEqual(cluster.registers[0].name, "CTRL")
        self.assertEqual(cluster.registers[0].addressOffset, 0)
        self.assertEqual(cluster.registers[1].name, "READREQ")
        self.assertEqual(cluster.registers[1].addressOffset, 2)

        self.assertEqual(len(cluster.clusters), 1)
        self.assertEqual(cluster.clusters[0].name, "SUBMODE")
        self.assertEqual(cluster.clusters[0].addressOffset, 16)

        self.assertIsNotNone(cluster.find('CTRL'))
        self.assertIsNotNone(cluster.find('READREQ'))
        self.assertIsNotNone(cluster.find('SUBMODE'))
        self.assertIsNone(cluster.find('VALUE'))


class TestElementRegister(unittest.TestCase):

    def test_required_exception(self):
        xml = '''<register />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Register(None, node)

    def test_fields_exception(self):
        xml = '''
        <register>
            <name>TimerCtrl0</name>
            <addressOffset>0x0</addressOffset>
            <fields />
        </register>
        '''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Register(None, node)

    def test_attributes(self):
        xml = '''
        <register>
            <name>TimerCtrl0</name>
            <description>Timer Control Register</description>
            <addressOffset>0x0</addressOffset>
            <access>read-write</access>
            <resetValue>0x00008001</resetValue>
            <resetMask>0x0000ffff</resetMask>
            <size>32</size>
            <writeConstraint>
                <writeAsRead>true</writeAsRead>
            </writeConstraint>
            <fields>
                <field>
                    <dim>2</dim>
                    <dimIncrement>3</dimIncrement>
                    <name>BIT%s</name>
                    <bitOffset>1</bitOffset>
                    <bitWidth>3</bitWidth>
                </field>
            </fields>
        </register>
        '''

        node = ET.fromstring(xml)
        test = pysvd.element.Register(None, node)

        self.assertEqual(test.name, "TimerCtrl0")
        self.assertEqual(test.description, "Timer Control Register")
        self.assertEqual(test.addressOffset, 0)
        self.assertEqual(test.access, pysvd.type.access.read_write)
        self.assertEqual(test.resetValue, 0x00008001)
        self.assertEqual(test.resetMask, 0x0000ffff)
        self.assertEqual(test.size, 32)

        self.assertIsNotNone(test.writeConstraint)

        self.assertEqual(len(test.fields), 2)
        self.assertEqual(test.fields[0].name, "BIT0")
        self.assertEqual(test.fields[0].bitOffset, 1)
        self.assertEqual(test.fields[0].bitWidth, 3)
        self.assertEqual(test.fields[1].name, "BIT1")
        self.assertEqual(test.fields[1].bitOffset, 4)
        self.assertEqual(test.fields[1].bitWidth, 3)

        self.assertIsNotNone(test.find("BIT0"))
        self.assertIsNotNone(test.find("BIT1"))
        self.assertIsNone(test.find("BIT2"))


class TestElementWriteConstraint(unittest.TestCase):

    def test_exception(self):
        xml = '''<writeConstraint />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.WriteConstraint(None, node)

    def test_writeAsRead(self):
        xml = '''
        <writeConstraint>
            <writeAsRead>true</writeAsRead>
        </writeConstraint>
        '''

        node = ET.fromstring(xml)
        test = pysvd.element.WriteConstraint(None, node)

        self.assertTrue(test.writeAsRead)

    def test_useEnumeratedValues(self):
        xml = '''
        <writeConstraint>
            <useEnumeratedValues>true</useEnumeratedValues>
        </writeConstraint>
        '''

        node = ET.fromstring(xml)
        test = pysvd.element.WriteConstraint(None, node)

        self.assertTrue(test.useEnumeratedValues)

    def test_range(self):
        xml = '''
        <writeConstraint>
            <range>
                <minimum>2</minimum>
                <maximum>4</maximum>
            </range>
        </writeConstraint>
        '''

        node = ET.fromstring(xml)
        test = pysvd.element.WriteConstraint(None, node)

        self.assertEqual(test.rangeMinimum, 2)
        self.assertEqual(test.rangeMaximum, 4)


class TestElementField(unittest.TestCase):

    def test_required_exception(self):
        xml = '''<field />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Field(None, node)

    def test_bitrange_exception(self):
        xml = '''
        <field>
            <name>BIT1</name>
        </field>'''
        node = ET.fromstring(xml)
        with self.assertRaises(ValueError):
            pysvd.element.Field(None, node)

    def test_bit_range_offset(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <bitOffset>4</bitOffset>
        </field>'''

        node = ET.fromstring(xml)
        test = pysvd.element.Field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bitOffset, 4)
        self.assertEqual(test.bitWidth, 1)

    def test_bit_range_offset_width(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <bitOffset>5</bitOffset>
            <bitWidth>3</bitWidth>
        </field>'''

        node = ET.fromstring(xml)
        test = pysvd.element.Field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bitOffset, 5)
        self.assertEqual(test.bitWidth, 3)

    def test_bit_range_lsb_msb(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <lsb>16</lsb>
            <msb>31</msb>
        </field>'''

        node = ET.fromstring(xml)
        test = pysvd.element.Field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bitOffset, 16)
        self.assertEqual(test.bitWidth, 16)

    def test_bit_range_pattern(self):
        xml = '''
        <field>
            <name>BIT1</name>
            <bitRange>[7:4]</bitRange>
        </field>'''

        node = ET.fromstring(xml)
        test = pysvd.element.Field(None, node)

        self.assertEqual(test.name, "BIT1")
        self.assertEqual(test.bitOffset, 4)
        self.assertEqual(test.bitWidth, 4)

    def test_attributes(self):
        xml = '''
        <field>
            <name>TimerCtrl0_IntSel</name>
            <description>Select interrupt line that is triggered by timer overflow.</description>
            <bitOffset>1</bitOffset>
            <bitWidth>3</bitWidth>
            <access>read-write</access>
            <modifiedWriteValues>oneToSet</modifiedWriteValues>
            <writeConstraint>
                <range>
                    <minimum>0</minimum>
                    <maximum>5</maximum>
                </range>
            </writeConstraint>
            <enumeratedValues>
                <name>TimerIntSelect</name>
                <enumeratedValue>
                    <name>disabled</name>
                    <value>0</value>
                </enumeratedValue>
            </enumeratedValues>
            <readAction>clear</readAction>
        </field>'''

        node = ET.fromstring(xml)
        test = pysvd.element.Field(None, node)

        self.assertEqual(test.name, "TimerCtrl0_IntSel")
        self.assertEqual(test.description, "Select interrupt line that is triggered by timer overflow.")
        self.assertEqual(test.bitOffset, 1)
        self.assertEqual(test.bitWidth, 3)

        self.assertEqual(test.access, pysvd.type.access.read_write)
        self.assertEqual(test.modifiedWriteValues, pysvd.type.modifiedWriteValues.oneToSet)
        self.assertEqual(test.readAction, pysvd.type.readAction.clear)

        self.assertIsNotNone(test.writeConstraint)
        self.assertEqual(test.writeConstraint.rangeMinimum, 0)
        self.assertEqual(test.writeConstraint.rangeMaximum, 5)

        self.assertIsNotNone(test.enumeratedValues)
        self.assertEqual(len(test.enumeratedValues.enumeratedValues), 1)

        self.assertIsNotNone(test.find("TimerIntSelect"))
        self.assertIsNone(test.find("TimerMode"))


class TestElementEnumberatedValues(unittest.TestCase):

    def test_exception(self):
        xml = '''<enumeratedValues />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.EnumeratedValues(None, node)

    def test_minimal(self):
        xml = '''
        <enumeratedValues>
            <enumeratedValue>
                <value>0</value>
            </enumeratedValue>
        </enumeratedValues>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValues(None, node)

        self.assertEqual(test.usage, pysvd.type.enumUsage.read_write)

        self.assertEqual(len(test.enumeratedValues), 1)
        self.assertEqual(test.enumeratedValues[0].value, 0)

    def test_attributes(self):
        xml = '''
        <enumeratedValues>
            <name>TimerIntSelect</name>
            <headerEnumName>TimerIntSelectEnum</headerEnumName>
            <usage>read-write</usage>
            <enumeratedValue>
                <name>disabled</name>
                <description>The clock source clk0 is turned off.</description>
                <value>0</value>
            </enumeratedValue>
            <enumeratedValue>
                <name>enabled</name>
                <description>The clock source clk1 is running.</description>
                <value>1</value>
            </enumeratedValue>
            <enumeratedValue>
                <name>reserved</name>
                <description>Reserved values. Do not use.</description>
                <isDefault>true</isDefault>
            </enumeratedValue>
        </enumeratedValues>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValues(None, node)

        self.assertEqual(test.name, "TimerIntSelect")
        self.assertEqual(test.headerEnumName, "TimerIntSelectEnum")
        self.assertEqual(test.usage, pysvd.type.enumUsage.read_write)

        self.assertEqual(len(test.enumeratedValues), 3)
        self.assertEqual(test.enumeratedValues[0].name, "disabled")
        self.assertEqual(test.enumeratedValues[0].description, "The clock source clk0 is turned off.")
        self.assertEqual(test.enumeratedValues[0].value, 0)
        self.assertEqual(test.enumeratedValues[1].name, "enabled")
        self.assertEqual(test.enumeratedValues[1].description, "The clock source clk1 is running.")
        self.assertEqual(test.enumeratedValues[1].value, 1)
        self.assertEqual(test.enumeratedValues[2].name, "reserved")
        self.assertEqual(test.enumeratedValues[2].description, "Reserved values. Do not use.")
        self.assertTrue(test.enumeratedValues[2].isDefault)


class TestElementEnumberatedValue(unittest.TestCase):

    def test_exception(self):
        xml = '''<enumeratedValue />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.EnumeratedValue(None, node)

    def test_minimal(self):
        xml = '''
        <enumeratedValue>
            <value>0</value>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValue(None, node)

        self.assertEqual(test.value, 0)

    def test_attributes_value(self):
        xml = '''
        <enumeratedValue>
            <name>disabled</name>
            <description>The clock source clk0 is turned off.</description>
            <value>0</value>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValue(None, node)

        self.assertEqual(test.name, "disabled")
        self.assertEqual(test.description, "The clock source clk0 is turned off.")
        self.assertEqual(test.value, 0)

        with self.assertRaises(AttributeError):
            self.assertIsNone(test.isDefault)

    def test_attributes_isDefault(self):
        xml = '''
        <enumeratedValue>
            <name>reserved</name>
            <description>Reserved values. Do not use.</description>
            <isDefault>true</isDefault>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValue(None, node)

        self.assertEqual(test.name, "reserved")
        self.assertEqual(test.description, "Reserved values. Do not use.")
        self.assertTrue(test.isDefault)

        with self.assertRaises(AttributeError):
            self.assertIsNone(test.value)


class TestElementDimArrayIndex(unittest.TestCase):

    def test_exception(self):
        xml = '''<dimArrayIndex />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.DimArrayIndex(None, node)

    def test_attributes(self):
        xml = '''
        <dimArrayIndex>
            <headerEnumName>FSMC_EnumArray</headerEnumName>
            <enumeratedValue>
                <name>UART0</name>
                <description>UART0 Peripheral</description>
                <value>0</value>
            </enumeratedValue>
            <enumeratedValue>
                <name>TIMER0</name>
                <description>TIMER0 Peripheral</description>
                <value>1</value>
            </enumeratedValue>
        </dimArrayIndex>'''

        node = ET.fromstring(xml)
        test = pysvd.element.DimArrayIndex(None, node)

        self.assertEqual(test.headerEnumName, "FSMC_EnumArray")
        self.assertEqual(len(test.enumeratedValues), 2)
        self.assertEqual(test.enumeratedValues[0].name, "UART0")
        self.assertEqual(test.enumeratedValues[0].description, "UART0 Peripheral")
        self.assertEqual(test.enumeratedValues[0].value, 0)
        self.assertEqual(test.enumeratedValues[1].name, "TIMER0")
        self.assertEqual(test.enumeratedValues[1].description, "TIMER0 Peripheral")
        self.assertEqual(test.enumeratedValues[1].value, 1)
