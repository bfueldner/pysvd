#!/usr/bin/env python3
# coding: utf-8
"""pysvd example project.

Read SVD file and generate C-style register access structs.
"""

import argparse
import xml.etree.ElementTree as ET
import pysvd
from enum import Enum

access = {
    pysvd.type.access.read_write: '__IO',
    pysvd.type.access.read_only: '__I',
    pysvd.type.access.write_only: '__O',
}

data_type = {
    8: 'uint8_t',
    16: 'uint16_t',
    32: 'uint32_t',
}

def format_registers(output, prefix, registers):
    data = []
    for register in registers:
        data.append(('`{1} <{0}.{1}_>`_'.format(prefix, register.name), '0x{:02X}'.format(register.addressOffset)))
    if len(data):
        output.write(table(('Register', 'Offset'), data))

    for register in registers:
        output.write('.. _{}.{}:\n\n'.format(prefix, register.name))

        output.write(underline(register.description, section.subsubsection))

        output.write(rst_list_name.format('Name', register.name))
        output.write(rst_list_name.format('Size', register.size))
        output.write(rst_list_name.format('Offset', '0x{:02X}'.format(register.addressOffset)))
        output.write(rst_list_name.format('Reset', '0x{:{fill}{width}X}'.format(register.resetValue, fill='0', width=register.size // 4)))
        output.write(rst_list_name.format('Access', register.access))
        output.write('\n')

        # Table

        # Bit description
        for field in register.fields:
            if field.bitWidth == 1:
                output.write('- Bit {} ({}) - {}\n'.format(field.bitOffset, field.access, field.name))
            else:
                output.write('- Bits {}:{} ({}) - {}\n'.format(
                    field.bitOffset + field.bitWidth - 1, field.bitOffset, field.access, field.name))
            output.write('   {}\n\n'.format(field.description))

            if hasattr(field, 'enumeratedValues'):
                for enumeratedValue in field.enumeratedValues.enumeratedValues:
                    output.write('   - {} - {}\n'.format(enumeratedValue.value, enumeratedValue.name))
                    if hasattr(enumeratedValue, 'description'):
                        output.write('      {}\n'.format(enumeratedValue.description))
                output.write('\n')


def write_register(register, output):
    output.write("    union\n    {\n")
    output.write("    {1} {2} {0.name};\n".format(register, access[register.access], data_type[register.size]))


def write_peripheral(peripheral, output):
    output.write("/* {0.name} - {0.description} */\n\n".format(peripheral))

    index = 1;
    offset = 0
    output.write("struct __attribute__((packed))  {0.name}_t\n{{\n".format(peripheral))
    for register in peripheral.registers:
        if register.addressOffset != offset:
            output.write("    __I {0} _{1};\n".format(data_type[register.addressOffset - offset]), index)
            index += 1
        write_register(register, output)
        offset = register.addressOffset + register.size // 8
    output.write("};\n")
    output.write("static_assert(sizeof({0}_t) == {1}, \"Size of {0}_t mismatch\");\n\n".format(peripheral.name, offset))

def main():
    parser = argparse.ArgumentParser(description='SVD to C-style register access structs')
    parser.add_argument('--svd', metavar='FILE', type=str, help='System view description (SVD) file', required=True)
    parser.add_argument('--output', '-o',  metavar='FILE', type=str, help='C output file', required=True)
    parser.add_argument('--version', action='version', version=pysvd.__version__)
    args = parser.parse_args()

    node = ET.parse(args.svd).getroot()
    device = pysvd.element.Device(node)

    output = open(args.output, "w")

    # Header
    output.write("/**\n" \
        " * @file\n" \
        " * @version {0.version}\n" \
        " * @brief Register access structs for {0.vendor} {0.name}\n" \
        " * @note This file is autogenerated using pysvd {1.__version__}\n" \
        " */\n\n".format(device, pysvd)
    )
    output.write("#pragma once\n\n")

    output.write("#define __I volatile const /*!< Read only permission */\n" \
        "#define __O volatile  /*!< Write only permission */\n" \
        "#define __IO volatile /*!< Read/write permission */\n\n"
    )

    # Interrupts
    interrupts = []
    for peripheral in device.peripherals:
        interrupts += peripheral.interrupts

    interrupt_count = 0
    interrupt_name = ""
    output.write("enum IRQn\n{\n")
    for interrupt in sorted(interrupts, key=lambda interrupt: interrupt.value):
        if interrupt_name != interrupt.name:
            output.write("    {0.name:20}= {0.value},\n".format(interrupt))
            interrupt_name = interrupt.name
            interrupt_count += 1
    output.write("};\n\n")

    # Peripherals
    data = []
    for peripheral in sorted(device.peripherals, key=lambda peripheral: peripheral.name):
        if peripheral.name.startswith('ADC'):
            write_peripheral(peripheral, output)
    output.close()

if __name__ == '__main__':
    main()
