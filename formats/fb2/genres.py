
import os, sys

from formats.utils import parse_xml, dump

_genres = None

class FB2Genres:
    def __init__(self):
        self._genres = {}
        self._aliases = {}

    def get(self, genre):
        if genre in self._genres:
            return self._genres[genre]
        elif genre in self._aliases:
            return self.get(self._aliases[genre])
        else:
            raise KeyError, genre

    def add_genre(self, genre, parent, title):
        self._genres[genre] = (parent, title)

    def add_alias(self, genre, alias):
        self._aliases[alias] = genre

    def validate(self):
        for genre, (parent, _) in self._genres.iteritems():
            if parent is not None:
                try:
                    self.get(parent)
                except KeyError:
                    raise KeyError('parent %s for %s is not defined' % (parent, genre))

        for alias, genre in self._aliases.iteritems():
            try:
                self.get(genre)
            except KeyError:
                raise KeyError('alias %s for %s is not defined' % (genre, alias))

def _ensure_genres(lang='en'):
    global _genres

    if _genres is None:
        genres_file = os.path.join(os.path.dirname(__file__), 'fb2genres.xml')

        result = FB2Genres()

        genres = parse_xml(open(genres_file, 'r').read())

        # dump(genres)

        for genre in genres:
            fb2_genre = genre.attrib['value']

            name = None

            for child in genre:
                if child.tag == 'root-descr':
                    if child.attrib['lang'] == 'en':
                        name = child.attrib['genre-title']
                elif child.tag == 'subgenres':
                    for subgenre in child:
                        fb2_subgenre = subgenre.attrib['value']
                        sub_name = None

                        for subelem in subgenre:
                            if subelem.tag == 'genre-descr':
                                if subelem.attrib['lang'] == 'en':
                                    sub_name = subelem.attrib['title']
                            elif subelem.tag == 'genre-alt':
                                result.add_alias(fb2_subgenre, subelem.attrib['value'])

                        if sub_name is None:
                            print >> sys.stderr, 'could not find name for %s' % fb2_subgenre
                        else:
                            result.add_genre(fb2_subgenre, fb2_genre, sub_name)

            if name is None:
                print >> sys.stderr, 'could not find name for %s' % fb2_genre
            else:
                result.add_genre(fb2_genre, None, name)

        result.validate()

        _genres = result

def normalize_tag(tag):
    _ensure_genres()

    if _genres is None:
        return tag

    try:
        result = []

        while tag is not None:
            tag, title = _genres.get(tag)

            result.insert(0, title)

        return '/'.join(result)
    except KeyError:
        return tag

# vim:ts=4:sw=4:et
