import unittest

import test_parser_text
import test_parser_integer

if __name__ == '__main__':
    parser_text = unittest.TestLoader().loadTestsFromTestCase(test_parser_text.test_parser_text)
    parser_integer = unittest.TestLoader().loadTestsFromTestCase(test_parser_integer.test_parser_integer)

    test_suites = [
        parser_text,
        parser_integer
    ]
    suite = unittest.TestSuite(test_suites)

    unittest.TextTestRunner(verbosity = 2).run(suite)

#    runner = unittest.TextTestRunner()
#    runner.run(loader)
