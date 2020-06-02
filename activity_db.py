import datetime
import sqlite3
from pathlib import Path

# TODO: experiment with DB format for better performance
#         - store date?
#         - store start of day?


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

    def save_timestamp(self, timestamp):
        self.cursor.execute(
            'INSERT INTO activity VALUES ({})'.format(timestamp))
        self.connection.commit()

    def get_activity_on_day(self, timestamp):
        first_activity_on_day = self.get_timestamp_of_first_activity_on_day(
            timestamp)
        last_activity_on_day = self.get_timestamp_of_last_activity_on_day(
            timestamp)
        if first_activity_on_day and last_activity_on_day:
            return (timestamp, last_activity_on_day - first_activity_on_day)
        else:
            return (timestamp, None)

    def get_timestamp_of_first_activity_on_day(self, timestamp):
        start_of_day = datetime.datetime(
            timestamp.year, timestamp.month, timestamp.day)
        epoch_at_start_of_day = int(start_of_day.timestamp())
        self.cursor.execute(
            'SELECT MIN(timestamp) FROM activity WHERE timestamp >= {}'
            .format(epoch_at_start_of_day))
        return self.cursor.fetchone()[0]

    def get_timestamp_of_last_activity_on_day(self, timestamp):
        start_of_day = datetime.datetime(
            timestamp.year, timestamp.month, timestamp.day)
        epoch_at_start_of_day = int(start_of_day.timestamp())
        start_of_next_day = start_of_day + datetime.timedelta(days=1)
        epoch_at_start_of_next_day = int(start_of_next_day.timestamp())
        self.cursor.execute(
            'SELECT MAX(timestamp) FROM activity '
            'WHERE timestamp >= {} AND timestamp < {}'
            .format(epoch_at_start_of_day, epoch_at_start_of_next_day))
        return self.cursor.fetchone()[0]
