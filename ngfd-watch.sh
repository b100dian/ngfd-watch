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
INTERVAL=10s
CONSECUTIVE_MATCHES=6

LAST_OGG=
LAST_OGG_FD=
MATCH_COUNT=0

while :
do
  sleep $INTERVAL
  OGG_LINE=$( lsof -p $( pgrep -x ngfd ) | grep \\.ogg | head -n 1 )
  if [ -z "$OGG_LINE" ];
  then
    LAST_OGG=
    LAST_OGG_FD=
    MATCH_COUNT=0
    continue
  fi
  OGG=$( echo "$OGG_LINE" | awk '{print $9}' )
  OGG_FD=$( echo $OGG_LINE | awk '{print $4}' )
  if [ $OGG = "$LAST_OGG" ] && [ $OGG_FD = "$LAST_OGG_FD" ] && [ $MATCH_COUNT -eq $CONSECUTIVE_MATCHES ];
  then
    echo COMA COMA COMA COMA COMA CHAMELEON $( date -Iseconds )  $( pidof ngfd ) $OGG_FD $OGG
    kill -9 $( pgrep -x ngfd ) && notificationtool -o add "Restarted ngfd, coma" "I had to restart ngfd on $(date -Iseconds), reason $OGG"
    LAST_OGG=
    LAST_OGG_FD=
    MATCH_COUNT=0
    continue
  else
    MATCH_COUNT=$(($MATCH_COUNT+1))
    echo Matched x $MATCH_COUNT $( date -Iseconds ) $OGG_FD $OGG
  fi
  LAST_OGG=$OGG
  LAST_OGG_FD=$OGG_FD
done

