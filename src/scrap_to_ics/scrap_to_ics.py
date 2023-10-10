from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from pathlib import Path
import pytz
import os
import json

dictionnaire = {
    "title": "Présentation du règlement des études",
    "start_time": {"hours": 10, "minutes": 15},
    "end_time": {"hours": 11, "minutes": 15},
    "professors": ["DJELOUAH Redouane"],
    "groups": ["GRE2 FR", "ING2 EN", "IR2 FR"],
    "location": "Amphi E",
    "date": 28,
}


def scrap_to_ics(
    title: str,
    group: str,
    year: int,
    month: int,
    day: int,
    hour_start: int,
    minute_start: int,
    hour_end: int,
    minute_end: int,
    course: str,
    organizer: str,
):
    # Creat calendar object and event object

    # cal = Calendar()
    event = Event()

    # Compliant properties

    # cal.add('prodid', '-//Calendrier Esaip//example.com//')
    # cal.add('version', '2.0')

    # Add data event

    event.add("summary", title)  # -> pass the title

    # Parse for dtstart et dtend

    event.add(
        "dtstart",
        datetime(
            year, month, day, hour_start, minute_start, 0, tzinfo=pytz.timezone("CEST")
        ),
    )
    event.add(
        "dtend",
        datetime(
            year, month, day, hour_end, minute_end, 0, tzinfo=pytz.timezone("CEST")
        ),
    )

    # Create organizer object

    organizer = vCalAddress(organizer)

    event["location"] = vText(course)  # Pass the class
    event["organizer"] = organizer

    attendee = vCalAddress(group)
    # Add alarm 15min

    alarm = Alarm()
    alarm.add("action", "DISPLAY")
    alarm.add("trigger", timedelta(minutes=-15))

    event.add_component(alarm)  # -> add alarm to event

    return event


def get_year():
    year = ""
    date = str(datetime.today())
    parse = date.split("-")
    year = int(parse[0])
    return year


def get_month():
    month = ""
    date = str(datetime.today())
    parse = date.split("-")
    month = int(parse[1])
    return month


def create_calendar():
    cal = Calendar()
    cal.add("prodid", "-//Calendrier Esaip//example.com//")
    cal.add("version", "2.0")

    return cal


def create_events(events):
    calendar = create_calendar()

    for dictio in events:
        event = scrap_to_ics(
            dictio["title"],
            dictio["groups"],
            get_year(),
            get_month(),
            dictio["date"],
            dictio["start_time"]["hours"],
            dictio["start_time"]["minutes"],
            dictio["end_time"]["hours"],
            dictio["end_time"]["minutes"],
            dictio["location"],
            dictio["professors"],
        )
        calendar.add_component(event)

    return calendar


if __name__ == "__main__":
    with open("logs/2023_09_13_11_27_41/23_24_B1_CYBER.json") as file:
        courses = json.load(file)

        create_events(courses)
