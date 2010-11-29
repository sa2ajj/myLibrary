import logging
LOG = logging.getLogger(__name__)

import sys

from formats.utils import parse_xml, get_good_zip, dump

CONTAINER = 'META-INF/container.xml'

CONTAINER_NS = 'urn:oasis:names:tc:opendocument:xmlns:container'

IDPF_NS = 'http://www.idpf.org/2007/opf'

def read_oeb_metadata(metadata):
    print 'OEB:'
    dump(metadata)

def read_opf_metadata(metadata):
    print 'OPF:'
    dump(metadata)

    title = None
    language = None
    authors = []
    series = []
    tags = []
    annotation = None

    for child in metadata:
        index = child.tag.find('}')
        if index == -1:     # skipped unqualified names
            continue

        name = child.tag[index+1:]

        if name == 'title':
            title = child.text.strip()
        elif name == 'language':
            language = child.text.strip()
        elif name == 'subject':
            tags.append(child.text.strip())
        elif name == 'description':
            if child.text:
                annotation = child.text.strip()
            else:
                annotation = ''
        elif name == 'creator':
            role = child.get('{%s}role', 'aut')

            if role == 'aut':
                authors.append(child.text.strip())

    result = {
        'title': title,
        'language': language,
        'authors': authors,
        'series': series,
        'tags': list(set(tags)),
        'annotation': annotation,
    }

    LOG.debug('read_opf_metadata output: %s', result)

    return result

def read(path):
    LOG.debug("reading %s", path)

    archive = get_good_zip(path)

    try:
        container = archive.read(CONTAINER)
    except KeyError:
        LOG.error('%s has no container', path)
        return

    container = parse_xml(container)

    if container is None:
        LOG.error('%s has invalid container', path)
        return

    opf_name = container.find('.//{%s}rootfile' % CONTAINER_NS).get('full-path')

    try:
        opf = archive.read(opf_name)
    except KeyError:
        LOG.error('Could not open opf file (%s)', opf_name.encode('utf-8'))
        return

    opf = parse_xml(opf)

    if 0:
        dump(opf)

    metadata = None

    for child in opf:
        if child.tag == 'metadata' or child.tag.endswith('}metadata'):
            metadata = child
            break

    if metadata is None:
        LOG.error('Could not find metadata in the opf file')
        return

    if metadata.tag == 'metadata':
        return read_oeb_metadata(metadata)
    else:
        return read_opf_metadata(metadata)

# vim:ts=4:sw=4:et
