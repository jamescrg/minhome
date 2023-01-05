
from datetime import datetime, timezone
import pytz


def timestamp_to_eastern(timestamp):
    """Convert a timestamp in UTC to a datetime object showing Eastern time.

    Args:
        id (timestamp): a unix timestamp representing a specfic point in time

    Returns:
        dt (datetime): a datetime object showing Eastern time
    """

    dt = datetime.fromtimestamp(timestamp)
    dt = dt.replace(tzinfo=timezone.utc)
    tz = pytz.timezone('US/Eastern')
    dt = dt.astimezone(tz)
    return dt
