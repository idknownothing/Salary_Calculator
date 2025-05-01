"""
Utility functions for time calculations.
"""
import re
from datetime import datetime, timedelta
from typing import Union

def validate_time_format(time_str: str) -> bool:
    """
    Validate that a string is in HH:MM format.
    
    Args:
        time_str: Time string to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
    return bool(re.match(pattern, time_str))

def calculate_hours_from_range(start_time: str, end_time: str) -> float:
    """
    Calculate hours between start and end times.
    
    Args:
        start_time: Start time in HH:MM format
        end_time: End time in HH:MM format
        
    Returns:
        Hours as float
    """
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        
        # Handle overnight shifts
        if end < start:
            end += timedelta(days=1)
        
        # Calculate duration in hours
        duration = (end - start).total_seconds() / 3600
        return round(duration, 2)
    except ValueError:
        return 0.0

def format_hours(hours: Union[float, int]) -> str:
    """
    Format hours as a string with 2 decimal places.
    
    Args:
        hours: Hours as float or int
        
    Returns:
        Formatted hours string
    """
    return f"{float(hours):.2f}"

def get_month_name(month: int) -> str:
    """
    Get the name of a month from its number.
    
    Args:
        month: Month number (1-12)
        
    Returns:
        Month name
    """
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return months[month - 1]
