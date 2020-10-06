# input_monitor
Monitor /dev/input and record activity for tracking active times at the
computer.

## Create package
  > dpkg-buildpackage -b -uc -tc

## Install package
  > sudo dpkg -i ../input-monitor_1.0.1_all.deb

## Remove package
  > sudo apt purge input-monitor

## Further plans (TODO)
- handle .db file
  - remove .db file at purge
  - do not remove it at update/remove
    - maybe only at incompatible DB updates?

- improve summary feature
  - somehow we should display all the records
    - with -s 0?
  - somehow we should detect if there are no more older records
    - this could speed up the "display" for larger look back times

- record more detailed output?
  - that could be put on charts
  - create a GUI for this?
