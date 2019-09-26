#!/usr/bin/env python3
# coding: utf-8
"""
Read SVD file and generate C preprocessor definitions of registers.
"""

import argparse
import lxml.etree as et
import pysvd

DEFAULT_TYPE_PREFIX = 'uint'
DEFAULT_TYPE_SUFFIX = '_t'

xslt_template = """
<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" indent="yes" encoding="utf-8"/>
    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'"/>
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
    <xsl:template match="/">
#ifndef <xsl:value-of select="concat(translate(device/name, $lowercase, $uppercase), '_H')"/>
#define <xsl:value-of select="concat(translate(device/name, $lowercase, $uppercase), '_H')"/>
{header}
        <xsl:variable name="default_register_size" select="device/size"/>
        <xsl:for-each select="device/peripherals/peripheral">
            <xsl:variable name="peripheral_name" select="translate(name, $lowercase, $uppercase)"/>
            <xsl:variable name="peripheral_base" select="concat(translate(name, $lowercase, $uppercase), '_BASE_ADDRESS')"/>
            <xsl:variable name="peripheral_addr" select="baseAddress"/>
#define <xsl:value-of select="concat($peripheral_base, ' (', $peripheral_addr, 'u)')"/>
            <xsl:for-each select="registers">
                <xsl:for-each select="register">
                    <xsl:variable name="register_name" select="translate(name, $lowercase, $uppercase)"/>
                    <xsl:choose>
                        <xsl:when test="size">
                            <xsl:call-template name="define_register">
                                <xsl:with-param name="peripheral_name" select = "$peripheral_name" />
                                <xsl:with-param name="register_name" select="$register_name"/>
                                <xsl:with-param name="register_size" select="size"/>
                                <xsl:with-param name="base_address" select="$peripheral_base"/>
                                <xsl:with-param name="address_offset" select="addressOffset"/>
                                <xsl:with-param name="count" select="dimIncrement"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:call-template name="define_register">
                                <xsl:with-param name="peripheral_name" select = "$peripheral_name" />
                                <xsl:with-param name="register_name" select="$register_name"/>
                                <xsl:with-param name="register_size" select="$default_register_size"/>
                                <xsl:with-param name="base_address" select="$peripheral_base"/>
                                <xsl:with-param name="address_offset" select="addressOffset"/>
                                <xsl:with-param name="count" select="dimIncrement"/>
                            </xsl:call-template>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:for-each>
#endif /* #ifndef <xsl:value-of select="concat(translate(device/name, $lowercase, $uppercase), '_H')"/> */
    </xsl:template>
    <xsl:template name="string_replace">
        <xsl:param name="text" />
        <xsl:param name="replace" />
        <xsl:param name="by" />
        <xsl:choose>
            <xsl:when test="contains($text, $replace)">
                <xsl:value-of select="substring-before($text,$replace)" />
                <xsl:value-of select="$by" />
                <xsl:call-template name="string_replace">
                    <xsl:with-param name="text" select="substring-after($text,$replace)" />
                    <xsl:with-param name="replace" select="$replace" />
                    <xsl:with-param name="by" select="$by" />
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$text" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="define_register">
        <xsl:param name="peripheral_name"/>
        <xsl:param name="register_name"/>
        <xsl:param name="register_size"/>
        <xsl:param name="base_address"/>
        <xsl:param name="address_offset"/>
        <xsl:param name="count"/>
        <xsl:choose>
            <xsl:when test="$count">
                <xsl:variable name="_tmp_0">
                    <xsl:call-template name="string_replace">
                        <xsl:with-param name="text" select="$register_name"/>
                        <xsl:with-param name="replace" select="'%S'" />
                        <xsl:with-param name="by" select="''"/>
                    </xsl:call-template>
                </xsl:variable>
#define <xsl:value-of select="concat($peripheral_name, '_', $_tmp_0, ' ((volatile {prefix}', $register_size, '{suffix} *)(', $base_address, ' + ', $address_offset, 'u))')"/>
                <xsl:for-each select="(//node())[$count >= position()]">
                    <xsl:variable name="_register_name">
                        <xsl:call-template name="string_replace">
                            <xsl:with-param name="text" select="$register_name"/>
                            <xsl:with-param name="replace" select="'%S'" />
                            <xsl:with-param name="by" select="concat('_', position() - 1)"/>
                        </xsl:call-template>
                    </xsl:variable>
#define <xsl:value-of select="concat($peripheral_name, '_', $_register_name, ' (*(volatile {prefix}', $register_size, '{suffix} *)(', $base_address, ' + ', $address_offset, ' + (', (position() - 1) * $register_size, 'u)))')"/>
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
#define <xsl:value-of select="concat($peripheral_name, '_', $register_name, ' (*(volatile {prefix}', $register_size, '{suffix} *)(', $base_address, ' + ', $address_offset, 'u))')"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:transform>"""


def get_string(svd,
               type_header=None,
               is_system=False,
               type_prefix=DEFAULT_TYPE_PREFIX,
               type_suffix=DEFAULT_TYPE_SUFFIX):
    dom = et.XML(svd.encode('utf-8'))
    include = ''
    if type_header:
        include = '#include <xsl:value-of select="concat(\'{}\', \'{}\', \'{}\')"/>'.format(
            '&lt;' if is_system else '&quot;',
            type_header,
            '&gt;' if is_system else '&quot;')
    xslt = et.XSLT(et.fromstring(xslt_template.format(header=include, prefix=type_prefix, suffix=type_suffix)))
    return str(xslt(dom))


def main():
    parser = argparse.ArgumentParser(description='SVD to C header converter')
    parser.add_argument('--svd', metavar='FILE', type=str, help='System view description (SVD) file', required=True)
    parser.add_argument('--output', '-o', metavar='FILE', type=str, help='C header output file', required=True)
    parser.add_argument('--type_header',
                        metavar='FILE',
                        type=str,
                        default=None,
                        help='C header file containing standard type definitions (e.g. stdint.h)')
    parser.add_argument('-is_system',
                        action='store_true',
                        help='if provided, the "type_header" will be included as system header (e.g. #include <...>)')
    parser.add_argument('--type_prefix',
                        metavar='PREFIX',
                        type=str,
                        default=DEFAULT_TYPE_PREFIX,
                        help='prefix in register type name (e.g. "uint" in "uint32_t")')
    parser.add_argument('--type_suffix',
                        metavar='SUFFIX',
                        type=str,
                        default=DEFAULT_TYPE_SUFFIX,
                        help='prefix in register type name (e.g. "_t" in "uint32_t")')
    parser.add_argument('--version', action='version', version=pysvd.__version__)
    args = parser.parse_args()
    with open(args.output, 'w') as out:
        with open(args.svd, 'rb') as svd:
            out.write(get_string(svd.read(), args.type_header, args.is_system, args.type_prefix, args.type_suffix))


if __name__ == '__main__':
    main()
