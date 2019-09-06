#!/usr/bin/env python3
# coding: utf-8
"""pysvd example project.

Read SVD file and generate device datasheet in rst format.
"""

import argparse
import xml.etree.ElementTree as ET
import pysvd
from enum import Enum

rst_list_name = ":{}: {}\n"


class section(Enum):
    section = '='
    subsection = '-'
    subsubsection = '^'
    paragraphs = '"'

    def __str__(self):
        return self.value


def underline(value, section):
    return "{}\n{}\n\n".format(value, str(section) * len(value))


def table(header, data):
    if len(data) == 0:
        raise ValueError("data has no length")

    if len(header) != len(data[0]):
        raise ValueError("columns in header and data do not match")

    # Find width of column
    widths = []
    for caption in header:
        widths.append(len(caption))

    for row in data:
        index = 0
        for text in row:
            widths[index] = max(widths[index], len(text))
            index += 1

    result = ''
    separator = []
    line = []

    index = 0
    for caption in header:
        separator.append('=' * widths[index])
        line.append('{:{align}{width}}'.format(caption, align='^', width=widths[index]))
        index += 1

    result = ' '.join(separator) + '\n'
    result += ' '.join(line).rstrip() + '\n'
    result += ' '.join(separator) + '\n'

    for row in data:
        index = 0
        for text in row:
            line[index] = '{:{width}}'.format(text, width=widths[index])
            index += 1
        result += ' '.join(line).rstrip() + '\n'
    result += ' '.join(separator) + '\n'

    return result + '\n'


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


def main():
    parser = argparse.ArgumentParser(description='SVD to ReST converter')
    parser.add_argument('--svd', metavar='FILE', type=str, help='System view description (SVD) file', required=True)
    parser.add_argument('--output', '-o',  metavar='FILE', type=str, help='ReST output file', required=True)
    parser.add_argument('--version', action='version', version=pysvd.__version__)
    args = parser.parse_args()

    node = ET.parse(args.svd).getroot()
    device = pysvd.element.Device(node)

    output = open(args.output, "w")

    # Device
    output.write(underline('Device', section.section))

    output.write(rst_list_name.format('Name', device.name))
    output.write(rst_list_name.format('Description', device.description))
    if hasattr(device, 'series'):
        output.write(rst_list_name.format('Series', device.series))
    output.write(rst_list_name.format('Version', device.version))
    if hasattr(device, 'vendor'):
        output.write(rst_list_name.format('Vendor', device.vendor))
    output.write('\n')

    output.write(rst_list_name.format('Address unit bits', device.addressUnitBits))
    output.write(rst_list_name.format('Data width', device.width))
    output.write('\n')

    # CPU
    output.write(underline('CPU', section.section))

    cpu = device.cpu
    output.write(rst_list_name.format('Name', str(cpu.name).replace('CM', 'Cortex-M').replace('CA', 'Cortex-A').replace('PLUS', '+')))
    output.write(rst_list_name.format('Revision', cpu.revision))
    output.write(rst_list_name.format('Endian', cpu.endian))
    output.write(rst_list_name.format('MPU', 'yes' if cpu.mpuPresent else 'no'))
    output.write(rst_list_name.format('FPU', 'yes' if cpu.fpuPresent else 'no'))
    if hasattr(cpu, 'fpuDP'):
        output.write(rst_list_name.format('FPU DP', 'yes' if cpu.fpuDP else 'no'))
    if hasattr(cpu, 'icachePresent'):
        output.write(rst_list_name.format('I-Cache', 'yes' if cpu.icachePresent else 'no'))
    if hasattr(cpu, 'dcachePresent'):
        output.write(rst_list_name.format('D-Cache', 'yes' if cpu.dcachePresent else 'no'))
    if hasattr(cpu, 'itcmPresent'):
        output.write(rst_list_name.format('ITCM', 'yes' if cpu.itcmPresent else 'no'))
    if hasattr(cpu, 'dtcmPresent'):
        output.write(rst_list_name.format('DTCM', 'yes' if cpu.dtcmPresent else 'no'))
    output.write(rst_list_name.format('VTOR', 'yes' if cpu.vtorPresent else 'no'))
    if hasattr(cpu, 'deviceNumInterrupts'):
        output.write(rst_list_name.format('Interrupts', cpu.deviceNumInterrupts))
    output.write(rst_list_name.format('Interrupt priorities', 2 ** cpu.nvicPrioBits))
    output.write(rst_list_name.format('Vendor SYSTICK', 'yes' if cpu.vendorSystickConfig else 'no'))
    output.write('\n')

    # Memory mapping
    output.write(underline('Memory mapping', section.section))

    data = []
    for peripheral in sorted(device.peripherals, key=lambda peripheral: peripheral.baseAddress):
        data.append(('{}_'.format(peripheral.name), '0x{:08X}'.format(peripheral.baseAddress)))
    output.write(table(('Peripheral', 'Address'), data))

    # Interrupt mapping
    output.write(underline('Interrupt mapping', section.section))

    data = []
    interrupts = []
    for peripheral in device.peripherals:
        interrupts += peripheral.interrupts

    for interrupt in sorted(interrupts, key=lambda interrupt: interrupt.value):
        data.append(('`{0}.{1} <{0}_>`_'.format(interrupt.parent.name, interrupt.name), str(interrupt.value)))
    output.write(table(('Peripheral', 'Interrupt'), data))

    # Peripheral
    output.write(underline('Peripheral', section.section))

    for peripheral in device.peripherals:
        output.write('.. _{}:\n\n'.format(peripheral.name))

        output.write(underline('{} ({})'.format(peripheral.description, peripheral.name), section.subsection))

        if hasattr(peripheral, 'version'):
            output.write(rst_list_name.format('Version', peripheral.version))
        output.write(rst_list_name.format('Address', '0x{:08X}'.format(peripheral.baseAddress)))
        for interrupt in peripheral.interrupts:
            output.write(rst_list_name.format('Interrupt {}'.format(interrupt.name), interrupt.value))
        output.write("\n")

        data = []
        for cluster in peripheral.clusters:
            data.append(('`{1} <{0}.{1}_>`_'.format(peripheral.name, cluster.name), '0x{:02X}'.format(cluster.addressOffset)))
        if len(data):
            output.write(table(('Cluster', 'Offset'), data))

        format_registers(output, peripheral.name, peripheral.registers)

        for cluster in peripheral.clusters:
            output.write('.. _{}.{}:\n\n'.format(peripheral.name, cluster.name))

            output.write(underline('{} ({})'.format(cluster.description, cluster.name), section.subsubsection))

            format_registers(output, '{}.{}'.format(peripheral.name, cluster.name), cluster.registers)

    output.write("Autogenerated ReST with pysvd {}\n".format(pysvd.__version__))
    output.close()


if __name__ == '__main__':
    main()
