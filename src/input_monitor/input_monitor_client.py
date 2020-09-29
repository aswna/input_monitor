"""
DESCRIPTION
  Client for the input monitor service
"""

import argparse
import datetime

from prettytable import PrettyTable

from input_monitor.activity_db import ActivityDB


def main():
    args = parse_arguments()
    activity_db = ActivityDB()
    handle_arguments(args, activity_db)


def parse_arguments():
    description = __doc__
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-e', '--etd',
        action='store_true',
        help='print estimated time to departure'
    )
    group.add_argument(
        '-s', '--show-summary-for-days',
        action='store_true',
        help='print latest active times summary'
    )

    # TODO: DAYS is used for summary only, MINUTES is used for ETD only
    parser.add_argument(
        '-d', '--days',
        metavar='DAYS',
        type=int,
        default=7 + datetime.datetime.now().weekday(),
        help='set days for summary'
    )
    parser.add_argument(
        '-l', '--lunch-time-duration',
        metavar='MINUTES',
        type=int,
        default=20,
        help='set lunch time duration in minutes'
    )

    return parser.parse_args()


def handle_arguments(args, activity_db):
    now = datetime.datetime.now()
    if args.etd:
        activities = get_the_activities_of_the_day(
            now,
            activity_db,
            args.lunch_time_duration
        )
        print_etd_and_activities(activities)
    elif args.show_summary_for_days:
        activities = get_latest_activities(now, args.days, activity_db)
        print_summary(activities)
    else:
        print('No action!')


def get_the_activities_of_the_day(now, activity_db, lunch_time_duration):
    _date, first_activity_today, last_activity_today, _net_activity = (
        activity_db.get_activity_on_day(now)
    )
    first_activity = get_activity_timepoint(first_activity_today)
    last_activity = get_activity_timepoint(last_activity_today)
    etd = get_estimated_time_of_departure(
        now,
        first_activity_today,
        lunch_time_duration
    )
    return (etd, first_activity, last_activity)


def get_estimated_time_of_departure(
        now,
        first_activity_today,
        lunch_time_duration
):
    if first_activity_today:
        estimated_time_of_departure = datetime.datetime.fromtimestamp(
            first_activity_today + (8 * 60 + lunch_time_duration) * 60
        )
        estimated_time_to_departure = abs(estimated_time_of_departure - now)
        prefix = ''
        if now > estimated_time_of_departure:
            prefix = '!'
        return '{}{}'.format(
            prefix,
            get_activity_duration(estimated_time_to_departure.total_seconds())
        )
    else:
        return 'N/A'


def print_etd_and_activities(activities):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['ETD', 'First activity', 'Last activity']
    pretty_table.add_row(activities)
    print(pretty_table)


def get_latest_activities(now, days, activity_db):
    activities = []
    for days_back in reversed(range(days + 1)):
        days = datetime.timedelta(days=days_back)
        date, first_activity, last_activity, net_activity = (
            activity_db.get_activity_on_day(now - days)
        )
        if first_activity and last_activity and net_activity:
            gross_activity = last_activity - first_activity
            activities.append((
                '{0.year}-{0.month:02d}-{0.day:02d}'.format(date),
                '{}'.format(get_activity_duration(net_activity)),
                '{}'.format(get_activity_duration(gross_activity)),
                '{}'.format(get_activity_timepoint(first_activity)),
                '{}'.format(get_activity_timepoint(last_activity))
            ))
        else:
            activities.append((
                '{0.year}-{0.month:02d}-{0.day:02d}'.format(date),
                'N/A',
                'N/A',
                'N/A',
                'N/A'
            ))
    return activities


def get_activity_timepoint(activity):
    return get_activity_using(datetime.datetime.fromtimestamp, activity)


def get_activity_duration(activity):
    return get_activity_using(datetime.datetime.utcfromtimestamp, activity)


def get_activity_using(func, activity):
    if activity:
        return '{0.hour:02d}:{0.minute:02d}'.format(func(activity))
    else:
        return 'N/A'


def print_summary(activities):
    pretty_table = PrettyTable()
    pretty_table.field_names = [
        'Date',
        'Active time',
        'Total time',
        'First activity',
        'Last activity'
    ]
    for activity in activities:
        pretty_table.add_row(activity)
    print(pretty_table)


if __name__ == "__main__":
    main()
