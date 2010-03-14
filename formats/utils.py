
import sys
from traceback import print_exc

from xml.etree import ElementTree as ET

def parse_xml(data):
    try:
        result = ET.fromstring(data)
    except:
        # TODO: try to find a way to catch the right exception only
        print_exc()
        print >> sys.stderr, 'parse_xml: %s: %s' % (type(data), data)

        result = None

    return result
