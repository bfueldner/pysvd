import unittest
import pysvd


class TestTypeCpuName(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.cpuName.CM0PLUS), 'CM0PLUS')


class TestTypeEndian(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.endian.little), 'little')


class TestTypeDataType(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.dataType.uint32_t), 'uint32_t')


class TestTypeProtection(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.protection.non_secure), 'non-secure')


class TestTypeSauAccess(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.sauAccess.non_secure_callable_secure), 'non-secure-callable-secure')


class TestTypeAccess(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.access.read_write), 'read-write')


class TestTypeModifiedWriteValues(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.modifiedWriteValues.zeroToClear), 'zeroToClear')


class TestTypeReadAction(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.readAction.modify), 'modify')


class TestTypeEnumUsage(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.enumUsage.read_write), 'read-write')


class TestTypeAddressBlockUsage(unittest.TestCase):

    def test_string(self):
        self.assertEqual(str(pysvd.type.addressBlockUsage.registers), 'registers')
