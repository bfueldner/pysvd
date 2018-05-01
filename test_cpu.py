from model import cpu

import xml.etree.ElementTree as ET

if __name__ == "__main__":
    node = ET.parse("test_cpu.svd").getroot()
    test_cpu = cpu(None, node)

    print("{}".format(test_cpu.name))
    print("{}".format(test_cpu.revision))
    print("{}".format(test_cpu.endian))
    print("{}".format(test_cpu.mpu_present))
