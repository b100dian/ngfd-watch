#!/bin/bash

#
# This script watches the file handles of ngfd by means of lsof.
# Whenever the same handle and filename that contains .ogg appear
# between two consecutive time INTERVALs, it kills ngfd.
# It also sens a notification that it did that, so you can see if it happened.
#
# The idea is that an audio file opened for a large amount of time
# is equivalent to ngfd encountering a GStreamer deadlock while playing it.
#

LSOF_NGFD="lsof -p $( pgrep -x ngfd )"
INTERVAL=60s

LAST_OGG=
LAST_OGG_FD=

while :
do
  sleep $INTERVAL
  OGG_LINE=$( $LSOF_NGFD | grep \\.ogg | head -n 1 )
  if [ -z "$OGG_LINE" ]; then continue; fi
  OGG=$( echo "$OGG_LINE" | awk '{print $9}' )
  OGG_FD=$( echo $OGG_LINE | awk '{print $4}' )
  if [ $OGG = "$LAST_OGG" ] && [ $OGG_FD = "$LAST_OGG_FD" ];
  then
    echo COMA COMA COMA COMA COMA CHAMELEON $( date -Iseconds )  $( pidof ngfd ) $OGG_FD $OGG
    kill -9 $( pgrep -x ngfd ) && notificationtool -o add "Restarted ngfd coma" "I had to restart ngfd on $(date -Iseconds), reason $OGG"
  else
    echo Matched $( date -Iseconds ) $OGG_FD $OGG
  fi
  LAST_OGG=$OGG
  LAST_OGG_FD=$OGG_FD
done

