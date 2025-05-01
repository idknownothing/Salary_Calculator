"""
Staff model representing an employee.
"""
from datetime import datetime
from typing import Dict, Union, Optional

class Staff:
    """Represents a staff member with their work records."""
    
    def __init__(self, name: str):
        """
        Initialize a staff member.
        
        Args:
            name: The name of the staff member
        """
        self.name = name
        self.work_records = {}  # {date_str: hours or {start, end}}
    
    def add_hours(self, date: str, hours: float) -> None:
        """
        Add total hours for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            hours: Total hours worked
        """
        self.work_records[date] = hours
    
    def add_time_range(self, date: str, start_time: str, end_time: str) -> None:
        """
        Add start and end times for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
        """
        self.work_records[date] = {'start': start_time, 'end': end_time}
    
    def get_hours_for_date(self, date: str) -> Optional[Union[float, Dict[str, str]]]:
        """
        Get hours worked for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Hours worked or time range dict, None if not found
        """
        return self.work_records.get(date)
    
    def get_hours_for_month(self, year: int, month: int) -> float:
        """
        Calculate total hours worked for a specific month.
        
        Args:
            year: Year as integer
            month: Month as integer (1-12)
            
        Returns:
            Total hours worked in the month
        """
        from utils.time_utils import calculate_hours_from_range
        
        total_hours = 0.0
        for date_str, hours in self.work_records.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.year == year and date_obj.month == month:
                if isinstance(hours, dict):  # Time range
                    total_hours += calculate_hours_from_range(hours['start'], hours['end'])
                else:  # Direct hours
                    total_hours += float(hours)
        return total_hours
    
    def to_dict(self) -> Dict:
        """
        Convert staff data to dictionary for serialization.
        
        Returns:
            Dictionary representation of staff data
        """
        return {
            'name': self.name,
            'work_records': self.work_records
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Staff':
        """
        Create a Staff instance from dictionary data.
        
        Args:
            data: Dictionary containing staff data
            
        Returns:
            Staff instance
        """
        staff = cls(data['name'])
        staff.work_records = data.get('work_records', {})
        return staff
