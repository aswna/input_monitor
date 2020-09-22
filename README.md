# input_monitor
Monitor /dev/input and record activity for tracking active times at the
computer.

## Create package
  > dpkg-buildpackage -b -uc -tc

## Install package
  > sudo dpkg -i ../input-monitor_1.0.0_all.deb

## Remove package
  > sudo apt purge input-monitor

## Further plans (TODO)
- Make lunch-time duration configurable (default is 20 minutes)
- improve summary feature
  - default could be 7-10 days (or last week + actual)
  - somehow we should display all the records (-s 0)
  - somehow we should detect if there are no more older records to speed
    up display
- remove .db file at purge (do not remove at update/remove)
  maybe only at incompatible DB updates?
