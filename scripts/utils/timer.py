# -*- coding: utf-8 -*-
# @Author: juan
# @Date:   2018-08-08 13:48:05
# @Last Modified by:   Juan Quintana
# @Last Modified time: 2018-08-21 17:27:00
# by Mikel Bober-Irizar

import time
from warnings import warn


# Function wrapper that warns is deprecated, and call the function anyway (by Mikel Bober-Irizar)
def _deprecated(func, old_name, new_name):
    def new_func(*args, **kwargs):
        message = '{}() has been deprecated in favour of {}() and will be removed soon'.format(old_name, new_name)
        warn(message)
        return func(*args, **kwargs)
    return new_func


class Timer:
    """A class for tracking timestamps and time elapsed since events. Useful for profiling code.
    Usage:
    >>> t = Timer()
    >>> t.since() # Seconds since the timetracker was initialised
    >>> t.add('func') # Save the current timestamp as 'func'
    >>> t.since('func') # Seconds since 'func' was added
    >>> t['func'] # Get the absolute timestamp of 'func' for other uses
    """

    def __init__(self):
        self.times = {}
        self.add(0)

    def __getitem__(self, key):
        return self.times[key]

    def add(self, key):
        """Add the current time to the index with the specified key"""
        self.times[key] = time.time()

    def since(self, key=0):
        """Get the time elapsed in seconds since the specified key was added to the index"""
        return time.time() - self.times[key]

    def fsince(self, key=0, max_fields=3):
        """Get the time elapsed in seconds, nicely formatted by format_duration()"""
        return format_duration(self.since(key), max_fields)

    elapsed = _deprecated(since, 'Timer.elapsed', 'Timer.since')
    format_elapsed = _deprecated(fsince, 'Timer.format_elapsed', 'Timer.fsince')


def now():
    """Returns the current time as a string in the format 'YYYY_MM_DD_HH_MM_SS'. Useful for timestamping filenames etc."""
    return time.strftime("%Y_%m_%d_%H_%M_%S")


# Alias for backwards-compatibility
str_time_now = _deprecated(now, 'mlcrate.time.str_time_now', 'mlcrate.time.now')


def format_duration(seconds, max_fields=3):
    """Formats a number of seconds in a pretty readable format, in terms of seconds, minutes, hours and days.
    Example:
    >>> format_duration(3825.21)
    '1h03m45s'
    >>> format_duration(3825.21, max_fields=2)
    '1h03m'
    Keyword arguments:
    seconds -- A duration to be nicely formatted, in seconds
    max_fields (default: 3) -- The number of units to display (eg. if max_fields is 1 and the time is three days it will only display the days unit)
    Returns: A string representing the duration
    """
    seconds = float(seconds)
    s = int(seconds % 60)
    m = int((seconds / 60) % 60)
    h = int((seconds / 3600) % 24)
    d = int(seconds / 86400)

    fields = []
    for unit, value in zip(['d', 'h', 'm', 's'], [d, h, m, s]):
        if len(fields) > 0:  # If it's not the first value, pad with 0s
            fields.append('{}{}'.format(str(value).rjust(2, '0'), unit))
        elif value > 0:  # If there are no existing values, we don't add this unit unless it's >0
            fields.append('{}{}'.format(value, unit))

    fields = fields[:max_fields]

    # If the time was less than a second, we just return '<1s' TODO: Maybe return ms instead?
    if len(fields) == 0:
        fields.append('<1s')

    return ''.join(fields)



# main
if __name__ == '__main__':
    from datetime import datetime

    # initialize
    t = Timer()

    # save the current timestamp as 'func' into a TIME LOGGER
    print('add "event"')
    t.add('event')

    # sleep (simulate any function usage)
    print('sleep...')
    time.sleep(5)

    # seconds since 'func' was added
    tf = t.since('event')
    print('time from .. %s sec' % tf)
    # format1
    stf1 = format_duration(tf)
    print('time from (formated by function).. %s' % stf1)
    # format2
    stf2 = t.fsince('event')
    print('time from (formated by attribute).. %s' % stf2)

    # get the absolute timestamp of 'func' for other uses
    print('absolute timestamp: %s' % t['event'])
    print('absolute timestemp (into datetime): %s ' % datetime.fromtimestamp(t['event']).strftime('%Y-%m-%d %H:%M:%S'))

    # datetime now (formated for output file names)
    print('now is: %s' % now())
