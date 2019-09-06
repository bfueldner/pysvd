import unittest
import xml.etree.ElementTree as ET

import pysvd


class TestSpecialCluster(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        node = ET.parse("test/specialCluster.xml").getroot()
        cls.peripheral = pysvd.element.Peripheral(None, node)

    def test_general(self):
        peripheral = self.peripheral

        self.assertEqual(peripheral.name, "RTC")
        self.assertEqual(peripheral.version, "1.0.1")
        self.assertEqual(peripheral.description, "Real-Time Counter")
        self.assertEqual(peripheral.groupName, "RTC")
        self.assertEqual(peripheral.prependToName, "RTC_")
        self.assertEqual(peripheral.baseAddress, 0x40001400)

    def test_address_block(self):
        self.assertEqual(len(self.peripheral.addressBlocks), 1)
        addressBlock = self.peripheral.addressBlocks[0]

        self.assertEqual(addressBlock.offset, 0)
        self.assertEqual(addressBlock.size, 0x40)
        self.assertEqual(addressBlock.usage, pysvd.type.addressBlockUsage.registers)

    def test_interrupt(self):
        self.assertEqual(len(self.peripheral.interrupts), 1)
        interrupt = self.peripheral.interrupts[0]

        self.assertEqual(interrupt.name, "RTC_INTREQ")
        self.assertEqual(interrupt.value, 3)

    def test_register(self):
        peripheral = self.peripheral

        self.assertEqual(len(peripheral.registers), 0)

    def test_cluster(self):
        peripheral = self.peripheral

        cluster_index = 0
        self.assertEqual(len(peripheral.clusters), 3)
        for cluster in peripheral.clusters:
            if cluster_index == 0:
                self.assertEqual(cluster.name, "MODE0")
                self.assertEqual(cluster.description, "32-bit Counter with Single 32-bit Compare")
                self.assertEqual(cluster.headerStructName, "RtcMode0")
                self.assertEqual(cluster.addressOffset, 0)

            elif cluster_index == 1:
                self.assertEqual(cluster.name, "MODE1")
                self.assertEqual(cluster.description, "16-bit Counter with Two 16-bit Compares")
                self.assertEqual(cluster.alternateCluster, "MODE0")
                self.assertEqual(cluster.headerStructName, "RtcMode1")
                self.assertEqual(cluster.addressOffset, 0)

            elif cluster_index == 2:
                self.assertEqual(cluster.name, "MODE2")
                self.assertEqual(cluster.description, "Clock/Calendar with Alarm")
                self.assertEqual(cluster.alternateCluster, "MODE0")
                self.assertEqual(cluster.headerStructName, "RtcMode2")
                self.assertEqual(cluster.addressOffset, 0)

            cluster_index += 1

    def test_cluster0_register(self):
        peripheral = self.peripheral

        self.assertEqual(len(peripheral.clusters), 3)
        cluster = peripheral.clusters[0]

        register_index = 0
        self.assertEqual(len(cluster.registers), 5)
        for register in cluster.registers:
            if register_index == 0:
                self.assertEqual(register.name, "CTRL")
                self.assertEqual(register.description, "MODE0 Control")
                self.assertEqual(register.addressOffset, 0x00)
                self.assertEqual(register.size, 16)

            elif register_index == 1:
                self.assertEqual(register.name, "READREQ")
                self.assertEqual(register.description, "Read Request")
                self.assertEqual(register.addressOffset, 0x02)
                self.assertEqual(register.size, 16)
                self.assertEqual(register.resetValue, 0x0010)

            elif register_index == 2:
                self.assertEqual(register.name, "STATUS")
                self.assertEqual(register.description, "Status")
                self.assertEqual(register.addressOffset, 0x0A)
                self.assertEqual(register.size, 8)

            elif register_index == 3:
                self.assertEqual(register.name, "COUNT")
                self.assertEqual(register.description, "MODE0 Counter Value")
                self.assertEqual(register.addressOffset, 0x10)
                self.assertEqual(register.size, 32)

            elif register_index == 4:
                self.assertEqual(register.name, "COMP0")
                self.assertEqual(register.description, "MODE0 Compare n Value")
                self.assertEqual(register.addressOffset, 0x18)
                self.assertEqual(register.size, 32)

            register_index += 1

    def test_cluster1_register(self):
        peripheral = self.peripheral

        self.assertEqual(len(peripheral.clusters), 3)
        cluster = peripheral.clusters[1]

        register_index = 0
        self.assertEqual(len(cluster.registers), 7)
        for register in cluster.registers:
            if register_index == 0:
                self.assertEqual(register.name, "CTRL")
                self.assertEqual(register.description, "MODE1 Control")
                self.assertEqual(register.addressOffset, 0x00)
                self.assertEqual(register.size, 16)

            elif register_index == 1:
                self.assertEqual(register.name, "READREQ")
                self.assertEqual(register.description, "Read Request")
                self.assertEqual(register.addressOffset, 0x02)
                self.assertEqual(register.size, 16)
                self.assertEqual(register.resetValue, 0x0010)

            elif register_index == 2:
                self.assertEqual(register.name, "STATUS")
                self.assertEqual(register.description, "Status")
                self.assertEqual(register.addressOffset, 0x0A)
                self.assertEqual(register.size, 8)

            elif register_index == 3:
                self.assertEqual(register.name, "COUNT")
                self.assertEqual(register.description, "MODE1 Counter Value")
                self.assertEqual(register.addressOffset, 0x10)
                self.assertEqual(register.size, 16)

            elif register_index == 4:
                self.assertEqual(register.name, "PER")
                self.assertEqual(register.description, "MODE1 Counter Period")
                self.assertEqual(register.addressOffset, 0x14)
                self.assertEqual(register.size, 16)

            elif register_index == 5:
                self.assertEqual(register.name, "COMP0")
                self.assertEqual(register.description, "MODE1 Compare n Value")
                self.assertEqual(register.addressOffset, 0x18)
                self.assertEqual(register.size, 16)

            elif register_index == 6:
                self.assertEqual(register.name, "COMP1")
                self.assertEqual(register.description, "MODE1 Compare n Value")
                self.assertEqual(register.addressOffset, 0x1A)
                self.assertEqual(register.size, 16)

            register_index += 1

    def test_cluster2_register(self):
        peripheral = self.peripheral

        self.assertEqual(len(peripheral.clusters), 3)
        cluster = peripheral.clusters[2]

        register_index = 0
        self.assertEqual(len(cluster.registers), 6)
        for register in cluster.registers:
            if register_index == 0:
                self.assertEqual(register.name, "CTRL")
                self.assertEqual(register.description, "MODE2 Control")
                self.assertEqual(register.addressOffset, 0x00)
                self.assertEqual(register.size, 16)

            elif register_index == 1:
                self.assertEqual(register.name, "READREQ")
                self.assertEqual(register.description, "Read Request")
                self.assertEqual(register.addressOffset, 0x02)
                self.assertEqual(register.size, 16)
                self.assertEqual(register.resetValue, 0x0010)

            elif register_index == 2:
                self.assertEqual(register.name, "STATUS")
                self.assertEqual(register.description, "Status")
                self.assertEqual(register.addressOffset, 0x0A)
                self.assertEqual(register.size, 8)

            elif register_index == 3:
                self.assertEqual(register.name, "CLOCK")
                self.assertEqual(register.description, "MODE2 Clock Value")
                self.assertEqual(register.addressOffset, 0x10)
                self.assertEqual(register.size, 32)

            elif register_index == 4:
                self.assertEqual(register.name, "ALARM0")
                self.assertEqual(register.description, "MODE2 Alarm n Value")
                self.assertEqual(register.addressOffset, 0x18)
                self.assertEqual(register.size, 32)

            elif register_index == 5:
                self.assertEqual(register.name, "MASK0")
                self.assertEqual(register.description, "MODE2 Alarm n Mask")
                self.assertEqual(register.addressOffset, 0x1C)
                self.assertEqual(register.size, 8)

            register_index += 1


class TestSpecialDerivePeripheral(unittest.TestCase):

    def test_ctor(self):
        pass

    def test_attributes(self):
        pass


class TestSpecialDeriveRegister(unittest.TestCase):

    def test_ctor(self):
        pass

    def test_attributes(self):
        pass


class TestSpecialDeriveField(unittest.TestCase):

    def test_ctor(self):
        pass

    def test_attributes(self):
        pass


class TestSpecialDeriveEnumeratedValues(unittest.TestCase):

    def test_ctor(self):
        pass

    def test_attributes(self):
        pass


class TestSpecialDeriveAll(unittest.TestCase):

    def test_ctor(self):
        pass

    def test_attributes(self):
        pass
