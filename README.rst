.. contents::

Introduction
============


check_planet.diff is a 'Nagios like' (Nagios|Icinga|Centreon|Shinken) probe checking the delay of your OSM Planet with offical, based on minute-diff state files.

More infos here http://wiki.openstreetmap.org/wiki/Minutely_Mapnik


Install
-------

easy_install | pip witthin or not a virtualenv ::

    tool paulla.check_planetdiff

zc.buildout users ::

    just add paulla.check_planetdiff to your eggs list as usual.

You could simply run tests with::
 
 bin/python setup.py test

Mayba add a symbolic link from bin/check_planetdiff to your nagios/plugins/ directory.



Nagios like configuration
---------------------------

check_planetdiff could be called localy or remotely via check_by_ssh or NRPE.

here a sample definition to check remotely by ssh ::

Command definition ::
 
 # 'check_ssh_planetdiff' command definition
 define command {
        command_name    check_ssh_planetdiff
        command_line    $USER1$/check_by_ssh -H $HOSTADDRESS$ -C "/usr/lib/nagios/plugins/check_planetdiff -w $ARG1$ -c $ARG2$ --state-file $ARG3$ -p" 
 }

Notice the last -p arg for performance data is optionnal, remove it if don't needed.

the service itself::
 
 # planet diff delay
 define service {
        use                             paulla-service
        service_description             delay planet diff
        check_command                   check_ssh_planetdiff!0.0:3600.0!0.0:21600.0!/home/mapnik/.osmosis/state.txt
        host_name                       biscaou
 }
