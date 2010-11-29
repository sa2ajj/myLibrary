
"""A set of classes for generating feeds"""

from datetime import datetime

from xml.etree import ElementTree as ET

from xmlutils import tostring
from utils import LocalTimezone

ATOM_NS = 'http://www.w3.org/2005/Atom'
DC_NS = 'http://purl.org/dc/elements/1.1/'

FEED_MIME_TYPE = 'application/atom+xml'

class FeedItemNotImplementedError(NotImplementedError):
    """helper for not implemented items in FeedItem"""

    def __init__(self, method, class_name):
        """a really simple constructor"""

        NotImplementedError.__init__(self, 'method "%s" not implemented in '
                                           'class "%s"' % (method, class_name))
class FeedItem(object):
    """base class for various feed related items"""

    def __init__(self, name='entry', text_=None, attrib_=None, **other):
        if attrib_ is None:
            attrib = other
        else:
            attrib = attrib_
            attrib.update(other)

        self._element = ET.Element(name, attrib=attrib)
        if text_ is not None:
            self._element.text = text_

        self._good = False

    def xml(self):
        """returns xml representation"""

        self._ensure_content()

        return tostring(self._element)

    @property
    def element(self):
        """returns the ElementTree instance"""

        self._ensure_content()

        return self._element

    def _ensure_content(self):
        """ensures content of the element"""

        if not self._good:
            self.add_child('id', self.uid)
            self.add_child('title', self.title)

            self.add_other_elems()

            self._good = True

    def add_element(self, element):
        """adds the specified element as a child"""

        assert ET.iselement(element)

        self._element.append(element)

    def add_child(self, name, text_=None, attrib_=None, **other):
        """adds a child element with the specified parameters"""

        if attrib_ is None:
            attrib = other
        else:
            attrib = attrib_
            attrib.update(other)

        child = ET.SubElement(self._element, name, attrib=attrib)
        if text_ is not None:
            child.text = text_

        return child

    def add_link(self, href, type_, rel=None, **other):
        """adds a link element"""

        attrib = {
            'href': href,
            'type': type_,
        }
        if rel is not None:
            attrib['rel'] = rel

        attrib.update(other)

        return self.add_child('link', attrib_=attrib)

    @property
    def uid(self):
        """item's unique id"""

        return self.get_uid()

    def get_uid(self):
        """get the item's unique id"""

        raise FeedItemNotImplementedError('get_uid', self.__class__.__name__)

    @property
    def title(self):
        """item's title"""

        return self.get_title()

    def get_title(self):
        """get the item's title"""

        raise FeedItemNotImplementedError('get_title', self.__class__.__name__)

    def add_other_elems(self):
        """add all other properties for the entry"""

        raise FeedItemNotImplementedError('add_other_elems',
                                          self.__class__.__name__)

class Feed(FeedItem):
    """represents an atom feed"""

    def __init__(self, link, title, updated=None):
        super(Feed, self).__init__('feed', attrib_={
            'xmlns': ATOM_NS,
            'xmlns:dc': DC_NS,
        })

        self._link = link
        self._title = title

        if updated is None:
            updated = datetime.now(LocalTimezone())

        self._updated = updated

    def add_other_elems(self):
        """adds items for the feed"""

        self.add_child('updated', self._updated.isoformat())
        self.add_link(self._link, type_=FEED_MIME_TYPE, rel='self')

    def get_uid(self):
        """returns feed's uid"""

        return self._link

    def get_title(self):
        """returns feed's title"""

        return self._title

    def add(self, item):
        """add an item to the feed"""
        assert isinstance(item, FeedItem)

        self.add_element(item.element)

    @staticmethod
    def mimetype():
        """feed's mimetype"""
        return FEED_MIME_TYPE

class FeedItemFeed(FeedItem):
    """a feed item that is in turn another feed"""

    def __init__(self, name, link):
        super(FeedItemFeed, self).__init__()

        self._name = name
        self._link = link

    def get_uid(self):
        """returns item's unique id"""
        return self._link

    def get_title(self):
        """returns item's title"""
        return self._name

    def add_other_elems(self):
        """add other items for the feed entry"""

        self.add_link(self.uid, type_=FEED_MIME_TYPE)

class FeedItemBook(FeedItem):
    """a feed item for a book"""

    def __init__(self, book):
        super(FeedItemBook, self).__init__()

        self._book = book

    def get_uid(self):
        """returns book's unique id"""

        return self._book.id

    def get_title(self):
        """returns book's title"""

        return self._book.title

    def add_other_elems(self):
        """add other items for the book entry"""

# vim:ts=4:sw=4:et
