import unittest
import pysvd


class TestParserText(unittest.TestCase):

    def test_no_param(self):
        test = pysvd.parser.Text('Text')

        self.assertEqual(test, 'Text')

    def test_default_none(self):
        test = pysvd.parser.Text(None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = pysvd.parser.Text(None, 'value')

        self.assertEqual(test, 'value')


class TestParserInteger(unittest.TestCase):

    def test_default_none(self):
        test = pysvd.parser.Integer(None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = pysvd.parser.Integer(None, 16)

        self.assertEqual(test, 16)

    def test_decimal(self):
        test = pysvd.parser.Integer('4711')

        self.assertEqual(test, 4711)

    def test_hexadecimal(self):
        test = pysvd.parser.Integer('0x1234')

        self.assertEqual(test, 0x1234)

    def test_binary_0b(self):
        test = pysvd.parser.Integer('0b110xx011')

        self.assertEqual(test, 195)

    def test_binary_hash(self):
        test = pysvd.parser.Integer('#110xx011')

        self.assertEqual(test, 195)

    def test_exception(self):
        with self.assertRaises(ValueError):
            pysvd.parser.Integer('text')


class TestParserBoolean(unittest.TestCase):

    def test_default_none(self):
        test = pysvd.parser.Boolean(None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = pysvd.parser.Boolean(None, False)

        self.assertEqual(test, False)

    def test_false_value(self):
        test = pysvd.parser.Boolean('0')

        self.assertEqual(test, False)

    def test_false_text(self):
        test = pysvd.parser.Boolean('FaLsE')

        self.assertEqual(test, False)

    def test_true_value(self):
        test = pysvd.parser.Boolean('1')

        self.assertEqual(test, True)

    def test_true_text(self):
        test = pysvd.parser.Boolean('tRuE')

        self.assertEqual(test, True)

    def test_exception(self):
        with self.assertRaises(ValueError):
            pysvd.parser.Boolean('text')


class TestParserEnum(unittest.TestCase):

    def test_default_none(self):
        test = pysvd.parser.Enum(pysvd.type.access, None)

        self.assertIsNone(test)

    def test_default_value(self):
        test = pysvd.parser.Enum(
            pysvd.type.access,
            None,
            pysvd.type.access.read_only)

        self.assertEqual(test, pysvd.type.access.read_only)

    def test_enum(self):
        test = pysvd.parser.Enum(pysvd.type.access, 'read-write')

        self.assertEqual(test, pysvd.type.access.read_write)

    def test_exception(self):
        with self.assertRaises(KeyError):
            pysvd.parser.Enum(pysvd.type.access, 'unknown')
