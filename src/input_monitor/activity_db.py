import datetime
import sqlite3
from pathlib import Path


class ActivityDB:
    def __init__(self):
        db_file = Path.home().joinpath(
            '.local/share/input_monitor/input_monitor.db')
        db_file.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(db_file))
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def create(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS activity (timestamp INTEGER)')

    def save_timestamp(self, date_time):
        first_activity_today = self.get_timestamp_of_first_activity_on_day(
            date_time)
        last_activity_today = self.get_timestamp_of_last_activity_on_day(
            date_time)
        epoch = date_time.timestamp()
        if (
                first_activity_today is not None and
                last_activity_today is not None and
                first_activity_today != last_activity_today
        ):
            self.cursor.execute(
                'UPDATE activity SET timestamp = {} WHERE timestamp = {}'
                .format(epoch, last_activity_today))
        else:
            self.cursor.execute(
                'INSERT INTO activity VALUES ({})'.format(epoch))
        self.connection.commit()

    def get_activity_on_day(self, date_time):
        first_activity_on_day = self.get_timestamp_of_first_activity_on_day(
            date_time)
        last_activity_on_day = self.get_timestamp_of_last_activity_on_day(
            date_time)
        if first_activity_on_day and last_activity_on_day:
            return (date_time, last_activity_on_day - first_activity_on_day)
        else:
            return (date_time, None)

    def get_timestamp_of_first_activity_on_day(self, date_time):
        start_of_day = datetime.datetime(
            date_time.year, date_time.month, date_time.day)
        epoch_at_start_of_day = int(start_of_day.timestamp())
        self.cursor.execute(
            'SELECT MIN(timestamp) FROM activity WHERE timestamp >= {}'
            .format(epoch_at_start_of_day))
        return self.cursor.fetchone()[0]

    def get_timestamp_of_last_activity_on_day(self, date_time):
        start_of_day = datetime.datetime(
            date_time.year, date_time.month, date_time.day)
        epoch_at_start_of_day = int(start_of_day.timestamp())
        start_of_next_day = start_of_day + datetime.timedelta(days=1)
        epoch_at_start_of_next_day = int(start_of_next_day.timestamp())
        self.cursor.execute(
            'SELECT MAX(timestamp) FROM activity '
            'WHERE timestamp >= {} AND timestamp < {}'
            .format(epoch_at_start_of_day, epoch_at_start_of_next_day))
        return self.cursor.fetchone()[0]
