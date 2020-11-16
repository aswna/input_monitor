import sqlite3
from pathlib import Path


class ActivityDB:
    timeout = 1  # seconds

    def __init__(self):
        db_file = Path('/var/lib/input_monitor/input_monitor.db')
        db_file.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(db_file))
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    @staticmethod
    def date_to_text(date_time):
        return '{}-{:02d}-{:02d}'.format(
            date_time.year,
            date_time.month,
            date_time.day
        )

    def create(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS activity ('
            '  date TEXT, '
            '  first_activity INTEGER, '
            '  last_activity INTEGER, '
            '  net_activity INTEGER'
            ')'
        )

    def save_timestamp(self, date_time):
        date_text = self.date_to_text(date_time)
        epoch = int(date_time.timestamp())
        if self.has_entry_for_today(date_text):
            self.cursor.execute(
                'UPDATE activity '
                'SET last_activity = {}, net_activity = net_activity + {} '
                'WHERE date == "{}"'
                .format(
                    epoch,
                    self.timeout,
                    date_text
                )
            )
        else:
            self.cursor.execute(
                f'INSERT INTO activity VALUES '
                f'("{date_text}", {epoch}, {epoch}, 0)'
            )
        self.connection.commit()

    def get_activity_on_day(self, date_time):
        date_text = self.date_to_text(date_time)
        self.cursor.execute(
            'SELECT first_activity, last_activity, net_activity '
            'FROM activity '
            'WHERE date == "{}"'
            .format(date_text)
        )
        result = self.cursor.fetchone()
        return (
            date_time,
            result[0],
            result[1],
            result[2]
        ) if result else (
            date_time,
            None,
            None,
            None
        )

    def has_entry_for_today(self, date_text):
        self.cursor.execute(
            'SELECT 1 FROM activity WHERE date == "{}"'.format(date_text)
        )
        return bool(self.cursor.fetchone())
