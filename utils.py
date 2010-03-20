"""A set of useful utilities"""

from datetime import timedelta, tzinfo
import time as _time

ZERO = timedelta(0)

STDOFFSET = timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

def _isdst(dst_):
    """ ... """

    stamp = _time.mktime((dst_.year, dst_.month, dst_.day,
            dst_.hour, dst_.minute, dst_.second,
            dst_.weekday(), 0, -1))
    return _time.localtime(stamp).tm_isdst > 0

class LocalTimezone(tzinfo):
    """Handler for local timezones"""

    def utcoffset(self, dst):
        """return difference between the timezone and UTC"""

        if self._isdst(dst):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dst_):
        """ ... """

        if self._isdst(dst_):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dst):
        """ ... """

        return _time.tzname[self._isdst(dst)]

# vim:ts=4:sw=4:et
