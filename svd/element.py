import svd.node
import svd.parser
import svd.classes
import svd.type

# https://www.python-course.eu/python3_inheritance.php
# https://docs.python.org/3/library/enum.html

# Base classes
class sau_regions_config_region(svd.classes.parent):
    '''Define the regions of the Secure Attribution Unit (SAU)'''

    def __init__(self, parent, node):
    #    if not isinstance(parent, sau_region_config):
    #        raise TypeError("Only parent 'sau_region_config' allowed")
        svd.classes.parent.__init__(self, parent)

        attr = {}
        attr['enabled'] = svd.parser.boolean(svd.node.attribute(node, 'enabled'), True)
        attr['name'] = svd.parser.text(svd.node.attribute(node, 'name'))

        attr['base'] = svd.parser.integer(svd.node.element(node, 'base', True))
        attr['limit'] = svd.parser.integer(svd.node.element(node, 'limit', True))
        attr['access'] = svd.parser.enum(svd.type.region_access, svd.node.element(node, 'access', True))
        self.add_attributes(attr)

class sau_region_config(svd.classes.group):
    '''Set the configuration for the Secure Attribution Unit (SAU) when they are preconfigured by HW or Firmware.'''

    attributes = ['protection']

    def __init__(self, parent, node):
    #    if not isinstance(parent, cpu):
    #        raise TypeError("Only parent 'cpu' allowed")
        svd.classes.group.__init__(self, parent)

        attr = {}
        attr['enabled'] = svd.parser.boolean(svd.node.attribute(node, 'enabled'))
        attr['protection'] = svd.parser.enum(svd.type.protection, svd.node.element(node, 'protectionWhenDisabled'))
        self.add_attributes(attr)

        self.region = []
        for child in node.findall('region'):
            self.region.append( sau_regions_config_region(self, child) )

class cpu(svd.classes.parent):
    '''The CPU section describes the processor included in the microcontroller device.'''

    def __init__(self, parent, node):
    #    if not isinstance(parent, device):
    #        raise TypeError("Only parent 'device' allowed")
        svd.classes.parent.__init__(self, parent)

        attr = {}
        attr['name'] = svd.parser.enum(svd.type.cpu_name, svd.node.element(node, 'name', True))
        attr['revision'] = svd.parser.text(svd.node.element(node, 'revision', True))
        attr['endian'] = svd.parser.enum(svd.type.endian, svd.node.element(node, 'endian', True))
        attr['mpu_present'] = svd.parser.boolean(svd.node.element(node, 'mpuPresent', True))
        attr['fpu_present'] = svd.parser.boolean(svd.node.element(node, 'fpuPresent', True))

        attr['fpu_dp'] = svd.parser.boolean(svd.node.element(node, 'fpuDP'))
        attr['icache_present'] = svd.parser.boolean(svd.node.element(node, 'icachePresent'))
        attr['dcache_present'] = svd.parser.boolean(svd.node.element(node, 'dcachePresent'))
        attr['itcm_present'] = svd.parser.boolean(svd.node.element(node, 'itcmPresent'))
        attr['dtcm_present'] = svd.parser.boolean(svd.node.element(node, 'dtcmPresent'))
        attr['vtor_present'] = svd.parser.boolean(svd.node.element(node, 'vtorPresent'), True)

        attr['nvic_prio_bits'] = svd.parser.integer(svd.node.element(node, 'nvicPrioBits', True))
        attr['vendor_systick_config'] = svd.parser.boolean(svd.node.element(node, 'vendorSystickConfig', True))

        attr['device_num_interrupts'] = svd.parser.integer(svd.node.element(node, 'deviceNumInterrupts'))
        attr['sau_num_regions'] = svd.parser.integer(svd.node.element(node, 'sauNumRegions'))
        self.add_attributes(attr)

        child = node.find('sauRegionsConfig')
        if child is not None:
            self.sau_regions_config = sau_region_config(self, child)
