from model import register
from model import registers

import xml.etree.ElementTree as ET

if __name__ == "__main__":
    node = ET.parse("test_register_derive.svd").getroot()
    regs = registers(None, node)

    regs.find("TimerCtrl0").name
    regs.find("TimerCtrl1").name

    for reg in regs.register:
        print("{} /* {} */".format(reg.name, reg.description))
        print("Address offset: 0x{:08X}".format(reg.address_offset))
        print("Size: {:d}".format(reg.size))
        print("Access: {}".format(reg.access))
        print("Protection: {}".format(reg.protection))
        print("Reset value: 0x{:08X}".format(reg.reset_value))
        print("Reset mask: 0x{:08X}".format(reg.reset_mask))
        print("\n")
