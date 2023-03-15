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
    now = datetime.now(pytz.timezone("US/Eastern"))
    today = now.date()
    return today > hidden


def show_section(user, section):
    """shows or hides a given section on the home page

    Args:
        user : a request customuser
        section (str): the section to be shown or hidden

    Returns:
        show_section (bool): whether the section is shown or hidden

    """

    enabled = check_if_enabled(user, section)
    if not enabled:
        return False

    hidden = check_if_hidden(user, section)
    if hidden:
        return False

    expired = check_if_hidden_expired(user, section, hidden)
    if not expired:
        return False

    return True
