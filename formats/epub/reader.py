from formats.utils import parse_xml, get_good_zip

CONTAINER = 'META-INF/container.xml'

def read(path):
    archive = get_good_zip(path)

    try:
        container = archive.read(CONTAINER)
    except KeyError:
        print >> sys.stderr, '%s has no container' % path
        return

    container = parse_xml(container)

    if container is None:
        print >> sys.stderr, '%s has invalid container' % path
        return

# vim:ts=4:sw=4:et
