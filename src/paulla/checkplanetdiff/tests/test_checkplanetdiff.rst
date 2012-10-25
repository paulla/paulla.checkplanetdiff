'Nagios like' synchronise delay OSM Planet check
=================================================


neccessary stuff

    >>> import glob
    >>> import subprocess
    >>> from datetime import datetime
    >>> from pprint import pprint

    >>> def print_lines_from_file(filename):
    ...     with open(filename) as state_file:
    ...         return state_file.read().splitlines()
    ...

We have to fake now according to tests files states.

Real check is datetime.datetime.utcnow()

    >>> now = datetime(2012, 10, 23, 20, 4, 30)


Less than 1 hour returns OK
--------------------------------

    >>> state_file_ok = "src/paulla/checkplanetdiff/tests/state_ok.txt"
    >>> pprint(print_lines_from_file(state_file_ok))
    ['#Tue Oct 23 22:05:12 CEST 2012',
     'sequenceNumber=59592',
     'timestamp=2012-10-23T20\\:04\\:02Z']

    >>> cmd_ok = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s" % state_file_ok
    >>> p_ok = subprocess.Popen(cmd_ok.split(), stdout=subprocess.PIPE)

Status code is 0 -> OK

    >>> p_ok.wait()
    0

String output

    >>> p_ok.stdout.read()
    'OK: delay : 28, sequence number : 59592\n'


Delay between 1 hour and 6 returns WARNING
-------------------------------------------

    >>> state_file_warn = "src/paulla/checkplanetdiff/tests/state_warning.txt"
    >>> pprint(print_lines_from_file(state_file_warn))
    ['#Tue Oct 23 18:25:07 CEST 2012',
     'sequenceNumber=59372',
     'timestamp=2012-10-23T16\\:24\\:03Z']

    >>> cmd_warn = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s" % state_file_warn
    >>> p_warn = subprocess.Popen(cmd_warn.split(), stdout=subprocess.PIPE)

Status code is 1 -> WARNING

    >>> p_warn.wait()
    1

String output

    >>> p_warn.stdout.read()
    'WARN: delay : 13227, sequence number : 59372\n'


More than 6 hours returns CRITICAL
----------------------------------

    >>> state_file_crit = "src/paulla/checkplanetdiff/tests/state_critical.txt"
    >>> pprint(print_lines_from_file(state_file_crit))
    ['#Tue Oct 23 12:25:07 CEST 2012',
     'sequenceNumber=59012',
     'timestamp=2012-10-23T10\\:24\\:03Z']

    >>> cmd_crit = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s" % state_file_crit
    >>> p_crit = subprocess.Popen(cmd_crit.split(), stdout=subprocess.PIPE)

Status code is 2 -> CRITICAL

    >>> p_crit.wait()
    2

String output

    >>> p_crit.stdout.read()
    'CRIT: delay : 34827, sequence number : 59012\n'


Non existant state file returns UNKNOWN
---------------------------------------

    >>> cmd_crit_non_exist_file = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file src/paulla/checkplanetdiff/tests/state_non_existant.txt"
    >>> p_crit_nonexist = subprocess.Popen(cmd_crit_non_exist_file.split(), stdout=subprocess.PIPE)

Status code is 3 -> UNKNOWN

    >>> p_crit_nonexist.wait()
    3

String output

    >>> p_crit_nonexist.stdout.read()
    'UNKNOWN: src/paulla/checkplanetdiff/tests/state_non_existant.txt filestate not found\n'
