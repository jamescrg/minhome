
from datetime import datetime, date
import pytz


def show_section(session, section):
    """ shows or hides a given section on the home page

    Args:
        session : a Django session
        section (str): the section to be shown or hidden

    Returns:
        show_section (bool): whether the section is shown or hidden

    Side Effect: ???
        sets the session value for that section
    """

    flag = 'show_' + section
    exp = section + '_hide_expire'

    show_section = session.get(flag, True)

    # if events are hidden, check the date they were hidden
    # if that date is less than today, show them
    if not show_section:

        # get current day
        now = datetime.now(pytz.timezone('US/Eastern'))
        today = now.date()

        # get day events were previously hidden
        timestamp = int(session.get(exp))
        old_date = date.fromtimestamp(timestamp)

        # set events to shown only if today is greater than the old date
        if today > old_date:
            show_section = True
            session[flag] = True

    return show_section


def change_session(session):
    """ a sample function that changes session data """
    session['motto'] = 'Stuff happens.'
    return True
