import datetime
import time

import inotify.adapters

from activity_db import ActivityDB


def main():
    activity_db = ActivityDB()
    activity_db.create()
    i_notify = inotify.adapters.Inotify()
    i_notify.add_watch('/dev/input', mask=inotify.constants.IN_ALL_EVENTS)

    while True:
        for _event in i_notify.event_gen(yield_nones=False):
            now = datetime.datetime.now()
            activity_db.save_timestamp(now)
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
