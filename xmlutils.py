
import sys

from cStringIO import StringIO

from xml.etree import ElementTree as ET

from traceback import print_exc

def parse_xml(data, info=False, label=None):
    ''' parses provided XML string using ElementTree '''

    try:
        result = ET.fromstring(data)
    except:
        # TODO: try to find a way to catch the right exception only
        if info:
            print_exc()
            if label:
                print >> sys.stderr, 'Label:', label
            print >> sys.stderr, 'parse_xml: %s: %s' % (type(data), data)

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
    output = StringIO()

    print >> output, '<?xml version="1.0" encoding="utf-8"?>'

    default_namespaces = {
        'http://www.w3.org/XML/1998/namespace': 'xml',
    }

    _tostring(output, elem, 0, namespaces=default_namespaces)

    return output.getvalue()

def _fix_ns(item, namespaces, attrib=False):
    if '}' in item:
        parts = item[1:].split('}', 1)

        xmlns = namespaces.get(parts[0], None)

        if xmlns is None:
            xmlns = 'ns%d' % len(namespaces)

            namespaces[parts[0]] = xmlns

        if xmlns:
            pp_item = '%s:%s' % (xmlns, parts[1])
        else:
            pp_item = parts[1]
    else:
        pp_item = item

    return pp_item

def _tostring(output, elem, indent, do_indent=True, namespaces={}):
    # TODO: add check that we are processing a ElementTree.Element

    if 0:
        print >> output, '_tostring:', elem.tag, indent, do_indent

    local_namespaces = {}

    for name, value in elem.items():
        if name == 'xmlns' or name.startswith('xmlns:'):
            parts = name.split(':')
            if len(parts) == 1:
                xmlns = ''
            else:
                xmlns = parts[1]

            local_namespaces[value] = xmlns

    inherited_namespaces = namespaces.copy()
    inherited_namespaces.update(local_namespaces)

    local_attrib = {}

    if '}' in elem.tag:
        parts = elem.tag[1:].split('}', 1)

        xmlns = inherited_namespaces.get(parts[0], None)

        if xmlns is None:
            xmlns = 'ns%d' % len(inherited_namespaces)

            inherited_namespaces[parts[0]] = xmlns
            local_attrib[xmlns] = parts[0]

        if xmlns:
            pp_tag = '%s:%s' % (xmlns, parts[1])
        else:
            pp_tag = parts[1]
    elif ':' in elem.tag:
        parts = elem.tag.split(':', 1)

        if parts[0] not in inherited_namespaces.values():
            raise ValueError, '%s namespace is used while it\'s not defined' % parts[0]

        pp_tag = elem.tag
    else:
        pp_tag = elem.tag

    if 0:
        print >> output, 'ELEM:', indent, pp_tag

    if do_indent:
        output.write(' '*indent)

    output.write('<%s' % pp_tag)

    for attrib in [ elem.items(), local_attrib.items() ]:
        if attrib:
            output.write(' ')

            output.write(' '.join([ '%s="%s"' % (_fix_ns(item[0], inherited_namespaces, True), item[1]) for item in attrib ]))

    children = elem.getchildren()

    if elem.text or children:
        output.write('>')

        if elem.text:
            output.write(elem.text.encode('utf-8'))
            do_child_indent = False
        else:
            output.write('\n')
            do_child_indent = True

        for child in children:
            if 0:
                print >> output, 'CHILD_INDENT:', child.tag, do_child_indent

            do_child_indent = _tostring(output, child, indent+2, do_child_indent, inherited_namespaces)

        if 0:
            print >> output, 'CHILD_INDENT:', do_child_indent

        if not elem.text and do_indent:
            output.write(' '*indent)

        output.write('</%s>' % pp_tag)
    else:
        output.write('/>')

    if elem.tail is not None and elem.tail.strip():
        output.write(elem.tail.encode('utf-8'))
        return False
    else:
        output.write('\n')
        return True

# vim:ts=4:sw=4:et
