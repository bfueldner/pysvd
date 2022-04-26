[![Latest version on PyPi](https://img.shields.io/pypi/v/pysvd)](https://pypi.org/project/pysvd) [![Python versions](https://img.shields.io/pypi/pyversions/pysvd)](https://pypi.org/project/pysvd) [![License](https://img.shields.io/pypi/l/pysvd)](https://pypi.org/project/pysvd) [![Build state](https://travis-ci.org/bfueldner/pysvd.svg?branch=master)](https://travis-ci.org/bfueldner/pysvd) [![Coverage](https://coveralls.io/repos/github/bfueldner/pysvd/badge.svg?branch=master)](https://coveralls.io/github/bfueldner/pysvd?branch=master)

# pysvd
A **S**ystem **V**iew **D**escription v1.3.5 parser package for Python 3.5+.

## What is SVD?

SVD is a XML based file format developed by ARM to describe the software sight of a microcontroller device. It contains all peripherals,
registers, bitfields and enumeration values to access every part on a device. For further information have a look at the [format description](https://www.keil.com/pack/doc/CMSIS/SVD/html/svd_Format_pg.html).

## Motivation

SVD is a great format to develop embedded systems on. Existing parser out in the field did not support all features (derive, dimension) supported by the format.

With the parsed system view tree, you can do several cool things:

* Automatic register generation (BSP skeleton)
* Linker file generation
* GDB register debug symbol generation
* Custom datasheet generation

## Conformance

This parser is build to reflect 1:1 the XSD format behind SVD. The only compromis has been made by the nodes `peripherals`, `registers` and `fields` that are simple container objects.

The node names and attributes follow the same naming convention in XML as in Python to map them easier between the languages.

## Installation

Install from [PyPI](https://pypi.org) using pip:

```bash
$ pip3 install pysvd
```

Install latest master from [GitHub](https://github.com/bfueldner/pysvd):

```bash
$ pip3 install https://github.com/bfueldner/pysvd/archive/master.zip
```

If you want to be able to change the code while using it, clone it and install the required pip packages:

```bash
$ git clone https://github.com/bfueldner/pysvd.git
$ cd pysvd
$ pip3 install -e .
```

## Script

On example of the parser is the script `svd_duplicates` to check a SVD file for possible duplicate `peripherals`, `registers`, `fields` and `enumeratedValues`:

```bash
$ svd_duplicate --help
usage: svd_duplicates [-h] --svd FILE [--output FILE] [--level {all,hint,warning}] [--depth {peripherals,registers,fields,enumeratedValues}] [--sort]

Read SVD file, order elements, check forvalid elements to generate register access structs and displays possible substitutions.

optional arguments:
  -h, --help            show this help message and exit
  --svd FILE            System view description (SVD) file
  --output FILE, -o FILE
                        Save ordered SVD output file
  --level {all,hint,warning}, -l {all,hint,warning}
                        Select level of output messages
  --depth {peripherals,registers,fields,enumeratedValues}, -d {peripherals,registers,fields,enumeratedValues}
                        Select depth of analysis
  --sort                Sort elements before comparing
```

Running `svd_duplicates` on a STM32F407 definition would generate this output (cut):

![svd_duplicates console output](doc/images/svd_duplicates_console.png)

## Example

As another example of the parser, a "SVD to ReST" converter `svd2rst` is included as a command line tool:

```bash
$ svd2rst --help
usage: svd2rst [-h] --svd FILE --output FILE

SVD to ReST converter

optional arguments:
  -h, --help              show this help message and exit
  --svd FILE              System view description (SVD) file
  --output FILE, -o FILE  ReST output file
  --version               show program's version number and exit
```

Running `svd2rst` on a Cortex-M3 core definition would generate this output:

```rst
Device
======

:Name: ARMCM3
:Description: ARM 32-bit Cortex-M3 Microcontroller based device, CPU clock up to 80MHz, etc.
:Series: ARMCM
:Version: 1.2
:Vendor: ARM Ltd.

:Address unit bits: 8
:Data width: 32

CPU
===

:Name: Cortex-M3
:Revision: r2p1
:Endian: little
:MPU: no
:FPU: no
:VTOR: yes
:Interrupts: 16
:Interrupt priorities: 16
:Vendor SYSTICK: no

Memory mapping
==============

========== ==========
Peripheral  Address
========== ==========
SYSTICK_   0xE000E010
NVIC_      0xE000E100
SCB_       0xE000ED00
MPU_       0xE000ED90
========== ==========

Interrupt mapping
=================

========== =========
Peripheral Interrupt
========== =========
SCB_       1
SYSTICK_   15
========== =========

Peripheral
==========

.. _SYSTICK:

System timer register (SYSTICK)
-------------------------------

:Address: 0xE000E010
:Size: 0x0010
:Usage: registers
:Interrupt: 15

========================= ======
      Register          Offset
========================= ======
`CSR <SYSTICK.CSR_>`_     0x00
`RVR <SYSTICK.RVR_>`_     0x04
`CVR <SYSTICK.CVR_>`_     0x08
`CALIB <SYSTICK.CALIB_>`_ 0x0C
========================= ======

.. _SYSTICK.CSR:

Control and Status Register
^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Name: CSR
:Size: 32
:Offset: 0x00
:Reset: 0x00000000
:Access: read-write

- Bit 0 (read-write) - ENABLE
 Enable Timer

- Bit 1 (read-write) - TICKINT
 Generate Exception

- Bit 2 (read-write) - CLKSOURCE
 Clock source

 - 0 - EXTERNAL
    External Clock
 - 1 - PROCESSOR
    CPU Clock

- Bit 16 (read-write) - COUNTFLAG
 Counted to zero

.. _SYSTICK.RVR:

Reload Value Register
^^^^^^^^^^^^^^^^^^^^^

:Name: RVR
:Size: 32
:Offset: 0x04
:Reset: 0x00000000
:Access: read-write

- Bits 23:0 (read-write) - RELOAD
 Reload value for CVR when counter reaches zero

.. _SYSTICK.CVR:

Current Value Register
^^^^^^^^^^^^^^^^^^^^^^

:Name: CVR
:Size: 32
:Offset: 0x08
:Reset: 0x00000000
:Access: read-write

- Bits 31:0 (read-write) - CURRENT
 Current counter value

.. _SYSTICK.CALIB:

Calibration Value Register
^^^^^^^^^^^^^^^^^^^^^^^^^^

:Name: CALIB
:Size: 32
:Offset: 0x0C
:Reset: 0x00000000
:Access: read-only

- Bits 23:0 (read-only) - TENMS
 Reload value to use for 10ms timing

- Bit 30 (read-only) - SKEW
 Clock Skew

 - 0 - EXACT
    10ms calibration value is exact
 - 1 - INEXACT
    10ms calibration value is inexact, because of the clock frequency

- Bit 31 (read-only) - NOREF
 No Ref

 - 0 - AVAILABLE
    Reference clock available
 - 1 - UNAVAILABLE
    Reference clock is not available

...
```