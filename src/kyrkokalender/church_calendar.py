from datetime import datetime

import pytz
from icalendar import Calendar, Event

from kyrkokalender import feast_formatters


def event_for_feast(year: int, feast: dict) -> Event:
    feast_id = feast["id"]
    date = datetime.fromisoformat(feast["startDate"]).date()
    event = Event()
    event.add("summary", feast["feastName"])
    event.add("description", feast_formatters.format_description(feast))
    event.add("dtstart", date)
    event.add("dtstamp", datetime.now().replace(tzinfo=pytz.timezone("Europe/Stockholm")))
    event.add("uid", f"feast-{year}-{feast_id}@svenskakyrkan.se")
    event.add(
        "url",
        f"https://www.svenskakyrkan.se/kyrkoaret/bibeltexter?id={feast_id}&year={year}",
    )
    return event


def create_calendar() -> Calendar:
    calendar = Calendar()
    calendar.add("prodid", "+//IDN skogsfors.net")
    calendar.add("version", "2.0")
    return calendar


def calendar_for_feasts(year: int, feasts: dict) -> Calendar:
    calendar = create_calendar()
    for feast in feasts:
        event = event_for_feast(year, feast)
        calendar.add_component(event)
    return calendar
