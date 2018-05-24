from enum import Enum

class access(Enum):
    read_only = 'read-only'
    write_only = 'write-only'
    read_write = 'read-write'
    write_once = 'writeOnce'
    read_write_once = 'read-writeOnce'

class cpu_name(Enum):
    cm0 = 'CM0'
    cm0plus = 'CM0PLUS'
#   cm0+ = 'CM0+'
    cm1 = 'CM1'
    sc000 = 'SC000'
    cm23 = 'CM23'
    cm3 = 'CM3'
    cm33 = 'CM33'
    sc300 = 'SC300'
    cm4 = 'CM4'
    cm7 = 'CM7'
    ca5 = 'CA5'
    ca7 = 'CA7'
    ca8 = 'CA8'
    ca9 = 'CA9'
    ca15 = 'CA15'
    ca17 = 'CA17'
    ca53 = 'CA53'
    ca57 = 'CA57'
    ca72 = 'CA72'
    other = 'other'

class endian(Enum):
    little = 'little'
    big = 'big'
    selectable = 'selectable'
    other = 'other'

class enum_usage(Enum):
    read = 'read'
    write = 'write'
    read_write = 'read-write'

class modified_write_values(Enum):
    one_to_clear = 'oneToClear'
    one_to_set = 'oneToSet'
    one_to_toggle = 'oneToToggle'
    zero_to_clear = 'zeroToClear'
    zero_to_set = 'zeroToSet'
    zero_to_toggle = 'zeroToToggle'
    clear = 'clear'
    set = 'set'
    modify = 'modify'

class protection(Enum):
    secure_callable = 's'
    non_secure = 'n'
    privileged = 'p'
    none = ''

class region_access(Enum):
    secure_callable = 'c'
    non_secure = 'n'
    none = ''

class read_action(Enum):
    clear = 'clear'
    set = 'set'
    modify = 'modify'
    modify_external = 'modifyExternal'

class usage(Enum):
    registers = 'registers'
    buffer = 'buffer'
    reserved = 'reserved'
