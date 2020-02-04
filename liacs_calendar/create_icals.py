import datetime
from os import path

try:
    from icalendar import Calendar, Event, vText
except ImportError:
    print("Please install all dependencies using `pip install -r requirements.txt`")
    exit(-1)

__calendar__ = None

def create_calendar() -> Calendar:
    """Initialises a Calendar object
    """
    c = Calendar()

    c.add("prodid", "-//LIACS calendar generator//nboonstra.nl//")
    c.add("version", "2.0")

    global __calendar__
    __calendar__ = c

    return c

def create_ical(title: str, dtstart: datetime.datetime, dtend: datetime.datetime, location: str, cal: Calendar, past_events=True) -> None:
    """Create an ical event with the information given in parameters. The event will be added 
    to the calendar, which is passed to the function in the cal parameter.

    :param title: Title of the event
    :type title: str
    :param dtstart: The date and time when the event starts
    :type dtstart: datetime.datetime
    :param dtstop: Date and time when the event stops
    :
    """
    if type(dtstart) is not datetime.datetime and type(dtend) is not datetime.datetime:
        raise TypeError("dtstart and/or dtstop must both be of type datetime.datetime")

    if dtend < dtstart:
        raise ValueError("The end date lies before the start date. Please check your input.")

    global __calendar__
    if type(cal) is not Calendar and not __calendar__:
        raise RuntimeError("Please provide a calendar or run create_calendar.")

    if __calendar__:
        c = __calendar__
    else:
        c = cal

    now = datetime.datetime.now(tz=dtstart.tzinfo)

    if not past_events and dtstart < now:
        #Does not raise an error
        print("Start date+time of event {} lies in the past ({})".format(title, dtstart.isoformat(sep=" ", timespec="seconds")))
        return

    e = Event()

    e.add("dtstart", dtstart)
    e.add("dtend", dtend)
    e.add("location", vText(location))
    e.add("summary", title)
    

    c.add_component(e)

def write_schedule(f: str, cal: Calendar = None) -> None:
    if type(f) is not str:
        raise TypeError("Parameter f must be of type str")

    global __calendar__
    if type(cal) is not Calendar and not __calendar__:
        raise RuntimeError("Please provide a calendar or run create_calendar.")


    if __calendar__:
        c = __calendar__
    else:
        c = cal

    with open(f, "wb") as writer:
        writer.write(c.to_ical())    
