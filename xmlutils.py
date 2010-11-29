
"""A set of xml related helpers"""

import logging
LOG = logging.getLogger(__name__)

import sys

from xml.etree import ElementTree as ET
from xml.dom import minidom

def parse_xml(data, info=False, label=None):
    ''' parses provided XML string using ElementTree '''

    try:
        result = ET.fromstring(data)
    except:
        # TODO: try to find a way to catch the right exception only
        if info:
            LOG.exception('Exception (label=%s):', label)
            LOG.error('parse_xml: %s: %s', type(data), data)

        result = None

    return result

def dump(elem, indent=0, stream=sys.stdout):
    ''' pretty dumps an ElementTree '''

    if elem is None:
        print >> stream, 'OOPS: no elem to dump'
        return

    if elem.text:
        text = ' text: %s' % repr(elem.text)
    else:
        text = ''

    if elem.tail:
        tail = ' tail: %s' % repr(elem.tail)
    else:
        tail = ''

    print >> stream, '%sdump: %s %s%s%s' % (' '*indent, elem.tag, elem.attrib, text, tail)

    for child in elem:
        dump(child, indent+2, stream)

def tostring(elem):
    """pretty printer of a xml representation of the given element"""

    return minidom.parseString(ET.tostring(elem, 'utf-8')).toprettyxml(indent='  ')

# vim:ts=4:sw=4:et
