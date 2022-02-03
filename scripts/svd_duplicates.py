#!/usr/bin/env python3
# coding: utf-8
"""Read SVD file, order elements, check for valid elements to generate register access structs and displays possible substitutions.
"""

import sys
import argparse
import xml.etree.ElementTree as ET
from enum import IntEnum
import itertools
from natsort import natsorted
from colorama import Fore, Back, Style

import pysvd

class Level(IntEnum):
    """Output level."""
    warning = 0
    hint = 1
    all = 2

class Depth(IntEnum):
    """Analysis depth."""
    peripherals = 0
    registers = 1
    fields = 2
    enumeratedValues = 3

def integer(value):
    """Convert binary, hex, octal and decimal strings to integer."""
    if value.startswith('#'):
        value = value.replace('#', '0b')

    if value.startswith('0b'):
        value = value.replace('x', '0')
    return int(value, 0)

def compare_peripherals(level, peripherals):
    """Compare peripherals."""

    print("{0.CYAN}Peripherals{0.RESET}".format(Fore))

    peripherals_base = []
    peripherals_derived = []
    peripherals_not_derived = []
    for a, b in itertools.combinations(peripherals, 2):
        # Check if item is already in list
        if a in peripherals_derived + peripherals_not_derived:
            continue

        if a.equal_struct(b):
            if a not in peripherals_base:
                peripherals_base.append(a)

            # Already derived peripheral
            if b.derivedFrom:
                if level >= Level.all:
                    print("[{0.GREEN}OK{0.RESET}] Peripheral '{2.name}' is derived from '{1.name}'".format(Fore, b.derivedFrom, b))
                peripherals_derived.append(b)
            # Derivable peripheral
            else:
                if level >= Level.warning:
                    print("[{0.RED}WARNING{0.RESET}] Peripheral '{2.name}' can be derived from '{1.name}'".format(Fore, a, b))
                peripherals_not_derived.append(b)

    peripherals_none_derivable = [peripheral for peripheral in peripherals \
        if peripheral not in peripherals_base and \
            peripheral not in peripherals_derived and \
            peripheral not in peripherals_not_derived]

    if level >= Level.hint:
        for peripheral in peripherals_none_derivable:
            print("[{0.YELLOW}HINT{0.RESET}] Peripheral '{1.name}' can not be derived".format(Fore, peripheral))
    print()

    return (peripherals_base, peripherals_none_derivable)

def compare_registers(level, peripheral, registers):
    print("{0.CYAN}Registers of peripheral '{1}'{0.RESET}".format(Fore, peripheral.name))

    registers_base = []
    registers_derived = []
    registers_not_derived = []

    for a, b in itertools.combinations(registers, 2):
        # Check if item is already in list
        if a in registers_derived + registers_not_derived:
            continue

        if a.equal_struct(b):
            if a not in registers_base:
                registers_base.append(a)

            # Already derived register
            if b.derivedFrom:
                if level >= Level.all:
                    print("[{0.GREEN}OK{0.RESET}] Register '{2.name}' is derived from '{1.name}'".format(Fore, b.derivedFrom, b))
                registers_derived.append(b)
            # Derivable register
            else:
                if level >= Level.warning:
                    print("[{0.RED}WARNING{0.RESET}] Register '{2.name}' can be derived from '{1.name}'".format(Fore, a, b))
                registers_not_derived.append(b)

    registers_none_derivable = [register for register in registers \
        if register not in registers_base and \
            register not in registers_derived and \
            register not in registers_not_derived]

    if level >= Level.hint:
        for register in registers_none_derivable:
            print("[{0.YELLOW}HINT{0.RESET}] Register '{1.name}' can not be derived".format(Fore, register))
    print()

    return (registers_base, registers_none_derivable)

def main():
    parser = argparse.ArgumentParser(description='Read SVD file, order elements, check for' \
        'valid elements to generate register access structs and displays possible substitutions.')
    parser.add_argument('--svd', metavar='FILE', type=str, help='System view description (SVD) file', required=True)
    parser.add_argument('--output', '-o', metavar='FILE', type=str, help='Save ordered SVD output file')
    parser.add_argument('--level', '-l', choices=['all', 'hint', 'warning'], help='Select level of output messages', default='all')
    parser.add_argument('--depth', '-d', choices=['peripherals', 'registers', 'fields', 'enumeratedValues'], help='Select depth of analysis', default='enumeratedValues')
    args = parser.parse_args()
    level = Level[args.level]
    depth = Depth[args.depth]

    xml = ET.parse(args.svd)

    print('Sort peripherals by name')
    for peripherals in xml.findall('.//peripherals'):
        peripherals[:] = natsorted(peripherals, key=lambda x: x.find('name').text)

    print('Sort registers by addressOffset')
    for registers in xml.findall('.//registers'):
        registers[:] = sorted(registers, key=lambda x: integer(x.find('addressOffset').text))

    print('Sort fields by bitOffset')
    for fields in xml.findall('.//fields'):
        fields[:] = sorted(fields, key=lambda x: integer(x.find('bitOffset').text))

    print('Sort enumeratedValues by value')
    for enumeratedValues in xml.findall('.//enumeratedValues'):
        enumeratedValues[:] = sorted(enumeratedValues, key=lambda x: integer(x.find('value').text))

    print('Remove linebreaks from description tags')
    for item in xml.findall('.//description'):
        text = item.text.replace('\n', ' ').strip()
        item.text = ' '.join(text.split())

    if args.output:
        xml.write(args.output, encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=True)
    print()

    # Load ordered SVD file
    try:
        device = pysvd.element.Device(xml.getroot())
    except Exception as e:
        print("Error parsing SVD file: {}".format(str(e)))
        sys.exit(2)

    (peripherals_base, peripherals_none_derivable) = compare_peripherals(level, device.peripherals)
    if depth >= Depth.registers:
        peripherals = natsorted(peripherals_base + peripherals_none_derivable, key=lambda peripheral: peripheral.name)
        for peripheral in peripherals:
            compare_registers(level, peripheral, peripheral.registers)

if __name__ == '__main__':
    main()
