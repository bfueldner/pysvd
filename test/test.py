import unittest

import test_parser_text
import test_parser_integer

def suite():
    suite = unittest.TestSuite()
    suite.addTests(test_parser_text.test_parser_text())
#    suite.addTest(test_parser_integer())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
#    runner.run(suite())
    runner.run(unittest.TestLoader.loadTestsFromTestCase(test_parser_text.test_parser_text()))
