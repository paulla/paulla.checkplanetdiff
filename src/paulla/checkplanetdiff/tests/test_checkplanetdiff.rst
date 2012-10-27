Nagios like' synchronise delay OSM Planet check
=================================================


Use case


The check is simple and robust, no database query.

Delay is just datetime.datetime.utcnow() - OSM timestamp in state.txt (usaualy /home/mapnik.osmosis/state.txt)

More infos here http://wiki.openstreetmap.org/wiki/Minutely_Mapnik

We fake 3 state files with three different timestamp (see tests/ directory). 

We have to fake now according to tests files states.

now = datetime(2012, 10, 23, 20, 4, 30) # see test function

Real check is datetime.datetime.utcnow()

Warning and critical thresholds are respectively 3600 and 21600 seconds (1 and 6 hours)

Time to work

necessary stuff::
    
    >>> import glob
    >>> import subprocess
    >>> from datetime import datetime
    >>> from pprint import pprint

a funtion to get lines from fake state files::
    
    >>> def get_lines_from_file(filename):
    ...     with open(filename) as state_file:
    ...         return state_file.read().splitlines()
    ...
    

Usage
------

-h option ::
    
    >>> cmd_h = "bin/test_check_planetdiff -h"
    >>> p_help = subprocess.Popen(cmd_h.split(), stdout=subprocess.PIPE)
    >>> pprint(p_help.stdout.readlines())
    ['Usage: test_check_planetdiff [options]\n',
     '\n',
     'Options:\n',
     '  --state-file=STATEFILE\n',
     '  -p                    return performance data\n',
     '  -v, --verbose         \n',
     '  -H HOSTNAME, --hostname=HOSTNAME\n',
     '  -w WARNING, --warning=WARNING\n',
     '  -c CRITICAL, --critical=CRITICAL\n',
     '  -t TIMEOUT, --timeout=TIMEOUT\n',
     '  -h, --help            show this help message and exit\n']


Checks
--------

Less than 1 hour returns OK::
    
    >>> state_file_ok = "src/paulla/checkplanetdiff/tests/state_ok.txt"
    >>> pprint(get_lines_from_file(state_file_ok))
    ['#Tue Oct 23 22:05:12 CEST 2012',
     'sequenceNumber=59592',
     'timestamp=2012-10-23T20\\:04\\:02Z']

    >>> cmd_ok = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s" % state_file_ok
    >>> p_ok = subprocess.Popen(cmd_ok.split(), stdout=subprocess.PIPE)

Status code is 0 -> OK::
    
    >>> p_ok.wait()
    0

String output::
    
    >>> p_ok.stdout.read()
    'OK: delay : 28, sequence number : 59592\n'

with perfdata option::
    
    >>> cmd_ok = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s -p" % state_file_ok 
    >>> p_ok = subprocess.Popen(cmd_ok.split(), stdout=subprocess.PIPE)
    >>> p_ok.stdout.read()
    'OK: delay : 28, sequence number : 59592|delayed=28s;3600;21600;;\n'

Delay between 1 hour and 6 returns WARNING::
    
    >>> state_file_warn = "src/paulla/checkplanetdiff/tests/state_warning.txt"
    >>> pprint(get_lines_from_file(state_file_warn))
    ['#Tue Oct 23 18:25:07 CEST 2012',
     'sequenceNumber=59372',
     'timestamp=2012-10-23T16\\:24\\:03Z']

    >>> cmd_warn = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s" % state_file_warn
    >>> p_warn = subprocess.Popen(cmd_warn.split(), stdout=subprocess.PIPE)

Status code is 1 -> WARNING::
    
    >>> p_warn.wait()
    1

String output::
    
    >>> p_warn.stdout.read()
    'WARN: delay : 13227, sequence number : 59372\n'

with perfdata option::
    
    >>> cmd_warn = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s -p" % state_file_warn
    >>> p_warn = subprocess.Popen(cmd_warn.split(), stdout=subprocess.PIPE)
    >>> p_warn.stdout.read()
    'WARN: delay : 13227, sequence number : 59372|delayed=13227s;3600;21600;;\n'

More than 6 hours returns CRITICAL::
    
    >>> state_file_crit = "src/paulla/checkplanetdiff/tests/state_critical.txt"
    >>> pprint(get_lines_from_file(state_file_crit))
    ['#Tue Oct 23 12:25:07 CEST 2012',
     'sequenceNumber=59012',
     'timestamp=2012-10-23T10\\:24\\:03Z']
    
    >>> cmd_crit = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s" % state_file_crit
    >>> p_crit = subprocess.Popen(cmd_crit.split(), stdout=subprocess.PIPE)

Status code is 2 -> CRITICAL::
    
    >>> p_crit.wait()
    2

String output::
    
    >>> p_crit.stdout.read()
    'CRIT: delay : 34827, sequence number : 59012\n'

with perfdata option::
    
    >>> cmd_crit = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file %s -p" % state_file_crit
    >>> p_crit = subprocess.Popen(cmd_crit.split(), stdout=subprocess.PIPE)
    >>> p_crit.stdout.read()
    'CRIT: delay : 34827, sequence number : 59012|delayed=34827s;3600;21600;;\n'

Non existant state file returns CRITICAL::
    
    >>> cmd_crit_non_exist_file = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file src/non_existant.txt"
    >>> p_crit_nonexist = subprocess.Popen(cmd_crit_non_exist_file.split(), stdout=subprocess.PIPE)

Status code is 2 -> CRITICAL::
    
    >>> p_crit_nonexist.wait()
    2

String output::
    
    >>> p_crit_nonexist.stdout.read()
    'CRIT: delay : 21601, sequence number : 0\n'

with perfdata option::
    
    >>> cmd_crit_non_exist_file = "bin/test_check_planetdiff -w 0.0:3600.0 -c 0.0:21600.0 --state-file src/non_existant.txt -p"
    >>> p_crit_nonexist = subprocess.Popen(cmd_crit_non_exist_file.split(), stdout=subprocess.PIPE)
    >>> p_crit_nonexist.stdout.read()
    'CRIT: delay : 21601, sequence number : 0|delayed=21601s;3600;21600;;\n'

