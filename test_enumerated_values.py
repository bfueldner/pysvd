import unittest
import xml.etree.ElementTree as ET

from model import enumerated_value
from model import enumerated_values
from type import enum_usage

class test_enumerated_values(unittest.TestCase):

    def setUp(self):
        self.node = ET.parse("res/" + __name__ + ".svd").getroot()

    def test_enumerated_values(self):
        enums = enumerated_values(None, self.node)
        self.assertEqual(enums.name, "TimerIntSelect")
        self.assertEqual(enums.usage, enum_usage.read_write)
        self.assertEqual(len(enums.enumerated_value), 3)

    def test_enumerated_value_0(self):
        enums = enumerated_values(None, self.node)
        enum_value = enums.enumerated_value[0]

        self.assertEqual(enum_value.name, "disabled")
        self.assertEqual(enum_value.description, "The clock source clk0 is turned off.")
        self.assertEqual(enum_value.value, 0)

        with self.assertRaises(AttributeError):
            x = enum_value.is_default

    def test_enumerated_value_1(self):
        enums = enumerated_values(None, self.node)
        enum_value = enums.enumerated_value[1]

        self.assertEqual(enum_value.name, "enabled")
        self.assertEqual(enum_value.description, "The clock source clk1 is running.")
        self.assertEqual(enum_value.value, 1)

        with self.assertRaises(AttributeError):
            x = enum_value.is_default

    def test_enumerated_value_default(self):
        enums = enumerated_values(None, self.node)
        enum_value = enums.enumerated_value[2]

        self.assertEqual(enum_value.name, "reserved")
        self.assertEqual(enum_value.description, "Reserved values. Do not use.")
        self.assertTrue(enum_value.is_default)

        with self.assertRaises(AttributeError):
            x = enum_value.value

if __name__ == "__main__":
    unittest.main()
