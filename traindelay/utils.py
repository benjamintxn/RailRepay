# utils.py
import sys
import re
from typing import List, Tuple, Optional
import datetime
from policies import TOC_REFUND_POLICIES

# If you decide to keep constants.py
try:
    from constants import Constants
    INTERFACE_PATTERN = Constants.INTERFACE_PATTERN
except ImportError:
    # Define the pattern here if constants.py is not used
    INTERFACE_PATTERN = r"([a-zA-Z]{3})\s([a-zA-Z]{3})\s(\d{4})\s(\d{4}-\d{2}-\d{2})"

def arg_parse(user_input: List[str]) -> Tuple[str, str, str, str]:
    """Parses command-line arguments."""
    input_str = " ".join(user_input).strip()

    match = re.fullmatch(INTERFACE_PATTERN, input_str)
    if not match:
        sys.exit("Usage: traindelay <from_loc> <to_loc> <time> <date>\n"
                 "Example: traindelay WAT WOK 0653 2023-10-14")

    from_loc, to_loc, time_str, date_str = match.groups()
    return from_loc, to_loc, time_str, date_str

def calculate_delay(scheduled_arrival: str, actual_arrival: str) -> int:
    """Calculates delay in minutes."""
    fmt = '%H%M'
    scheduled = datetime.datetime.strptime(scheduled_arrival, fmt)
    actual = datetime.datetime.strptime(actual_arrival, fmt)
    delay = (actual - scheduled).total_seconds() / 60
    return int(delay)

def get_refund_percentage(toc_code: str, delay_minutes: int) -> Tuple[float, str]:
    """Determines refund percentage based on TOC policies."""
    policies = TOC_REFUND_POLICIES.get(toc_code, [])
    for policy in policies:
        min_delay, max_delay, refund_pct, *ticket_type = policy
        if min_delay <= delay_minutes <= max_delay:
            ticket_type = ticket_type[0] if ticket_type else 'single'
            return refund_pct, ticket_type
    return 0.0, 'single'