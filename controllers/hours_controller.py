"""
Controller for managing hours tracking.
"""
from typing import Dict, Optional, Tuple, List
from datetime import datetime
from controllers.staff_controller import StaffController
from utils.time_utils import validate_time_format, calculate_hours_from_range

class HoursController:
    """Controller for hours-related operations."""
    
    def __init__(self, staff_controller: StaffController):
        """
        Initialize the hours controller.
        
        Args:
            staff_controller: StaffController instance
        """
        self.staff_controller = staff_controller
    
    def add_hours(self, name: str, date: str, hours: float) -> Tuple[bool, str]:
        """
        Add hours for a staff member on a specific date.
        
        Args:
            name: Name of the staff member
            date: Date string in YYYY-MM-DD format
            hours: Hours worked
            
        Returns:
            Tuple of (success, message)
        """
        if hours < 0:
            return False, "Hours cannot be negative"
        
        success = self.staff_controller.add_hours(name, date, hours)
        if success:
            return True, f"Hours saved for {name}"
        else:
            return False, f"Staff member {name} not found"
    
    def add_time_range(self, name: str, date: str, start_time: str, end_time: str) -> Tuple[bool, str]:
        """
        Add time range for a staff member on a specific date.
        
        Args:
            name: Name of the staff member
            date: Date string in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            
        Returns:
            Tuple of (success, message)
        """
        # Validate time formats
        if not validate_time_format(start_time):
            return False, "Start time must be in HH:MM format"
        
        if not validate_time_format(end_time):
            return False, "End time must be in HH:MM format"
        
        success = self.staff_controller.add_time_range(name, date, start_time, end_time)
        if success:
            return True, f"Time range saved for {name}"
        else:
            return False, f"Staff member {name} not found"
    
    def get_hours_for_date(self, name: str, date: str) -> Tuple[bool, Optional[Dict]]:
        """
        Get hours or time range for a staff member on a specific date.
        
        Args:
            name: Name of the staff member
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Tuple of (success, data)
            data can be:
            - None if not found
            - float if direct hours
            - dict with 'start' and 'end' if time range
        """
        staff = self.staff_controller.get_staff(name)
        if not staff:
            return False, None
        
        hours_data = staff.get_hours_for_date(date)
        return True, hours_data
    
    def get_daily_hours_summary(self, date: str) -> Dict[str, Dict]:
        """
        Get a summary of hours for all staff on a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Dictionary with staff names as keys and their hours info as values
        """
        result = {}
        for name in self.staff_controller.get_staff_list():
            success, hours_data = self.get_hours_for_date(name, date)
            
            if success and hours_data is not None:
                if isinstance(hours_data, dict):  # Time range
                    hours = calculate_hours_from_range(hours_data['start'], hours_data['end'])
                    result[name] = {
                        'type': 'range',
                        'start': hours_data['start'],
                        'end': hours_data['end'],
                        'hours': hours
                    }
                else:  # Direct hours
                    result[name] = {
                        'type': 'direct',
                        'hours': float(hours_data)
                    }
            else:
                result[name] = {
                    'type': 'none',
                    'hours': 0.0
                }
        
        return result
