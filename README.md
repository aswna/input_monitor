# Overview
Input monitor monitors /dev/input and records any user activity (mouse,
keyboard, etc) for tracking active times at the computer.

This can be useful for single-user systems.

## deb package
### Create deb package
  > dpkg-buildpackage -b -uc -tc

### Install deb package
  > sudo dpkg -i ../input-monitor_1.0.4_all.deb

### Remove deb package
  > sudo apt purge input-monitor

## Usage
### Estimated Time to Departure (ETD)
```
> input-monitor-client etd --lunch-time-duration 45
+-------+----------------+---------------+
|  ETD  | First activity | Last activity |
+-------+----------------+---------------+
| 05:34 |     07:30      |     10:41     |
+-------+----------------+---------------+
```

ETD := First activity + 8 hours + <lunch time duration> - <now>

### Summary
```
> input-monitor-client summary -d 1
+------------+-------------+------------+----------------+---------------+
|    Date    | Active time | Total time | First activity | Last activity |
+------------+-------------+------------+----------------+---------------+
| 2020-11-03 |    04:52    |   07:25    |     07:36      |     15:02     |
| 2020-11-04 |    02:19    |   03:12    |     07:30      |     10:43     |
+------------+-------------+------------+----------------+---------------+
```

After the heading, the first meaningful line is the summary for
yesterday, the second line is the summary for today, tracked so far.

### Output formats
By default the pretty-printed output is generated, but you can select
the plain output format for easier post processing (with scripts).

#### Plain ETD
Using `plain` output format for *ETD* prints the ETD only without the
first- and last activity.

```
> input-monitor-client --format plain etd --lunch-time-duration 45
08:33
```

#### Plain summary
Using `plain` output format for *summary* prints a TAB separated summary.

```
> input-monitor-client --format plain summary -d 0
2020-11-16      00:12   00:15   07:47   08:02
```

## Further plans (TODO)
- option to choose resolution (in the beginning it was 60 seconds, then
  5 seconds, now it is 1 second), this requires a config file, since
  this value is shared on the server-side
- config option in the client for required daily working time (default
  hard-coded setting is 8 hours)
- to be able to show all the summary records
  - with DAYS 0/-1?
- detect if there are no more older records (for larger DAYS)
  - this could speed up the "display" for larger look back times
