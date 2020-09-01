# input_monitor
Monitor /dev/input and record activity for tracking active times at the
computer.

## Create package
  > dpkg-buildpackage -b -uc -tc

## Install package
  > sudo dpkg -i ../input-monitor_1.0.0_all.deb

## Remove package
  > sudo apt purge input-monitor
