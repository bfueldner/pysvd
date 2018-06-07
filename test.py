import unittest

import test.node.element
import test.node.attribute

import test.parser.text
import test.parser.integer
import test.parser.boolean
import test.parser.enum

import test.classes.base
import test.classes.parent
import test.classes.group
import test.classes.derive
import test.classes.dim

import test.element.cpu
import test.element.sau_regions_config
import test.element.sau_regions_config_region

import test.element.address_block
import test.element.interrupt

import test.element.write_constraint
import test.element.enumerated_value
import test.element.enumerated_values

if __name__ == '__main__':
    node_element = unittest.TestLoader().loadTestsFromTestCase(test.node.element.case)
    node_attribute = unittest.TestLoader().loadTestsFromTestCase(test.node.attribute.case)

    parser_text = unittest.TestLoader().loadTestsFromTestCase(test.parser.text.value)
    parser_integer = unittest.TestLoader().loadTestsFromTestCase(test.parser.integer.value)
    parser_boolean = unittest.TestLoader().loadTestsFromTestCase(test.parser.boolean.value)
    parser_enum = unittest.TestLoader().loadTestsFromTestCase(test.parser.enum.value)

    class_base_case = unittest.TestLoader().loadTestsFromTestCase(test.classes.base.case)
    class_parent_case = unittest.TestLoader().loadTestsFromTestCase(test.classes.parent.case)
    class_group_case = unittest.TestLoader().loadTestsFromTestCase(test.classes.group.case)
    class_derive_case = unittest.TestLoader().loadTestsFromTestCase(test.classes.derive.case)
    class_dim_case = unittest.TestLoader().loadTestsFromTestCase(test.classes.dim.case)

    element_cpu = unittest.TestLoader().loadTestsFromTestCase(test.element.cpu.case)
    element_sau_regions_config = unittest.TestLoader().loadTestsFromTestCase(test.element.sau_regions_config.case)
    element_sau_regions_config_region = unittest.TestLoader().loadTestsFromTestCase(test.element.sau_regions_config_region.case)

    element_address_block = unittest.TestLoader().loadTestsFromTestCase(test.element.address_block.case)
    element_interrupt = unittest.TestLoader().loadTestsFromTestCase(test.element.interrupt.case)

    element_write_constraint = unittest.TestLoader().loadTestsFromTestCase(test.element.write_constraint.case)
    element_enumerated_value = unittest.TestLoader().loadTestsFromTestCase(test.element.enumerated_value.case)
    element_enumerated_values = unittest.TestLoader().loadTestsFromTestCase(test.element.enumerated_values.case)

    test_suites = [
        node_element,
        node_attribute,

        parser_text,
        parser_integer,
        parser_boolean,
        parser_enum,

        class_base_case,
        class_parent_case,
        class_group_case,
        class_derive_case,
        class_dim_case,
    ]
    x = '''
        element_cpu,
        element_sau_regions_config,
        element_sau_regions_config_region,

        element_address_block,
        element_interrupt,

        element_write_constraint,
        element_enumerated_value,
        element_enumerated_values,
    ]
'''
    suite = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity = 2).run(suite)
