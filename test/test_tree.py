import unittest
import xml.etree.ElementTree as ET

import pysvd


class TestTreeComplete(unittest.TestCase):

    # def setup()
    # use setup to parse file and separate tests to check deriveFrom, derive  Attribute and dim functionallity

    @classmethod
    def setUpClass(cls):
        node = ET.parse("test/example.svd").getroot()
        cls.device = pysvd.element.Device(node)

    def test_device_attributes(self):
        device = self.device

        self.assertEqual(device.schemaVersion, '1.1')
        self.assertEqual(device.vendor, 'ARM Ltd.')
        self.assertEqual(device.vendorID, 'ARM')
        self.assertEqual(device.name, 'ARM_Example')
        self.assertEqual(device.series, 'ARMCM3')
        self.assertEqual(device.version, '1.2')
        self.assertEqual(device.description, 'ARM 32-bit Cortex-M3 Microcontroller based device, CPU clock up to 80MHz, etc.')
        self.assertEqual(device.addressUnitBits, 8)
        self.assertEqual(device.width, 32)
        self.assertEqual(device.size, 32)
        self.assertEqual(device.access, pysvd.type.access.read_write)
        self.assertEqual(device.resetValue, 0)
        self.assertEqual(device.resetMask, 0xffffffff)

    def test_cpu_attributes(self):
        cpu = self.device.cpu

        self.assertEqual(cpu.name, pysvd.type.cpuName.CM3)
        self.assertEqual(cpu.revision, 'r1p0')
        self.assertEqual(cpu.endian, pysvd.type.endian.little)
        self.assertTrue(cpu.mpuPresent)
        self.assertFalse(cpu.fpuPresent)
        self.assertEqual(cpu.nvicPrioBits, 3)
        self.assertFalse(cpu.vendorSystickConfig)

    def test_peripheral_equal_attributes(self):
        device = self.device

        self.assertEqual(len(device.peripherals), 3)
        for peripheral in device.peripherals:
            # general
            self.assertEqual(peripheral.version, "1.0")
            self.assertEqual(peripheral.size, 32)
            self.assertEqual(peripheral.access, pysvd.type.access.read_write)
            self.assertEqual(peripheral.groupName, "TIMER")

            # inherited
            self.assertEqual(peripheral.resetValue, 0x00000000)
            self.assertEqual(peripheral.resetMask, 0xffffffff)

            # addressBlock
            self.assertEqual(len(peripheral.addressBlocks), 1)
            self.assertEqual(peripheral.addressBlocks[0].offset, 0)
            self.assertEqual(peripheral.addressBlocks[0].size, 0x100)
            self.assertEqual(peripheral.addressBlocks[0].usage, pysvd.type.addressBlockUsage.registers)

    def test_peripheral_derivedFrom_attributes(self):
        device = self.device

        peripheral_index = 0
        self.assertEqual(len(device.peripherals), 3)
        for peripheral in device.peripherals:
            if peripheral_index == 0:
                # general
                self.assertEqual(peripheral.name, "TIMER0")
                self.assertEqual(peripheral.description, "32 Timer / Counter, counting up or down from different sources")
                self.assertEqual(peripheral.baseAddress, 0x40010000)
                self.assertIsNone(peripheral.derivedFrom)

                # interrupt
                self.assertEqual(len(peripheral.interrupts), 1)
                self.assertEqual(peripheral.interrupts[0].name, "TIMER0")
                self.assertEqual(peripheral.interrupts[0].description, "Timer 0 interrupt")
                self.assertEqual(peripheral.interrupts[0].value, 0)

            elif peripheral_index == 1:
                # general
                self.assertEqual(peripheral.name, "TIMER1")
                self.assertEqual(peripheral.description, "32 Timer / Counter, counting up or down from different sources")
                self.assertEqual(peripheral.baseAddress, 0x40010100)
                self.assertEqual(peripheral.derivedFrom, device.peripherals[0])

                # interrupt
                self.assertEqual(len(peripheral.interrupts), 1)
                self.assertEqual(peripheral.interrupts[0].name, "TIMER1")
                self.assertEqual(peripheral.interrupts[0].description, "Timer 1 interrupt")
                self.assertEqual(peripheral.interrupts[0].value, 4)

            elif peripheral_index == 2:
                # general
                self.assertEqual(peripheral.name, "TIMER2")
                self.assertEqual(peripheral.description, "32 Timer / Counter, counting up or down from different sources")
                self.assertEqual(peripheral.baseAddress, 0x40010200)
                self.assertEqual(peripheral.derivedFrom, device.peripherals[0])

                # interrupt
                self.assertEqual(len(peripheral.interrupts), 1)
                self.assertEqual(peripheral.interrupts[0].name, "TIMER2")
                self.assertEqual(peripheral.interrupts[0].description, "Timer 2 interrupt")
                self.assertEqual(peripheral.interrupts[0].value, 6)

            # registers
            register_index = 0
            self.assertEqual(len(peripheral.registers), 8)
            for register in peripheral.registers:
                if register_index == 0:
                    self.assertEqual(register.name, "CR")
                    self.assertEqual(register.description, "Control Register")
                    self.assertEqual(register.addressOffset, 0)
                    self.assertEqual(register.size, 32)
                    self.assertEqual(register.access, pysvd.type.access.read_write)
                    self.assertEqual(register.resetValue, 0x00000000)
                    self.assertEqual(register.resetMask, 0x1337f7f)

                    # fields
                    field_index = 0
                    self.assertEqual(len(register.fields), 12)
                    for field in register.fields:
                        if field_index == 0:
                            self.assertEqual(field.name, "EN")
                            self.assertEqual(field.description, "Enable")
                            self.assertEqual(field.bitOffset, 0)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Disable")
                                    self.assertEqual(enumeratedValue.description, "Timer is disabled and does not operate")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Enable")
                                    self.assertEqual(enumeratedValue.description, "Timer is enabled and can operate")
                                    self.assertEqual(enumeratedValue.value, 1)
                                enumeratedValue_index += 1

                        elif field_index == 1:
                            self.assertEqual(field.name, "RST")
                            self.assertEqual(field.description, "Reset Timer")
                            self.assertEqual(field.bitOffset, 1)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.write_only)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "No_Action")
                                    self.assertEqual(enumeratedValue.description, "Write as ZERO if necessary")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Reset_Timer")
                                    self.assertEqual(enumeratedValue.description, "Reset the Timer")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 2:
                            self.assertEqual(field.name, "CNT")
                            self.assertEqual(field.description, "Counting direction")
                            self.assertEqual(field.bitOffset, 2)
                            self.assertEqual(field.bitWidth, 2)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 3)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Count_UP")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer Counts UO and wraps, if no STOP condition is set")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Count_DOWN")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer Counts DOWN and wraps, if no STOP condition is set")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "Toggle")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer Counts up to MAX, then DOWN to ZERO, if no STOP condition is set")
                                    self.assertEqual(enumeratedValue.value, 2)

                                enumeratedValue_index += 1

                        elif field_index == 3:
                            self.assertEqual(field.name, "MODE")
                            self.assertEqual(field.description, "Operation Mode")
                            self.assertEqual(field.bitOffset, 4)
                            self.assertEqual(field.bitWidth, 3)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 5)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Continous")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer runs continously")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Single_ZERO_MAX")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer counts to 0x00 or 0xFFFFFFFF (depending on CNT) and stops")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "Single_MATCH")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer counts to the Value of MATCH Register and stops")
                                    self.assertEqual(enumeratedValue.value, 2)

                                elif enumeratedValue_index == 3:
                                    self.assertEqual(enumeratedValue.name, "Reload_ZERO_MAX")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer counts to 0x00 or 0xFFFFFFFF (depending on CNT), loads the RELOAD Value and continues")
                                    self.assertEqual(enumeratedValue.value, 3)

                                elif enumeratedValue_index == 4:
                                    self.assertEqual(enumeratedValue.name, "Reload_MATCH")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer counts to the Value of MATCH Register, loads the RELOAD Value and continues")
                                    self.assertEqual(enumeratedValue.value, 4)

                                enumeratedValue_index += 1

                        elif field_index == 4:
                            self.assertEqual(field.name, "PSC")
                            self.assertEqual(field.description, "Use Prescaler")
                            self.assertEqual(field.bitOffset, 7)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Disabled")
                                    self.assertEqual(enumeratedValue.description, "Prescaler is not used")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Enabled")
                                    self.assertEqual(enumeratedValue.description, "Prescaler is used as divider")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 5:
                            self.assertEqual(field.name, "CNTSRC")
                            self.assertEqual(field.description, "Timer / Counter Source Divider")
                            self.assertEqual(field.bitOffset, 8)
                            self.assertEqual(field.bitWidth, 4)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 9)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is used directly")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div2")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 2")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div4")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 4")
                                    self.assertEqual(enumeratedValue.value, 2)

                                elif enumeratedValue_index == 3:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div8")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 8")
                                    self.assertEqual(enumeratedValue.value, 3)

                                elif enumeratedValue_index == 4:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div16")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 16")
                                    self.assertEqual(enumeratedValue.value, 4)

                                elif enumeratedValue_index == 5:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div32")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 32")
                                    self.assertEqual(enumeratedValue.value, 5)

                                elif enumeratedValue_index == 6:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div64")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 64")
                                    self.assertEqual(enumeratedValue.value, 6)

                                elif enumeratedValue_index == 7:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div128")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 128")
                                    self.assertEqual(enumeratedValue.value, 7)

                                elif enumeratedValue_index == 8:
                                    self.assertEqual(enumeratedValue.name, "CAP_SRC_div256")
                                    self.assertEqual(enumeratedValue.description, "Capture Source is divided by 256")
                                    self.assertEqual(enumeratedValue.value, 8)

                                enumeratedValue_index += 1

                        elif field_index == 6:
                            self.assertEqual(field.name, "CAPSRC")
                            self.assertEqual(field.description, "Timer / Counter Capture Source")
                            self.assertEqual(field.bitOffset, 12)
                            self.assertEqual(field.bitWidth, 4)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 16)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "CClk")
                                    self.assertEqual(enumeratedValue.description, "Core Clock")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "GPIOA_0")
                                    self.assertEqual(enumeratedValue.description, "GPIO A, PIN 0")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 15:
                                    self.assertEqual(enumeratedValue.name, "GPIOC_6")
                                    self.assertEqual(enumeratedValue.description, "GPIO C, PIN 2")
                                    self.assertEqual(enumeratedValue.value, 15)

                                enumeratedValue_index += 1

                        elif field_index == 7:
                            self.assertEqual(field.name, "CAPEDGE")
                            self.assertEqual(
                                field.description,
                                "Capture Edge, select which Edge should result in a counter increment or decrement")
                            self.assertEqual(field.bitOffset, 16)
                            self.assertEqual(field.bitWidth, 2)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 3)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "RISING")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Only rising edges result in a counter increment or decrement")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "FALLING")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Only falling edges result in a counter increment or decrement")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "BOTH")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Rising and falling edges result in a counter increment or decrement")
                                    self.assertEqual(enumeratedValue.value, 2)

                                enumeratedValue_index += 1

                        elif field_index == 8:
                            self.assertEqual(field.name, "TRGEXT")
                            self.assertEqual(field.description, "Triggers an other Peripheral")
                            self.assertEqual(field.bitOffset, 20)
                            self.assertEqual(field.bitWidth, 2)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 4)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "NONE")
                                    self.assertEqual(enumeratedValue.description, "No Trigger is emitted")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "DMA1")
                                    self.assertEqual(enumeratedValue.description, "DMA Controller 1 is triggered, dependant on MODE")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "DMA2")
                                    self.assertEqual(enumeratedValue.description, "DMA Controller 2 is triggered, dependant on MODE")
                                    self.assertEqual(enumeratedValue.value, 2)

                                elif enumeratedValue_index == 3:
                                    self.assertEqual(enumeratedValue.name, "UART")
                                    self.assertEqual(enumeratedValue.description, "UART is triggered, dependant on MODE")
                                    self.assertEqual(enumeratedValue.value, 3)

                                enumeratedValue_index += 1

                        elif field_index == 9:
                            self.assertEqual(field.name, "RELOAD")
                            self.assertEqual(field.description, "Select RELOAD Register n to reload Timer on condition")
                            self.assertEqual(field.bitOffset, 24)
                            self.assertEqual(field.bitWidth, 2)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 4)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "RELOAD0")
                                    self.assertEqual(enumeratedValue.description, "Selects Reload Register number 0")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "RELOAD1")
                                    self.assertEqual(enumeratedValue.description, "Selects Reload Register number 1")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "RELOAD2")
                                    self.assertEqual(enumeratedValue.description, "Selects Reload Register number 2")
                                    self.assertEqual(enumeratedValue.value, 2)

                                elif enumeratedValue_index == 3:
                                    self.assertEqual(enumeratedValue.name, "RELOAD3")
                                    self.assertEqual(enumeratedValue.description, "Selects Reload Register number 3")
                                    self.assertEqual(enumeratedValue.value, 3)

                                enumeratedValue_index += 1

                        elif field_index == 10:
                            self.assertEqual(field.name, "IDR")
                            self.assertEqual(
                                field.description,
                                "Selects, if Reload Register number is incremented, decremented or not modified")
                            self.assertEqual(field.bitOffset, 26)
                            self.assertEqual(field.bitWidth, 2)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 3)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "KEEP")
                                    self.assertEqual(enumeratedValue.description, "Reload Register number does not change automatically")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "INCREMENT")
                                    self.assertEqual(enumeratedValue.description, "Reload Register number is incremented on each match")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "DECREMENT")
                                    self.assertEqual(enumeratedValue.description, "Reload Register number is decremented on each match")
                                    self.assertEqual(enumeratedValue.value, 2)

                                enumeratedValue_index += 1

                        elif field_index == 11:
                            self.assertEqual(field.name, "S")
                            self.assertEqual(field.description, "Starts and Stops the Timer / Counter")
                            self.assertEqual(field.bitOffset, 31)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "STOP")
                                    self.assertEqual(enumeratedValue.description, "Timer / Counter is stopped")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "START")
                                    self.assertEqual(enumeratedValue.description, "Timer / Counter is started")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        field_index += 1

                elif register_index == 1:
                    self.assertEqual(register.name, "SR")
                    self.assertEqual(register.description, "Status Register")
                    self.assertEqual(register.addressOffset, 0x04)
                    self.assertEqual(register.size, 16)
                    self.assertEqual(register.access, pysvd.type.access.read_write)
                    self.assertEqual(register.resetValue, 0x0000)
                    self.assertEqual(register.resetMask, 0xd701)

                    # fields
                    field_index = 0
                    self.assertEqual(len(register.fields), 6)
                    for field in register.fields:
                        if field_index == 0:
                            self.assertEqual(field.name, "RUN")
                            self.assertEqual(field.description, "Shows if Timer is running or not")
                            self.assertEqual(field.bitOffset, 0)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_only)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Stopped")
                                    self.assertEqual(enumeratedValue.description, "Timer is not running")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Running")
                                    self.assertEqual(enumeratedValue.description, "Timer is running")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 1:
                            self.assertEqual(field.name, "MATCH")
                            self.assertEqual(field.description, "Shows if the MATCH was hit")
                            self.assertEqual(field.bitOffset, 8)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "No_Match")
                                    self.assertEqual(enumeratedValue.description, "The MATCH condition was not hit")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Match_Hit")
                                    self.assertEqual(enumeratedValue.description, "The MATCH condition was hit")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 2:
                            self.assertEqual(field.name, "UN")
                            self.assertEqual(field.description, "Shows if an underflow occured. This flag is sticky")
                            self.assertEqual(field.bitOffset, 9)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "No_Underflow")
                                    self.assertEqual(enumeratedValue.description, "No underflow occured since last clear")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Underflow")
                                    self.assertEqual(enumeratedValue.description, "A minimum of one underflow occured since last clear")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 3:
                            self.assertEqual(field.name, "OV")
                            self.assertEqual(field.description, "Shows if an overflow occured. This flag is sticky")
                            self.assertEqual(field.bitOffset, 10)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "No_Overflow")
                                    self.assertEqual(enumeratedValue.description, "No overflow occured since last clear")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Overflow_occured")
                                    self.assertEqual(enumeratedValue.description, "A minimum of one overflow occured since last clear")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 4:
                            self.assertEqual(field.name, "RST")
                            self.assertEqual(field.description, "Shows if Timer is in RESET state")
                            self.assertEqual(field.bitOffset, 12)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_only)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Ready")
                                    self.assertEqual(enumeratedValue.description, "Timer is not in RESET state and can operate")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "In_Reset")
                                    self.assertEqual(enumeratedValue.description, "Timer is in RESET state and can not operate")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 5:
                            self.assertEqual(field.name, "RELOAD")
                            self.assertEqual(field.description, "Shows the currently active RELOAD Register")
                            self.assertEqual(field.bitOffset, 14)
                            self.assertEqual(field.bitWidth, 2)
                            self.assertEqual(field.access, pysvd.type.access.read_only)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 4)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "RELOAD0")
                                    self.assertEqual(enumeratedValue.description, "Reload Register number 0 is active")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "RELOAD1")
                                    self.assertEqual(enumeratedValue.description, "Reload Register number 1 is active")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "RELOAD2")
                                    self.assertEqual(enumeratedValue.description, "Reload Register number 2 is active")
                                    self.assertEqual(enumeratedValue.value, 2)

                                elif enumeratedValue_index == 3:
                                    self.assertEqual(enumeratedValue.name, "RELOAD3")
                                    self.assertEqual(enumeratedValue.description, "Reload Register number 3 is active")
                                    self.assertEqual(enumeratedValue.value, 3)

                                enumeratedValue_index += 1

                        field_index += 1

                elif register_index == 2:
                    self.assertEqual(register.name, "INT")
                    self.assertEqual(register.description, "Interrupt Register")
                    self.assertEqual(register.addressOffset, 0x10)
                    self.assertEqual(register.size, 16)
                    self.assertEqual(register.access, pysvd.type.access.read_write)
                    self.assertEqual(register.resetValue, 0x0000)
                    self.assertEqual(register.resetMask, 0x0771)

                    # fields
                    field_index = 0
                    self.assertEqual(len(register.fields), 2)
                    for field in register.fields:
                        if field_index == 0:
                            self.assertEqual(field.name, "EN")
                            self.assertEqual(field.description, "Interrupt Enable")
                            self.assertEqual(field.bitOffset, 0)
                            self.assertEqual(field.bitWidth, 1)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 2)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Disabled")
                                    self.assertEqual(enumeratedValue.description, "Timer does not generate Interrupts")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Enable")
                                    self.assertEqual(enumeratedValue.description, "Timer triggers the TIMERn Interrupt")
                                    self.assertEqual(enumeratedValue.value, 1)

                                enumeratedValue_index += 1

                        elif field_index == 1:
                            self.assertEqual(field.name, "MODE")
                            self.assertEqual(
                                field.description,
                                "Interrupt Mode, selects on which condition the Timer should generate an Interrupt")
                            self.assertEqual(field.bitOffset, 4)
                            self.assertEqual(field.bitWidth, 3)
                            self.assertEqual(field.access, pysvd.type.access.read_write)

                            # enumeratedValues
                            enumeratedValue_index = 0
                            self.assertEqual(len(field.enumeratedValues.enumeratedValues), 3)
                            for enumeratedValue in field.enumeratedValues.enumeratedValues:
                                if enumeratedValue_index == 0:
                                    self.assertEqual(enumeratedValue.name, "Match")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer generates an Interrupt when the MATCH condition is hit")
                                    self.assertEqual(enumeratedValue.value, 0)

                                elif enumeratedValue_index == 1:
                                    self.assertEqual(enumeratedValue.name, "Underflow")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer generates an Interrupt when it underflows")
                                    self.assertEqual(enumeratedValue.value, 1)

                                elif enumeratedValue_index == 2:
                                    self.assertEqual(enumeratedValue.name, "Overflow")
                                    self.assertEqual(
                                        enumeratedValue.description,
                                        "Timer generates an Interrupt when it overflows")
                                    self.assertEqual(enumeratedValue.value, 2)

                                enumeratedValue_index += 1

                        field_index += 1

                elif register_index == 3:
                    self.assertEqual(register.name, "COUNT")
                    self.assertEqual(register.description, "The Counter Register reflects the actual Value of the Timer/Counter")
                    self.assertEqual(register.addressOffset, 0x20)
                    self.assertEqual(register.size, 32)
                    self.assertEqual(register.access, pysvd.type.access.read_write)
                    self.assertEqual(register.resetValue, 0x00000000)
                    self.assertEqual(register.resetMask, 0xffffffff)

                elif register_index == 4:
                    self.assertEqual(register.name, "MATCH")
                    self.assertEqual(register.description, "The Match Register stores the compare Value for the MATCH condition")
                    self.assertEqual(register.addressOffset, 0x24)
                    self.assertEqual(register.size, 32)
                    self.assertEqual(register.access, pysvd.type.access.read_write)
                    self.assertEqual(register.resetValue, 0x00000000)
                    self.assertEqual(register.resetMask, 0xffffffff)

                elif register_index == 5:
                    self.assertEqual(register.name, "PRESCALE_RD")
                    self.assertEqual(
                        register.description,
                        "The Prescale Register stores the Value for the prescaler. The cont event gets divided by this value")
                    self.assertEqual(register.addressOffset, 0x28)
                    self.assertEqual(register.size, 32)
                    self.assertEqual(register.access, pysvd.type.access.read_only)
                    self.assertEqual(register.resetValue, 0x00000000)
                    self.assertEqual(register.resetMask, 0xffffffff)

                elif register_index == 6:
                    self.assertEqual(register.name, "PRESCALE_WR")
                    self.assertEqual(
                        register.description,
                        "The Prescale Register stores the Value for the prescaler. The cont event gets divided by this value")
                    self.assertEqual(register.addressOffset, 0x28)
                    self.assertEqual(register.size, 32)
                    self.assertEqual(register.access, pysvd.type.access.write_only)
                    self.assertEqual(register.resetValue, 0x00000000)
                    self.assertEqual(register.resetMask, 0xffffffff)

                elif register_index == 7:
                    self.assertEqual(register.name, "RELOAD[4]")
                    self.assertEqual(
                        register.description,
                        "The Reload Register stores the Value the COUNT Register gets reloaded on a when a condition was met.")
                    self.assertEqual(register.addressOffset, 0x50)
                    self.assertEqual(register.size, 32)
                    self.assertEqual(register.access, pysvd.type.access.read_write)
                    self.assertEqual(register.resetValue, 0x00000000)
                    self.assertEqual(register.resetMask, 0xffffffff)

                register_index += 1

            peripheral_index += 1
