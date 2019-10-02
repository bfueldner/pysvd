import pytest

from scripts.svd2h import get_string

svd = """<?xml version="1.0" encoding="utf-8"?>
<device schemaVersion="1.2" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xs:noNamespaceSchemaLocation="CMSIS-SVD.xsd">
    <name>ARMCM3</name>
    <description>ARM 32-bit Cortex-M3 Microcontroller based device, CPU clock up to 80MHz, etc.</description>
    <size>{device_size}</size>
        {peripherals}
</device>
"""


@pytest.mark.parametrize('type_header, is_system, result', [
    pytest.param(None, False, """
#ifndef ARMCM3_H
#define ARMCM3_H
#endif /* #ifndef ARMCM3_H */
    """, id='no user type header'),
    pytest.param(None, True, """
#ifndef ARMCM3_H
#define ARMCM3_H
#endif /* #ifndef ARMCM3_H */
    """, id='no system type header'),
    pytest.param('test.h', False, """
#ifndef ARMCM3_H
#define ARMCM3_H
#include "test.h"
#endif /* #ifndef ARMCM3_H */
    """, id='user type header'),
    pytest.param('test.h', True, """
#ifndef ARMCM3_H
#define ARMCM3_H
#include <test.h>
#endif /* #ifndef ARMCM3_H */
    """, id='system type header')
])
def test_include_type_header(type_header, is_system, result):
    assert get_string(svd.format(peripherals='', device_size=32), type_header, is_system) == result


@pytest.mark.parametrize('type_prefix, type_suffix, device_size, register_size, result', [
    pytest.param('_p', '_s', 16, None, """
#ifndef ARMCM3_H
#define ARMCM3_H
#define PERIPHERAL_BASE_ADDRESS (0x00000000u)
#define PERIPHERAL_REGISTER (*(volatile _p16_s *)(PERIPHERAL_BASE_ADDRESS + 0x00u))
#endif /* #ifndef ARMCM3_H */
    """, id='\'_p\' prefix, \'_s\' suffix, device size 16, no register size'),
    pytest.param('_p', '_s', 32, None, """
#ifndef ARMCM3_H
#define ARMCM3_H
#define PERIPHERAL_BASE_ADDRESS (0x00000000u)
#define PERIPHERAL_REGISTER (*(volatile _p32_s *)(PERIPHERAL_BASE_ADDRESS + 0x00u))
#endif /* #ifndef ARMCM3_H */
    """, id='\'_p\' prefix, \'_s\' suffix, device size 16, register size 32'),
    pytest.param('_p', '_s', 16, 32, """
#ifndef ARMCM3_H
#define ARMCM3_H
#define PERIPHERAL_BASE_ADDRESS (0x00000000u)
#define PERIPHERAL_REGISTER (*(volatile _p32_s *)(PERIPHERAL_BASE_ADDRESS + 0x00u))
#endif /* #ifndef ARMCM3_H */
    """, id='\'_p\' prefix, \'_s\' suffix, device size 32, no register size')
])
def test_register_type(type_prefix, type_suffix, device_size, register_size, result):
    assert get_string(svd.format(peripherals="""<peripherals>
    <peripheral>
        <name>PERIPHERAL</name>
        <baseAddress>0x00000000</baseAddress>
        <registers>
            <register>
                <name>REGISTER</name>
                <addressOffset>0x00</addressOffset>
                {size}
            </register>
        </registers>
    </peripheral>
</peripherals>""".format(size='' if register_size is None else '<size>' + str(register_size) + '</size>'),
                                 device_size=device_size),
                      type_prefix=type_prefix,
                      type_suffix=type_suffix) == result


def test_array_register():
    assert get_string(svd.format(peripherals="""<peripherals>
        <peripheral>
            <name>PERIPHERAL</name>
            <baseAddress>0x00000000</baseAddress>
            <registers>
                <register>
                    <dim>16</dim>
                    <dimIncrement>4</dimIncrement>
                    <name>REGISTER%s</name>
                    <addressOffset>0x00000000</addressOffset>
                </register>
            </registers>
        </peripheral>
    </peripherals>""", device_size=32)) == """
#ifndef ARMCM3_H
#define ARMCM3_H
#define PERIPHERAL_BASE_ADDRESS (0x00000000u)
#define PERIPHERAL_REGISTER ((volatile uint32_t *)(PERIPHERAL_BASE_ADDRESS + 0x00000000u))
#define PERIPHERAL_REGISTER_0 (*(volatile uint32_t *)(PERIPHERAL_BASE_ADDRESS + 0x00000000 + (0u)))
#define PERIPHERAL_REGISTER_1 (*(volatile uint32_t *)(PERIPHERAL_BASE_ADDRESS + 0x00000000 + (32u)))
#define PERIPHERAL_REGISTER_2 (*(volatile uint32_t *)(PERIPHERAL_BASE_ADDRESS + 0x00000000 + (64u)))
#define PERIPHERAL_REGISTER_3 (*(volatile uint32_t *)(PERIPHERAL_BASE_ADDRESS + 0x00000000 + (96u)))
#endif /* #ifndef ARMCM3_H */
    """
