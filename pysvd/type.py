"""SVD types from XSD schema file v1.3.3

Note: Type order taken from XSD file.
"""

from enum import Enum


class cpuName(Enum):
    """Specifies a selection of Cortex-M and Secure-Cores. This list will get
    extended as new processors are released.
    """

    CM0 = 'CM0'
    CM0PLUS = 'CM0PLUS'
    CM1 = 'CM1'
    SC000 = 'SC000'
    CM23 = 'CM23'
    CM3 = 'CM3'
    CM33 = 'CM33'
    CM35P = 'CM35P'
    SC300 = 'SC300'
    CM4 = 'CM4'
    CM7 = 'CM7'
    ARMV8MML = 'ARMV8MML'
    ARMV8MBL = 'ARMV8MBL'
    CA5 = 'CA5'
    CA7 = 'CA7'
    CA8 = 'CA8'
    CA9 = 'CA9'
    CA15 = 'CA15'
    CA17 = 'CA17'
    CA53 = 'CA53'
    CA57 = 'CA57'
    CA72 = 'CA72'
    other = 'other'

    def __str__(self):
        return self.value


# revision
# Specifies the CPU revision format as defined by ARM (rNpM)


class endian(Enum):
    """Pre-defines the tokens for specifying the endianess of the device"""

    little = 'little'
    big = 'big'
    selectable = 'selectable'
    other = 'other'

    def __str__(self):
        return self.value


class dataType(Enum):
    """Pre-defines the tokens in line with CMSIS data type definitions"""

    uint8_t = 'uint8_t'
    uint16_t = 'uint16_t'
    uint32_t = 'uint32_t'
    uint64_t = 'uint64_t'
    int8_t = 'int8_t'
    int16_t = 'int16_t'
    int32_t = 'int32_t'
    int64_t = 'int64_t'

    uint8_t_ptr = 'uint8_t *'
    uint16_t_ptr = 'uint16_t *'
    uint32_t_ptr = 'uint32_t *'
    uint64_t_ptr = 'uint64_t *'
    int8_t_ptr = 'int8_t *'
    int16_t_ptr = 'int16_t *'
    int32_t_ptr = 'int32_t *'
    int64_t_ptr = 'int64_t *'

    def __str__(self):
        return self.value


# nvicPrioBits
# Specifies the integer value range for the number of bits used in NVIC to
# encode priority levels


# dimableIdentifier
# Specifies the subset and sequence of characters used for specifying
# identifiers that may contain %s from dim. This is particularly important as
# these are used in ANSI C Structures during the device header file generation.


# identifier
# Specifies the subset and sequence of characters used for specifying
# identifiers that must not contain %s from dim. This is particularly
# important as these are used in ANSI C Structures during the device header
# file generation.


class protection(Enum):
    """V1.3: Protection Access Attribute Strings"""

    none = ''
    secure = 's'
    non_secure = 'n'
    privileged = 'p'

    def __str__(self):
        return self.name.replace('_', '-')


class sauAccess(Enum):
    """V1.3: SAU Access Type"""

    none = ''
    non_secure_callable_secure = 'c'
    non_secure = 'n'

    def __str__(self):
        return self.name.replace('_', '-')


# dimIndex
# Specifies the subset and sequence of characters used for specifying the
# sequence of indices in register arrays


# scaledNonNegativeInteger
# Specifies the format in which numbers are represented in hexadecimal or
# decimal format


# enumeratedValueData
# Specifies the number formats for the values in enumeratedValues


class access(Enum):
    """Specfies the pre-defined tokens for the available accesses"""

    read_only = 'read-only'
    write_only = 'write-only'
    read_write = 'read-write'
    writeOnce = 'writeOnce'
    read_writeOnce = 'read-writeOnce'

    def __str__(self):
        return self.value


class modifiedWriteValues(Enum):
    """Specifies the pre-defined tokens for the write side effects"""

    oneToClear = 'oneToClear'
    oneToSet = 'oneToSet'
    oneToToggle = 'oneToToggle'
    zeroToClear = 'zeroToClear'
    zeroToSet = 'zeroToSet'
    zeroToToggle = 'zeroToToggle'
    clear = 'clear'
    set = 'set'
    modify = 'modify'

    def __str__(self):
        return self.value


class readAction(Enum):
    """Specifies the pre-defined tokens for read side effects"""

    clear = 'clear'
    set = 'set'
    modify = 'modify'
    modifyExternal = 'modifyExternal'

    def __str__(self):
        return self.value


class enumUsage(Enum):
    """Specifies the pre-defined tokens for selecting what access types an
    enumeratedValues set is associated with
    """

    read = 'read'
    write = 'write'
    read_write = 'read-write'

    def __str__(self):
        return self.value


class addressBlockUsage(Enum):
    registers = 'registers'
    buffer = 'buffer'
    reserved = 'reserved'

    def __str__(self):
        return self.value
