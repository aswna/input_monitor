"""
DESCRIPTION
  Client for the input monitor service
"""

import argparse
import datetime

from activity_db import ActivityDB

# TODO:
# - refactor / clean-up


def main():
    args = parse_arguments()
    activity_db = ActivityDB()

    now = datetime.datetime.now()
    if args.etd:
        first_activity_today = \
            activity_db.get_timestamp_of_first_activity_on_day(now)
        if first_activity_today:
            print('First activity today: '
                  '{0.hour:02d}:{0.minute:02d}:{0.second:02d} ({1})'
                  .format(
                      datetime.datetime.fromtimestamp(first_activity_today),
                      first_activity_today))
        else:
            print('First activity today: N/A')

        last_activity_today = \
            activity_db.get_timestamp_of_last_activity_on_day(now)
        if last_activity_today:
            print('Last activity today : '
                  '{0.hour:02d}:{0.minute:02d}:{0.second:02d} ({1})'
                  .format(
                      datetime.datetime.fromtimestamp(last_activity_today),
                      last_activity_today))
        else:
            print('Last activity today : N/A')

        if first_activity_today:
            estimated_time_of_departure = datetime.datetime.fromtimestamp(
                first_activity_today + (8 * 60 + 20) * 60)
            estimated_time_to_departure = estimated_time_of_departure - now
            print('ETD: {}'.format(estimated_time_to_departure))
        else:
            print('ETD: N/A')

    elif args.time_spent_with_work is not None:
        for days_back in reversed(range(args.time_spent_with_work + 1)):
            days = datetime.timedelta(days=days_back)
            date, activity_today = activity_db.get_activity_on_day(now - days)
            if activity_today:
                activity = datetime.timedelta(seconds=activity_today)
                print('Activity on {0.year}-{0.month:02d}-{0.day:02d}: {1}'
                      .format(date, activity))
            else:
                print('Activity on {0.year}-{0.month:02d}-{0.day:02d}: N/A'
                      .format(date))

    else:
        print('No action!')


def parse_arguments():
    description = __doc__
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-e', '--etd', action='store_true',
        help='print estimated time to departure')
    group.add_argument(
        '-t', '--time-spent-with-work', type=int,
        help='print times spent with work for the last given days')
    return parser.parse_args()


if __name__ == "__main__":
    main()
