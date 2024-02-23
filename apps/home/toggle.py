from datetime import date, datetime

import pytz


def check_if_enabled(user, section):
    """Checks whether a home page feature is enabled.

    Args:
        user : a request customuser
        section (str): a home page feature (section of home page)

    Returns:
        enabled (bool): whether the section is shown or hidden

    """
    # if user has enabled the section, the user's "home_{section}"
    # attribute will have a values of "1" aka "True"
    attrib = (f"home_{section}")
    enabled = getattr(user, attrib)
    return enabled


def check_if_hidden(user, section):
    """Checks whether a home page feature is hidden.

    Args:
        user : a request customuser
        section (str): a home page feature (section of home page)

    Returns:
        hidden (datetime.date): the date the section was hidden, or None

    """
    # A section that is enabled is shown by default.
    # A user may hide the section, in which case the user's
    # "home_{section}_hidden" attribute will be stamped with the date
    # on which the section was hidden.
    # This function therefore returns a date if the section was hidden
    # or false if the section is shown.
    attrib = (f"home_{section}_hidden")
    hidden = getattr(user, attrib)
    return hidden


def check_if_hidden_expired(user, section, hidden):
    """Checks whether the interval for which the feature was hidden has expired

    Args:
        user : a request customuser
        section (str): a home page feature (section of home page)
        hidden (datetime.date): the date the section was hidden

    Returns:
        expired (bool): whether the hidden interval has expired

    """
    # A section remains hidden for a period of one day. After that,
    # it returns to the home screen. This function creates that behavior.
    # If the "home_{section}_hidden" value is less than the current day,
    # the section will be shown.
    now = datetime.now(pytz.timezone("US/Eastern"))
    today = now.date()
    return today > hidden


def show_section(user, section):
    """Sets the value of show section variable

    Args:
        user : a request customuser
        section (str): the section to be shown or hidden

    Returns:
        show_section (bool): whether the section is shown or hidden

    Notes:
        False means don't show the section
        True means shows the section

    """

    # check whether the section has been enabled in the "settings" app
    # if so, return the value False to the "show_{section}"
    # variable in the index view
    enabled = check_if_enabled(user, section)

    # this is a double negative so "True" will continue to the next
    # conditional test
    if not enabled:
        return False

    # check whether the user has hidden the section for the day
    # if so, return the value False to the "show_{section}"
    # variable in the index view
    hidden = check_if_hidden(user, section)

    # this is a double negative so "True" will continue to the next
    # conditional test
    if not hidden:
        return True

    # check whether the section hide time has experied
    # (i.e. it's the next day)
    hidden_expired = check_if_hidden_expired(user, section, hidden)
    if hidden_expired:
        attrib = (f"home_{section}_hidden")
        setattr(user, attrib, None)
        user.save()
        return True

    else:
        return False
