# services.py
import os
import sys
import requests
from dotenv import load_dotenv
from typing import Tuple, Dict
import datetime
import calendar

load_dotenv()

class ServiceMetric:
    """Handles communication with the HSP API Service Metrics component."""

    def __init__(self, from_loc: str, to_loc: str, from_date: str, from_time: str) -> None:
        self.url: str = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
        self.auth: Tuple[str, str] = (os.environ["DARWIN_EMAIL"], os.environ["DARWIN_PASS"])
        self.headers: Dict[str, str] = {"Content-Type": "application/json"}
        self.from_loc = from_loc.upper()
        self.to_loc = to_loc.upper()
        self.from_date = from_date
        self.to_date = self.from_date
        self.from_time = from_time
        self.to_time = self.to_time_calculator(self.from_time)
        self.day = self.get_day_type(self.from_date)

        # POST request parameters
        self.params = {
            "from_loc": self.from_loc,
            "to_loc": self.to_loc,
            "from_time": self.from_time,
            "to_time": self.to_time,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "days": self.day
        }

    @staticmethod
    def to_time_calculator(time_str: str, delta: int = 60) -> str:
        """Calculates the 'to_time' by adding delta minutes to 'from_time'."""
        fmt = '%H%M'
        time_obj = datetime.datetime.strptime(time_str, fmt)
        time_obj += datetime.timedelta(minutes=delta)
        return time_obj.strftime('%H%M')

    @staticmethod
    def get_day_type(date_str: str) -> str:
        """Determines the day type for the given date."""
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        weekday = date_obj.weekday()
        if weekday >= 0 and weekday <= 4:
            return "WEEKDAY"
        elif weekday == 5:
            return "SATURDAY"
        else:
            return "SUNDAY"

    def post_service_metrics(self) -> None:
        """Sends a POST request to the HSP Service Metrics API."""
        response = requests.post(
            url=self.url,
            json=self.params,
            headers=self.headers,
            auth=self.auth
        )
        if response.status_code != 200:
            sys.exit(f"Service Metrics POST request failed with status code {response.status_code}.")
        self.response = response

class ServiceDetail:
    """Handles communication with the HSP API Service Details component."""

    def __init__(self, rid: str) -> None:
        self.url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
        self.auth = (os.environ["DARWIN_EMAIL"], os.environ["DARWIN_PASS"])
        self.headers = {"Content-Type": "application/json"}
        self.params = {"rid": rid}
        self.toc_code = ''

    def post_service_detail(self) -> None:
        """Sends a POST request to the HSP Service Details API."""
        response = requests.post(
            url=self.url,
            json=self.params,
            headers=self.headers,
            auth=self.auth
        )
        if response.status_code != 200:
            sys.exit(f"Service Detail POST request failed with status code {response.status_code}.")
        self.response = response
        # Extract toc_code from the response
        self.toc_code = self.response.json()["serviceAttributesDetails"]["toc_code"]