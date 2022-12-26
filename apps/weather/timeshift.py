
from datetime import datetime, timezone
import pytz


def timestamp_to_eastern(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    dt = dt.replace(tzinfo=timezone.utc)
    tz = pytz.timezone('US/Eastern')
    dt = dt.astimezone(tz)
    return dt
