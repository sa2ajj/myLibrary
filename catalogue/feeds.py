
"""A set of classes for generating feeds"""

from datetime import datetime

from xml.etree import ElementTree as ET

from utils import LocalTimezone

ATOM_NS = 'http://www.w3.org/2005/Atom'
DC_NS = 'http://purl.org/dc/elements/1.1/'

FEED_MIME_TYPE = 'application/atom+xml'

def add_child(parent, name, text_=None, **attrib):
    """adds a child element with the specified parameters"""

    child = ET.SubElement(parent, name, attrib=attrib)
    if text_ is not None:
        child.text = text_

    return child

def make_link(href, type_, rel, **other):
    """creates a link element"""

    attrib = {
        'href': href,
        'type': type_,
        'rel': rel,
    }
    attrib.update(other)

    return ET.Element('link', attrib=attrib)

class FeedItem(object):
    """Feed item"""

    def __init__(self):
        self._element = ET.Element('entry')

        self._element.append(self.uid)
        self._element.append(self.title)

    @property
    def element(self):
        """returns the ElementTree instance"""

        return self._element

    @property
    def uid(self):
        """returns ET.Element with the item's id"""

        return ET.Element('id', self.get_uid())

    def get_uid(self):
        """get the item's unique id"""

        raise NotImplementedError, '%s has no implementation for get_uid' % self.__class__.__name__

    @property
    def title(self):
        """returns ET.Element with the item's title"""

        return ET.Element('id', self.get_title())

    def get_title(self):
        """get the item's title"""

        raise NotImplementedError, '%s has no implementation for get_title' % self.__class__.__name__

class Feed(object):
    """represents an atom feed"""

    def __init__(self, link, title, updated=None):
        self._feed = ET.Element('feed', attrib={
            'xmlns': ATOM_NS,
            'xmlns:dc': DC_NS,
        })

        add_child(self._feed, 'title', text_=title)

        if updated is None:
            updated = datetime.now(LocalTimezone())

        add_child(self._feed, 'updated', text_=updated.isoformat())
        self._feed.append(make_link(link, type_=FEED_MIME_TYPE, rel='self'))

    @property
    def element(self):
        """ElementTree of the feed"""

        return self._feed

    def add(self, item):
        """add an item to the feed"""
        assert isinstance(item, FeedItem)

        self._feed.append(item.element)

    @property
    def mimetype(self):
        """feed's mimetype"""
        return FEED_MIME_TYPE

    def __unicode__(self):
        return ET.tostring(self._feed, 'utf-8')

class FeedItemFeed(FeedItem):
    """a feed item that is in turn another feed"""

    def __init__(self, name, link):
        super(FeedItem, self).__init__()

        self._name = name
        self._link = link

    def get_uid(self):
        """returns item's unique id"""
        return self._link

    def get_title(self):
        """returns item's title"""
        return self._name

class FeedItemBook(FeedItem):
    """a feed item for a book"""

    def __init__(self, book):
        super(FeedItem, self).__init__()

        self._book = book

    def get_uid(self):
        """returns book's unique id"""

    def get_title(self):
        """returns book's title"""

        return self._book.title
