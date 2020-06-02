"""
DESCRIPTION
  Client for the input monitor service
"""

import argparse
import datetime

from prettytable import PrettyTable

from activity_db import ActivityDB


def main():
    args = parse_arguments()
    activity_db = ActivityDB()
    handle_arguments(args, activity_db)


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
        '-s', '--show-summary-for-days', metavar='DAYS', type=int,
        help='print times spent with work for the last given days')
    return parser.parse_args()


def handle_arguments(args, activity_db):
    now = datetime.datetime.now()
    if args.etd:
        activities = get_the_activities_of_the_day(now, activity_db)
        print_etd_and_activities(activities)
    elif args.show_summary_for_days is not None:
        activities = get_latest_activities(now, args, activity_db)
        print_summary(activities)
    else:
        print('No action!')


def get_the_activities_of_the_day(now, activity_db):
    first_activity_today = \
        activity_db.get_timestamp_of_first_activity_on_day(now)
    first_activity = get_activity(first_activity_today)

    last_activity_today = \
        activity_db.get_timestamp_of_last_activity_on_day(now)
    last_activity = get_activity(last_activity_today)

    etd = get_estimated_time_of_departure(now, first_activity_today)
    return (first_activity, last_activity, etd)


def get_activity(activity_today):
    if activity_today:
        return (
            '{0.hour:02d}:{0.minute:02d}:{0.second:02d} ({1})'
            .format(datetime.datetime.fromtimestamp(activity_today),
                    activity_today))
    else:
        return 'N/A'


def get_estimated_time_of_departure(now, first_activity_today):
    if first_activity_today:
        estimated_time_of_departure = datetime.datetime.fromtimestamp(
            first_activity_today + (8 * 60 + 20) * 60)
        estimated_time_to_departure = estimated_time_of_departure - now
        return '{}'.format(estimated_time_to_departure)
    else:
        return 'N/A'


def print_etd_and_activities(activities):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['First activity', 'Last activity', 'ETD']
    pretty_table.add_row(activities)
    print(pretty_table)


def get_latest_activities(now, args, activity_db):
    activities = []
    for days_back in reversed(range(args.show_summary_for_days + 1)):
        days = datetime.timedelta(days=days_back)
        date, activity_today = activity_db.get_activity_on_day(now - days)
        if activity_today:
            activity = datetime.timedelta(seconds=activity_today)
            activities.append((
                '{0.year}-{0.month:02d}-{0.day:02d}'.format(date),
                '{}'.format(activity)))
        else:
            activities.append((
                '{0.year}-{0.month:02d}-{0.day:02d}'.format(date),
                'N/A'))
    return activities


def print_summary(activities):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Date', 'Time spent with work']
    for activity in activities:
        pretty_table.add_row(activity)
    print(pretty_table)


if __name__ == "__main__":
    main()
