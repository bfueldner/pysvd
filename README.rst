.. image:: https://img.shields.io/pypi/v/pysvd
    :target: https://pypi.org/project/pysvd
    :alt: Latest version on PyPi

.. image:: https://img.shields.io/pypi/pyversions/pysvd
    :target: https://pypi.org/project/pysvd
    :alt: Python versions

.. image:: https://img.shields.io/pypi/l/pysvd
    :target: https://pypi.org/project/pysvd
    :alt: License

.. image:: https://travis-ci.org/bfueldner/pysvd.svg?branch=master
    :target: https://travis-ci.org/bfueldner/pysvd
    :alt: Build state

.. image:: https://coveralls.io/repos/github/bfueldner/pysvd/badge.svg?branch=master
    :target: https://coveralls.io/github/bfueldner/pysvd?branch=master
    :alt: Coverage


pysvd
=====

A **S**\ ystem **V**\ iew **D**\ escription v1.3.3 parser package for Python 3.4+.


Motivation
----------

SVD is a greate format to develop embedded systems on. Existing parser out in the field did not support all features (derive, dimension) supported by the format.

With the parsed system view tree, you can several cool things:

* Automatic register generation (BSP skeleton)
* Linker file generation
* GDB register debug symbol generation
* Custom datasheet generation


Conformance
-----------

This parser is build to reflect 1:1 the XSD format behind SVD. The only compromis has been made by the nodes ``peripherals``, ``registers`` and ``fields`` that are simple container objects.

The node names and attributes follow the same naming convention in XML as in Python to map them easier between the languages.


Installation
------------

Install from PyPI_ using pip::

    $ pip3 install pysvd

Install latest master from GitHub_::

    $ pip3 install https://github.com/bfueldner/pysvd/archive/master.zip

If you want to be able to change the code while using it, clone it and install the required pip packages::

    $ git clone https://github.com/bfueldner/pysvd.git
    $ cd pysvd
    $ pip3 install -e .

.. _PyPi: https://pypi.org
.. _GitHub: https://github.com/bfueldner/pysvd


Example
-------

As an example of the parser, a "SVD to ReST" converter ``svd2rst`` is included as a command line tool::

    $ svd2rst --help
    usage: svd2rst [-h] --svd FILE --output FILE

    SVD to ReST converter

    optional arguments:
        -h, --help     show this help message and exit
        --svd FILE     System view description (SVD) file
        --output FILE  ReST output file

Running ``svd2rst`` on a Cortex-M3 core definition would generate this output::

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
