# input_monitor
Monitor /dev/input and record any user activity (mouse, keyboard, etc)
for tracking active times at the computer.

## Create package
  > dpkg-buildpackage -b -uc -tc

## Install package
  > sudo dpkg -i ../input-monitor_1.0.3_all.deb

## Remove package
  > sudo apt purge input-monitor

## Usage
### Estimated Time to Departure (ETD)
```
> input-monitor-client etd --lunch-time-duration 45
+-------+----------------+---------------+
|  ETD  | First activity | Last activity |
+-------+----------------+---------------+
| 05:34 |     07:30      |     10:41     |  <-- ETD = First activity + 8 hours + <lunch time duration> - <now>
+-------+----------------+---------------+
```

### Summary
```
> input-monitor-client summary -d 1
+------------+-------------+------------+----------------+---------------+
|    Date    | Active time | Total time | First activity | Last activity |
+------------+-------------+------------+----------------+---------------+
| 2020-11-03 |    04:52    |   07:25    |     07:36      |     15:02     |  <-- yesterday
| 2020-11-04 |    02:19    |   03:12    |     07:30      |     10:43     |  <-- today (activity so far)
+------------+-------------+------------+----------------+---------------+
```

## Further plans (TODO)
- config option for required daily working time (default hard-coded setting is 8 hours)
- to be able to display all the summary records
  - with DAYS 0/-1?
- detect if there are no more older records (for larger DAYS)
  - this could speed up the "display" for larger look back times
