import datetime
import time

import inotify.adapters

from activity_db import ActivityDB

# TODO:
# - clean up DB time-to-time?
# - check performance after deleting obsolete data
# - transform to be a service


def main():
    activity_db = ActivityDB()
    activity_db.create()
    i_notify = inotify.adapters.Inotify()
    i_notify.add_watch('/dev/input', mask=inotify.constants.IN_ALL_EVENTS)

    while True:
        for _event in i_notify.event_gen(yield_nones=False):
            epoch = int(datetime.datetime.now().timestamp())
            activity_db.save_timestamp(epoch)
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
