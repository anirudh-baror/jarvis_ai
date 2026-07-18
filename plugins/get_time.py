import datetime

def get_current_time():
    """Returns the current time in HH:MM AM/PM format.

    Use this whenever the user asks what time it is right now.
    """
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")