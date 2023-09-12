from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from pathlib import Path
import pytz
import os

def scrap_to_ics(title, group, year, month, day, hour, minute, course, organizer):

    # Creat calendar object and event object

    cal = Calendar()
    event = Event()

    # Compliant properties

    cal.add('prodid', '-//Calendrier Esaip//example.com//')
    cal.add('version', '2.0')

    # Add data event

    event.add('name', title) # -> pass the title

    # Parse for dtstart et dtend

    event.add('dtstart', datetime(year, month, day, hour, minute, 0, tzinfo=pytz.utc))
    event.add('dtend', datetime(year, month, day, hour, minute, 0, tzinfo=pytz.utc))

    # Create organizer object

    organizer = vCalAddress(organizer)

    event['location'] = vText(course) # Pass the class
    event['organizer'] = organizer

    # Add alarm 15min

    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('trigger', timedelta(minutes=-15))
    event.add_component(alarm) # -> add alarm to event

    # Add event to calendar
    cal.add_component(event)

    # Create the file and save it
    directory = Path.cwd() / 'MyCalendar' # "MyCalendar" -> name of the directory
    try:
        directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("Folder already exists")
    else:
        print("Folder was created")

    f = open(os.path.join(directory, 'exampl4.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()