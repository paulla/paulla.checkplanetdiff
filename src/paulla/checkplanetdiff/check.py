# -*- coding: utf-8 -*-

"""See tests/test_checkplanetdiff.rst
"""

__docformat__ = 'restructuredtext en'

import os

from datetime import datetime
from pynagios import Plugin, make_option, Response, UNKNOWN


class CheckPlanetDiff(Plugin):
    """Plugin Check delay."""

    statefile = make_option("--state-file", dest="state-file")

    def state_file_exists(self, statefile_path):
        """Catch bad statefile path."""

        if not os.path.isfile(statefile_path):
            msg = '%s filestate not found' % statefile_path
            return Response(UNKNOWN, msg).exit()

    def get_last_update(self, now):
        """Get sequence number and diff time from statefile."""

        self.state_file_exists(self.options.statefile)

        ts_format = '%Y-%m-%dT%H\\:%M\\:%SZ'
        with open(self.options.statefile) as f_state:
            lines = f_state.read().splitlines()

        seq_nber = lines[1].split('=')[-1]
        osm_update = lines[-1].split('=')[-1]
        last_diff = datetime.strptime(osm_update, ts_format)
        delay = now - last_diff
        return (delay.total_seconds(), seq_nber)

    def check(self, now):
        """Check delay value."""
        msg = 'delay : %d, sequence number : %s'
        delay, seq_nber = self.get_last_update(now)
        result = self.response_for_value(delay, msg % (int(delay), seq_nber))
        return result


def run():
    """Run check."""

    now = datetime.utcnow()
    CheckPlanetDiff().check(now=now).exit()


def test():
    """Similar to check, but we have to enforce now."""

    now = datetime(2012, 10, 23, 20, 4, 30)
    CheckPlanetDiff().check(now=now).exit()

# vim:set et sts=4 ts=4 tw=80: