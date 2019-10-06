#!/bin/bash

### BEGIN INIT INFO
# Provides:          chandeleur
# Required-Start:    $local_fs $network $syslog
# Required-Stop:     $local_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: chandeleur
# Description:       chandeleur management script
### END INIT INFO

# This script should be located in /etc/init.d/chandeleur
#   (do not make a link because it won't work at system boot)
#   cp /home/chandeleur/chandeleur/scripts/init.d.sh /etc/init.d/chandeleur
# To make this script start at boot:
#   systemctl enable chandeleur
# To remove it use:
#   systemctl disable chandeleur

if [[ $# < 1 ]]; then
    echo "Not enough arguments."
    exit 1
fi

/bin/su chandeleur -c "python3 /home/chandeleur/chandeleur/scripts/control.py $1"
exit $?
