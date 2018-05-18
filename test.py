import unittest

import test.parser.text
import test.parser.integer
import test.parser.boolean
import test.parser.enum

if __name__ == '__main__':
    parser_text = unittest.TestLoader().loadTestsFromTestCase(test.parser.text.value)
    parser_integer_decimal = unittest.TestLoader().loadTestsFromTestCase(test.parser.integer.decimal)
    parser_integer_hexadecimal = unittest.TestLoader().loadTestsFromTestCase(test.parser.integer.hexadecimal)
    parser_integer_binary1 = unittest.TestLoader().loadTestsFromTestCase(test.parser.integer.binary1)
    parser_integer_binary2 = unittest.TestLoader().loadTestsFromTestCase(test.parser.integer.binary2)
    parser_integer_exception = unittest.TestLoader().loadTestsFromTestCase(test.parser.integer.exception)
    parser_boolean_false_integer = unittest.TestLoader().loadTestsFromTestCase(test.parser.boolean.false_integer)
    parser_boolean_false_text = unittest.TestLoader().loadTestsFromTestCase(test.parser.boolean.false_text)
    parser_boolean_true_integer = unittest.TestLoader().loadTestsFromTestCase(test.parser.boolean.true_integer)
    parser_boolean_true_text = unittest.TestLoader().loadTestsFromTestCase(test.parser.boolean.true_text)
    parser_boolean_exception = unittest.TestLoader().loadTestsFromTestCase(test.parser.boolean.exception)
    parser_enum_value = unittest.TestLoader().loadTestsFromTestCase(test.parser.enum.value)
    parser_enum_exception = unittest.TestLoader().loadTestsFromTestCase(test.parser.enum.exception)

    test_suites = [
        parser_text,
        parser_integer_decimal,
        parser_integer_hexadecimal,
        parser_integer_binary1,
        parser_integer_binary2,
        parser_integer_exception,
        parser_boolean_false_integer,
        parser_boolean_false_text,
        parser_boolean_true_integer,
        parser_boolean_true_text,
        parser_boolean_exception,
        parser_enum_value,
        parser_enum_exception,
    ]
    suite = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity = 2).run(suite)
