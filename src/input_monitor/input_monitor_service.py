import datetime
import time

import pyinotify

from activity_db import ActivityDB


def main():
    activity_db = ActivityDB()
    activity_db.create()
    wm = pyinotify.WatchManager()
    wm.add_watch('/dev/input', mask=pyinotify.ALL_EVENTS)
    timeout = 60
    notifier = pyinotify.Notifier(wm, None, timeout=timeout)

    while True:
        while notifier.check_events():
            notifier.read_events()
            now = datetime.datetime.now()
            activity_db.save_timestamp(now)
            break
        time.sleep(timeout)


if __name__ == "__main__":
    main()
