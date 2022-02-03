"""SVD elements from XSD schema file v1.3.3
"""
import re
import pysvd


def compare_attribute(lhs, rhs, attibute):
    """Compare attibute of objects.
    """
    if hasattr(lhs, attibute) != hasattr(rhs, attibute):
        return False

    if hasattr(lhs, attibute):
        return getattr(lhs, attibute) == getattr(rhs, attibute)

    return True

# /device
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_device.html
class Device(pysvd.classes.Base):
    """The element <device> provides the outermost frame of the description.

    * Only one <device> section is allowed per file. All other elements are described within this scope.
    * A <device> contains one or more peripherals, but one <cpu> description.
    * Optional elements such as <size>, <access>, or <resetValue> defined on this level represent default values for registers and can be
      refined at lower levels.
    """

    def __init__(self, node):
        self.peripherals = []

        super().__init__(node)

    def parse(self, node):
        super().parse(node)

        self.__dict__['schemaVersion'] = pysvd.parser.Text(pysvd.node.Attribute(node, 'schemaVersion', True))

        self.add_attribute(node, 'vendor', pysvd.parser.Text)
        self.add_attribute(node, 'vendorID', pysvd.parser.Text)
        self.add_attribute(node, 'name', pysvd.parser.Text, True)
        self.add_attribute(node, 'series', pysvd.parser.Text)
        self.add_attribute(node, 'version', pysvd.parser.Text, True)
        self.add_attribute(node, 'description', pysvd.parser.Text, True)
        self.add_attribute(node, 'licenseText', pysvd.parser.Text)
        self.add_attribute(node, 'headerSystemFilename', pysvd.parser.Text)
        self.add_attribute(node, 'headerDefinitionsPrefix', pysvd.parser.Text)
        self.add_attribute(node, 'addressUnitBits', pysvd.parser.Integer, True)
        self.add_attribute(node, 'width', pysvd.parser.Integer, True)

        # property group
        self.add_attribute(node, 'size', pysvd.parser.Integer, False, 32)
        self.add_enum_attribute(node, 'access', pysvd.type.access, False, pysvd.type.access.read_write)
        self.add_enum_attribute(node, 'protection', pysvd.type.protection, False, pysvd.type.protection.none)
        self.add_attribute(node, 'resetValue', pysvd.parser.Integer, False, 0x00000000)
        self.add_attribute(node, 'resetMask', pysvd.parser.Integer, False, 0xFFFFFFFF)

        # Clean up license text from whitespaces
        result = ''
        if hasattr(self, 'licenseText'):
            for line in self.licenseText.splitlines():
                line = line.strip()
                if len(line):
                    result += line + '\n'
            self.licenseText = result

        cpu_node = node.find('cpu')
        if cpu_node is not None:
            self.cpu = pysvd.element.Cpu(self, cpu_node)

        peripherals_node = node.find('./peripherals')
        if peripherals_node is None:
            raise SyntaxError("No element 'peripherals' found in 'device'")

        Peripheral.add_elements(self, self.peripherals, peripherals_node, 'peripheral')
        if len(self.peripherals) < 1:
            raise SyntaxError("At least one element of 'peripheral' is mandatory in 'peripherals'")

    def find(self, name):
        """Find peripheral by name."""
        for peripheral in self.peripherals:
            if peripheral.name == name:
                return peripheral
        return None


# /device/cpu
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_cpu.html
class Cpu(pysvd.classes.Parent):
    """The CPU section describes the processor included in the microcontroller device. This section is mandatory if the SVD file is used to
    generate the device header file.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        self.__dict__['name'] = pysvd.parser.Enum(pysvd.type.cpuName, pysvd.node.Element(node, 'name', True).replace('+', 'PLUS'))
        self.add_attribute(node, 'revision', pysvd.parser.Text, True)
        self.add_enum_attribute(node, 'endian', pysvd.type.endian, True)
        self.add_attribute(node, 'mpuPresent', pysvd.parser.Boolean, True)
        self.add_attribute(node, 'fpuPresent', pysvd.parser.Boolean, True)
        self.add_attribute(node, 'fpuDP', pysvd.parser.Boolean)
        self.add_attribute(node, 'dspPresent', pysvd.parser.Boolean)
        self.add_attribute(node, 'icachePresent', pysvd.parser.Boolean)
        self.add_attribute(node, 'dcachePresent', pysvd.parser.Boolean)
        self.add_attribute(node, 'itcmPresent', pysvd.parser.Boolean)
        self.add_attribute(node, 'dtcmPresent', pysvd.parser.Boolean)
        self.add_attribute(node, 'vtorPresent', pysvd.parser.Boolean, False, True)

        self.add_attribute(node, 'nvicPrioBits', pysvd.parser.Integer, True)
        self.add_attribute(node, 'vendorSystickConfig', pysvd.parser.Boolean, True)

        self.add_attribute(node, 'deviceNumInterrupts', pysvd.parser.Integer)
        self.add_attribute(node, 'sauNumRegions', pysvd.parser.Integer)

        sau_regions_config_node = node.find('./sauRegionsConfig')
        if sau_regions_config_node is not None:
            self.sauRegionsConfig = SauRegionConfig(self, sau_regions_config_node)


# /device/cpu/sauRegionsConfig
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_cpu.html#elem_sauRegionsConfig
class SauRegionConfig(pysvd.classes.Group):
    """Set the configuration for the Secure Attribution Unit (SAU) when they are preconfigured by HW or Firmware.
    """

    attributes = ['protectionWhenDisabled']

    def __init__(self, parent, node):
        self.regions = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        enabled = pysvd.parser.Boolean(pysvd.node.Attribute(node, 'enabled'))
        if enabled is not None:
            self.__dict__['enabled'] = enabled

        protectionWhenDisabled = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Attribute(node, 'protectionWhenDisabled'))
        if protectionWhenDisabled is not None:
            self.__dict__['protectionWhenDisabled'] = protectionWhenDisabled

        for sau_regions_config_region_node in node.findall('region'):
            self.regions.append(SauRegionsConfigRegion(self, sau_regions_config_region_node))


# /device/cpu/sauRegionsConfig/region
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_cpu.html#elem_region
class SauRegionsConfigRegion(pysvd.classes.Parent):
    """Define the regions of the Secure Attribution Unit (SAU). The protection level is inherited from the attribute
    <protectionWhenDisabled> of the enclosing element sauRegionsConfig.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        self.__dict__['enabled'] = pysvd.parser.Boolean(pysvd.node.Attribute(node, 'enabled'), True)
        name = pysvd.parser.Text(pysvd.node.Attribute(node, 'name'))
        if name is not None:
            self.__dict__['name'] = name

        self.add_attribute(node, 'base', pysvd.parser.Integer, True)
        self.add_attribute(node, 'limit', pysvd.parser.Integer, True)
        self.add_enum_attribute(node, 'access', pysvd.type.sauAccess, True)


# /device/peripherals
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html
# All peripherals of a device are enclosed within the tag <peripherals>.
#
# Note: This level is skipped for better readability

# /device/peripherals/peripheral
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html#elem_peripheral
class Peripheral(pysvd.classes.Dim):
    """At least one peripheral has to be defined.

    * Each peripheral describes all registers belonging to that peripheral.
    * The address range allocated by a peripheral is defined through one or more address blocks.
    * An address block and register addresses are specified relative to the base address of a peripheral. The address block information can
      be used for constructing a memory map for the device peripherals.

    Starting version 1.3 of the SVD specification, arrays of peripherals can be specified. The single peripheral description gets
    duplicated automatically into an array. The number of array elements is specified by the <dim> element. To define arrays, the <name>
    needs the format myPeripheral[%s]. The tag <dimIncrement> specifies the address offset between two peripherals. To create copies of a
    peripheral using different names, you must use the derivedFrom attribute.
    """

    def __init__(self, parent, node):
        self.addressBlocks = []
        self.registers = []
        self.clusters = []

        super().__init__(parent, node)

    def __eq__(self, other):
        """Compare element and all attributes.
        """
        if not isinstance(other, Peripheral):
            return NotImplemented

        if not self.equal_struct(other):
            return False

        return compare_attribute(self, other, 'name') and \
            compare_attribute(self, other, 'description') and \
            compare_attribute(self, other, 'version') and \
            compare_attribute(self, other, 'alternatePeripheral') and \
            compare_attribute(self, other, 'groupName') and \
            compare_attribute(self, other, 'prependToName') and \
            compare_attribute(self, other, 'appendToName') and \
            compare_attribute(self, other, 'headerStructName') and \
            compare_attribute(self, other, 'disableCondition') and \
            compare_attribute(self, other, 'baseAddress') and \
            compare_attribute(self, other, 'addressBlock') and \
            compare_attribute(self, other, 'interrupt')

    def equal_struct(self, other):
        """Compare only child elements.
        """
        if not isinstance(other, Peripheral):
            return NotImplemented

        if len(self.registers) != len(other.registers):
            return False

        for (lhs, rhs) in zip(self.registers, other.registers):
            if lhs != rhs:
                return False

        if len(self.clusters) != len(other.clusters):
            return False

        for (lhs, rhs) in zip(self.clusters, other.clusters):
            if lhs != rhs:
                return False
        return True

    def set_offset(self, value):
        self.baseAddress += value

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'version', pysvd.parser.Text)
        self.add_attribute(node, 'alternatePeripheral', pysvd.parser.Text)
        self.add_attribute(node, 'groupName', pysvd.parser.Text)
        self.add_attribute(node, 'prependToName', pysvd.parser.Text)
        self.add_attribute(node, 'appendToName', pysvd.parser.Text)
        self.add_attribute(node, 'headerStructName', pysvd.parser.Text)
        self.add_attribute(node, 'disableCondition', pysvd.parser.Text)
        self.add_attribute(node, 'baseAddress', pysvd.parser.Integer, True)

        AddressBlock.add_elements(self, self.addressBlocks, node, 'addressBlock')

        self.interrupts = []
        Interrupt.add_elements(self, self.interrupts, node, 'interrupt')

        registers_node = node.find('./registers')
        if registers_node is not None:
            Register.add_elements(self, self.registers, registers_node, 'register')
            Cluster.add_elements(self, self.clusters, registers_node, 'cluster')

            if len(self.registers) < 1 and len(self.clusters) < 1:
                raise SyntaxError("At least one element of 'register' or 'cluster' is mandatory in 'registers'")

    def find(self, name):
        """Find cluster and register by name."""
        for cluster in self.clusters:
            if cluster.name == name:
                return cluster

        for register in self.registers:
            if register.name == name:
                return register
        return None


# /device/peripherals/peripheral/addressBlock
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html#elem_addressBlock
class AddressBlock(pysvd.classes.Group):
    """Specify an address range uniquely mapped to this peripheral. A peripheral must have at least one address block. If a peripheral is
    derived form another peripheral, the <addressBlock> is not mandatory.
    """

    attributes = ['protection']

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'offset', pysvd.parser.Integer, True)
        self.add_attribute(node, 'size', pysvd.parser.Integer, True)
        self.add_enum_attribute(node, 'usage', pysvd.type.addressBlockUsage, True)
        self.add_enum_attribute(node, 'protection', pysvd.type.protection)


# /device/peripherals/peripheral/interrupt
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html#elem_interrupt
class Interrupt(pysvd.classes.Parent):
    """A peripheral can have multiple interrupts. This entry allows the debugger to show interrupt names instead of interrupt numbers.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text, True)
        self.add_attribute(node, 'description', pysvd.parser.Text)
        self.add_attribute(node, 'value', pysvd.parser.Integer, True)


# /device/peripherals/peripheral/registers
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html
# All registers of a peripheral are enclosed between the <registers> opening and closing tags. Clusters define a set of registers. You can
# either use the <cluster> or the <register> element.
#
# Note: This level is skipped for better readability


# /device/pripherals/peripheral/registers/.../cluster
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_cluster
class Cluster(pysvd.classes.Dim):
    """Cluster describes a sequence of neighboring registers within a peripheral. A <cluster> specifies the addressOffset relative to the
    baseAddress of the grouping element. All <register> elements within a <cluster> specify their addressOffset relative to the cluster
    base address (<peripheral.baseAddress> + <cluster.addressOffset>).

    Multiple <register> and <cluster> sections may occur in any order. Since version 1.3 of the specification, the nesting of <cluster>
    elements is supported. Nested clusters express hierarchical structures of registers. It is predominantely targeted at the generation of
    device header files to create a C-data structure within the peripheral structure instead of a flat list of registers. Note, you can
    also specify an array of a cluster using the <dim> element.
    """

    def __init__(self, parent, node):
        self.registers = []
        self.clusters = []

        super().__init__(parent, node)

    def set_offset(self, value):
        self.addressOffset += value

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text, True)
        self.add_attribute(node, 'description', pysvd.parser.Text, self.derivedFrom is not None)
        self.add_attribute(node, 'alternateCluster', pysvd.parser.Text)
        self.add_attribute(node, 'headerStructName', pysvd.parser.Text)
        self.add_attribute(node, 'addressOffset', pysvd.parser.Integer, True)

        self.add_attribute(node, 'size', pysvd.parser.Integer)
        self.add_enum_attribute(node, 'access', pysvd.type.access)
        self.add_enum_attribute(node, 'protection', pysvd.type.protection)
        self.add_attribute(node, 'resetValue', pysvd.parser.Integer)
        self.add_attribute(node, 'resetMask', pysvd.parser.Integer)

        Register.add_elements(self, self.registers, node, 'register')
        Cluster.add_elements(self, self.clusters, node, 'cluster')

    def find(self, name):
        """Find cluster and register by name."""
        for cluster in self.clusters:
            if cluster.name == name:
                return cluster

        for register in self.registers:
            if register.name == name:
                return register
        return None


# /device/peripherals/peripheral/registers/.../register
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_register
class Register(pysvd.classes.Dim):
    """The description of registers is the most essential part of SVD. If the elements <size>, <access>, <resetValue>, and <resetMask>
    have not been specified on a higher level, then these elements are mandatory on register level.

    A register can represent a single value or can be subdivided into individual bit-fields of specific functionality and semantics. From
    a schema perspective, the element <fields> is optional, however, from a specification perspective, <fields> are mandatory when they are
    described in the device documentation.

    You can define register arrays where the single description gets duplicated automatically. The size of the array is specified by the
    <dim> element. Register names get composed by the element <name> and the index-specific string defined in <dimIndex>. The element
    <dimIncrement> specifies the address offset between two registers.
    """

    def __init__(self, parent, node):
        self.fields = []

        super().__init__(parent, node)

    def __eq__(self, other):
        """Compare element and all attributes.
        """
        if not isinstance(other, Register):
            return NotImplemented

        if not self.equal_struct(other):
            return False

        return compare_attribute(self, other, 'name') and \
            compare_attribute(self, other, 'displayName') and \
            compare_attribute(self, other, 'description') and \
            compare_attribute(self, other, 'alternateGroup') and \
            compare_attribute(self, other, 'alternateRegister') and \
            compare_attribute(self, other, 'addressOffset') and \
            compare_attribute(self, other, 'size') and \
            compare_attribute(self, other, 'access') and \
            compare_attribute(self, other, 'protection') and \
            compare_attribute(self, other, 'resetValue') and \
            compare_attribute(self, other, 'resetMask') and \
            compare_attribute(self, other, 'dataType') and \
            compare_attribute(self, other, 'modifiedWriteValues') and \
            compare_attribute(self, other, 'readAction')

    def equal_struct(self, other):
        """Compare only child elements.
        """
        if not isinstance(other, Register):
            return NotImplemented

        if len(self.fields) != len(other.fields):
            return False

        for (lhs, rhs) in zip(self.fields, other.fields):
            if lhs != rhs:
                return False
        return True

    def set_offset(self, value):
        self.addressOffset += value

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text, True)
        self.add_attribute(node, 'displayName', pysvd.parser.Text)
        self.add_attribute(node, 'description', pysvd.parser.Text, self.derivedFrom is not None)
        self.add_attribute(node, 'alternateGroup', pysvd.parser.Text)
        self.add_attribute(node, 'alternateRegister', pysvd.parser.Text)
        self.add_attribute(node, 'addressOffset', pysvd.parser.Integer, True)

        self.add_attribute(node, 'size', pysvd.parser.Integer)
        self.add_enum_attribute(node, 'access', pysvd.type.access)
        self.add_enum_attribute(node, 'protection', pysvd.type.protection)
        self.add_attribute(node, 'resetValue', pysvd.parser.Integer)
        self.add_attribute(node, 'resetMask', pysvd.parser.Integer)

        self.add_enum_attribute(node, 'dataType', pysvd.type.dataType)
        self.add_enum_attribute(node, 'modifiedWriteValues', pysvd.type.modifiedWriteValues, False, pysvd.type.modifiedWriteValues.modify)
        self.add_enum_attribute(node, 'readAction', pysvd.type.readAction)

        write_constraint_node = node.find('./writeConstraint')
        if write_constraint_node is not None:
            self.writeConstraint = WriteConstraint(self, write_constraint_node)

        fields_node = node.find('./fields')
        if fields_node is not None:
            Field.add_elements(self, self.fields, fields_node, 'field')

            if len(self.fields) < 1:
                raise SyntaxError("At least one element of 'field' is mandatory in 'fields'")

    def find(self, name):
        """Find field by name."""
        for field in self.fields:
            if field.name == name:
                return field
        return None


# /device/peripherals/peripheral/registers/.../register/.../writeConstraint
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_writeConstraint
class WriteConstraint(pysvd.classes.Parent):
    """Define constraints for writing values to a field. You can choose between three options, which are mutualy exclusive.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        writeAsRead = pysvd.node.Element(node, 'writeAsRead')
        useEnumeratedValues = pysvd.node.Element(node, 'useEnumeratedValues')
        range_node = node.find("./range")
        if writeAsRead is not None:
            self.__dict__['writeAsRead'] = pysvd.parser.Boolean(writeAsRead)
        elif useEnumeratedValues is not None:
            self.__dict__['useEnumeratedValues'] = pysvd.parser.Boolean(useEnumeratedValues)
        else:
            rangeMinimum = None
            rangeMaximum = None
            if range_node is not None:
                rangeMinimum = pysvd.node.Element(range_node, 'minimum')
                rangeMaximum = pysvd.node.Element(range_node, 'maximum')

            if rangeMinimum is None or rangeMaximum is None:
                raise SyntaxError("Either 'writeAsRead', 'useEnumeratedValues' or 'range' is mandatory in 'writeConstraint'")

            self.__dict__['rangeMinimum'] = pysvd.parser.Integer(rangeMinimum)
            self.__dict__['rangeMaximum'] = pysvd.parser.Integer(rangeMaximum)


# /device/peripherals/peripheral/registers/.../register/fields
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_fields
# Grouping element to define bit-field properties of a register.
#
# Note: This level is skipped for better readability


# /device/peripherals/peripheral/registers/.../fields/field
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_field
class Field(pysvd.classes.Dim):
    """All fields of a register are enclosed between the <fields> opening and closing tags.

    A bit-field has a name that is unique within the register. The position and size within the register can be decsribed in two ways:
    * by the combination of the least significant bit's position (lsb) and the most significant bit's position (msb), or
    * the lsb and the bit-width of the field.

    A field may define an enumeratedValue in order to make the display more intuitive to read.
    """

    attributes = ['access']

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def __eq__(self, other):
        if not isinstance(other, Field):
            return NotImplemented

        if not self.equal_struct(other):
            return False

        return compare_attribute(self, other, 'name') and \
            compare_attribute(self, other, 'description') and \
            compare_attribute(self, other, 'bitOffset') and \
            compare_attribute(self, other, 'bitWidth') and \
            compare_attribute(self, other, 'access') and \
            compare_attribute(self, other, 'modifiedWriteValues') and \
            compare_attribute(self, other, 'readAction') and \
            compare_attribute(self, other, 'writeConstraint')

    def equal_struct(self, other):
        """Check structure elements, but not overridable attributes.
        """
        if not isinstance(other, Field):
            return NotImplemented

        return compare_attribute(self, other, 'enumeratedValues')

        x = """
        if len(self.enumeratedValues) != len(other.enumeratedValues):
            return False

        for (lhs, rhs) in zip(self.enumeratedValues, other.enumeratedValues):
            if lhs != rhs:
                return False
        return True
        """


    def set_offset(self, value):
        self.bitOffset += value

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text, True)
        self.add_attribute(node, 'description', pysvd.parser.Text, self.derivedFrom is not None)

        # bitRangeOffsetWidthStyle
        bitOffset = pysvd.parser.Integer(pysvd.node.Element(node, 'bitOffset'))
        bitWidth = pysvd.parser.Integer(pysvd.node.Element(node, 'bitWidth'))
        if bitOffset is not None:
            # If bitWidth is not set, default is 1
            bitWidth = 1 if bitWidth is None else bitWidth
        else:
            # bitRangeLsbMsbStyle
            lsb = pysvd.parser.Integer(pysvd.node.Element(node, 'lsb'))
            msb = pysvd.parser.Integer(pysvd.node.Element(node, 'msb'))
            if lsb is None or msb is None:
                bitRange = pysvd.parser.Text(pysvd.node.Element(node, 'bitRange'))
                if bitRange is None:
                    raise ValueError("Field '{}' has no valid bit-range".format(self.name if hasattr(self, 'name') else '<unknown>'))

                match = re.search(r'\[([0-9]+):([0-9]+)\]', bitRange)
                lsb = int(match.group(2))
                msb = int(match.group(1))

            bitOffset = lsb
            bitWidth = (msb - lsb) + 1

        self.__dict__['bitOffset'] = bitOffset
        self.__dict__['bitWidth'] = bitWidth

        self.add_enum_attribute(node, 'access', pysvd.type.access)
        self.add_enum_attribute(node, 'modifiedWriteValues', pysvd.type.modifiedWriteValues, False, pysvd.type.modifiedWriteValues.modify)
        self.add_enum_attribute(node, 'readAction', pysvd.type.readAction)

        write_constraint_node = node.find('./writeConstraint')
        if write_constraint_node is not None:
            self.writeConstraint = WriteConstraint(self, write_constraint_node)

        enumerated_values_node = node.find('./enumeratedValues')
        if enumerated_values_node is not None:
            self.enumeratedValues = EnumeratedValues(self, enumerated_values_node)

    def find(self, name):
        """Find enumeratedValues by name."""
        if hasattr(self, 'enumeratedValues') and hasattr(self.enumeratedValues, 'name') and self.enumeratedValues.name == name:
            return self.enumeratedValues
        return None


# /device/peripherals/peripheral/registers/.../field/enumeratedValues
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_enumeratedValues
class EnumeratedValues(pysvd.classes.Derive):
    """The concept of enumerated values creates a map between unsigned integers and an identifier string. In addition, a description string
    can be associated with each entry in the map.

    0 <-> disabled -> "The clock source clk0 is turned off."
    1 <-> enabled  -> "The clock source clk1 is running."
    2 <-> reserved -> "Reserved values. Do not use."
    3 <-> reserved -> "Reserved values. Do not use."

    This information generates an enum in the device header file. The debugger may use this information to display the identifier string as
    well as the description. Just like symbolic constants making source code more readable, the system view in the debugger becomes more
    instructive. The detailed description can provide reference manual level details within the debugger.
    """

    def __init__(self, parent, node):
        self.enumeratedValues = []

        super().__init__(parent, node)

    def __eq__(self, other):
        if not isinstance(other, EnumeratedValues):
            return NotImplemented

        if not self.equal_struct(other):
            return False

        return compare_attribute(self, other, 'name') and \
            compare_attribute(self, other, 'headerEnumName') and \
            compare_attribute(self, other, 'usage')

    def equal_struct(self, other):
        if not isinstance(other, EnumeratedValues):
            return NotImplemented

        if len(self.enumeratedValues) != len(other.enumeratedValues):
            return False

        for (lhs, rhs) in zip(self.enumeratedValues, other.enumeratedValues):
            if lhs != rhs:
                return False
        return True

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text)
        self.add_attribute(node, 'headerEnumName', pysvd.parser.Text)
        self.add_enum_attribute(node, 'usage', pysvd.type.enumUsage, False, pysvd.type.enumUsage.read_write)

        for child in node.findall('./enumeratedValue'):
            self.enumeratedValues.append(EnumeratedValue(self, child))

        if len(self.enumeratedValues) < 1:
            raise SyntaxError("At least one element of enumeratedValue is needed in enumeratedValues '{}'".format(
                self.name if hasattr(self, 'name') else '<unknown>'))


# /device/peripherals/peripheral/registers/.../enumeratedValue
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_enumeratedValue
class EnumeratedValue(pysvd.classes.Parent):
    """An enumeratedValue defines a map between an unsigned integer and a string.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def __eq__(self, other):
        if not isinstance(other, EnumeratedValue):
            return NotImplemented

        return compare_attribute(self, other, 'name') and \
            compare_attribute(self, other, 'value') and \
            compare_attribute(self, other, 'description') and \
            compare_attribute(self, other, 'isDefault')

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text)
        self.add_attribute(node, 'description', pysvd.parser.Text)
        self.add_attribute(node, 'value', pysvd.parser.Integer)
        self.add_attribute(node, 'isDefault', pysvd.parser.Boolean)

        if not hasattr(self, 'value') and not hasattr(self, 'isDefault'):
            raise SyntaxError("Either 'value' or 'isDefault' is mandatory in enumeratedValue '{}'".format(
                self.name if hasattr(self, 'name') else '<unknown>'))


# /device/peripherals/peripheral/.../dimArrayIndex
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_special.html#elem_dimArrayIndex
class DimArrayIndex(pysvd.classes.Parent):
    """This information is used for generating an enum in the device header file. The debugger may use this information to display the
    identifier string as well as the description. Just like symbolic constants making source code more readable, the system view in the
    debugger becomes more instructive.
    """

    def __init__(self, parent, node):
        self.enumeratedValues = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'headerEnumName', pysvd.parser.Text)

        for child in node.findall('./enumeratedValue'):
            self.enumeratedValues.append(EnumeratedValue(self, child))

        if len(self.enumeratedValues) < 1:
            raise SyntaxError("At least one element of enumeratedValue is needed in dimArrayIndex '{}'".format(
                self.headerEnumNames if hasattr(self, 'headerEnumName') else '<unknown>'))
