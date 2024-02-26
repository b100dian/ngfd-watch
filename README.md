Non-graphical feedback daemon watchdog
-----

The NGFD uses gstreamer to play back notifications and it so happens that sometimes that deadlocks.
This watchdog works on the assumption that an audio (ogg) file is open by NGFD process when it is deadlocked.
When a such file is opened for 60 seconds (polling each 10 seconds) then the process is killed.
A notification is sent to Sailfish homescreen too.

60 seconds is also an alarm or unanswered ringtone.
