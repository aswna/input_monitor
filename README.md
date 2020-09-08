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
- rework DB and activity_db
  - use table schema:
    DATE | first activity epoch | last activity epoch | net activity
- calculate & store net activity (increase on activity & store it every minute)
- remove .db file at purge (do not remove at update/remove)
