"""Course class module"""
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Course:
    """Course class"""

    title: str
    start_time: Dict[str, str]
    end_time: Dict[str, str]
    professors: list[str]
    location: str
    date: int
    group: Optional[str] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @staticmethod
    def from_dict(obj):
        """Initialize the Course from a dictionnary"""
        start_datetime = datetime.fromisoformat(obj["start_datetime"])
        end_datetime = datetime.fromisoformat(obj["end_datetime"])

        start_time = {
            "hours": start_datetime.hour,
            "minutes": start_datetime.minute,
        }

        end_time = {
            "hours": end_datetime.hour,
            "minutes": end_datetime.minute,
        }

        return Course(
            obj["title"],
            start_time,
            end_time,
            obj["professors"],
            obj["location"],
            start_datetime.day,
            obj["group"],
            start_datetime.month,
            start_datetime.year,
        )

    def as_dict(self):
        """Return the course as a dictionnary"""
        return {
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "professors": self.professors,
            "group": self.group,
            "location": self.location,
            "date": self.date,
            "month": self.month,
            "year": self.year,
        }

    def as_supabase_dict(self):
        """Return the course as a dictionnary (for supabase)"""
        sth = self.start_time["hours"]
        stm = self.start_time["minutes"]

        eth = self.end_time["hours"]
        etm = self.end_time["minutes"]

        start_date = (
            datetime(self.year, self.month, self.date, sth, stm, 0).strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )
            + "+02:00"
        )

        end_date = (
            datetime(self.year, self.month, self.date, eth, etm, 0).strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )
            + "+02:00"
        )

        return {
            "title": self.title,
            "description": "",
            "start_datetime": start_date,
            "end_datetime": end_date,
            "group": self.group,
            "professors": self.professors,
            "location": self.location,
        }

    @staticmethod
    def set_month(courses: list["Course"], month: int):
        """Set the course month value"""
        for course in courses:
            course.month = month

    @staticmethod
    def set_year(courses: list["Course"], year: int):
        """Set the course year value"""
        for course in courses:
            course.year = year

    @staticmethod
    def set_group(courses: list["Course"], group: str):
        """Set the course group value"""
        for course in courses:
            course.group = group
