"""
WorkRecord model for storing work hours.
"""
from datetime import datetime
from typing import Dict, Union, Optional

class WorkRecord:
    """Represents a work record for a specific date."""
    
    def __init__(self, date: str):
        """
        Initialize a work record.
        
        Args:
            date: Date string in YYYY-MM-DD format
        """
        self.date = date
        self.hours = None  # Direct hours
        self.start_time = None  # Start time
        self.end_time = None  # End time
    
    def set_hours(self, hours: float) -> None:
        """
        Set direct hours.
        
        Args:
            hours: Hours worked
        """
        self.hours = hours
        self.start_time = None
        self.end_time = None
    
    def set_time_range(self, start_time: str, end_time: str) -> None:
        """
        Set time range.
        
        Args:
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
        """
        self.start_time = start_time
        self.end_time = end_time
        self.hours = None
    
    def get_hours(self) -> Optional[float]:
        """
        Get hours worked.
        
        Returns:
            Hours worked or None if not set
        """
        if self.hours is not None:
            return self.hours
        
        if self.start_time and self.end_time:
            from utils.time_utils import calculate_hours_from_range
            return calculate_hours_from_range(self.start_time, self.end_time)
        
        return None
    
    def is_time_range(self) -> bool:
        """
        Check if this record uses time range.
        
        Returns:
            True if time range, False if direct hours
        """
        return self.start_time is not None and self.end_time is not None
    
    def to_dict(self) -> Dict:
        """
        Convert work record to dictionary for serialization.
        
        Returns:
            Dictionary representation of work record
        """
        if self.is_time_range():
            return {
                'date': self.date,
                'type': 'range',
                'start': self.start_time,
                'end': self.end_time
            }
        else:
            return {
                'date': self.date,
                'type': 'direct',
                'hours': self.hours
            }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'WorkRecord':
        """
        Create a WorkRecord instance from dictionary data.
        
        Args:
            data: Dictionary containing work record data
            
        Returns:
            WorkRecord instance
        """
        record = cls(data['date'])
        
        if data.get('type') == 'range':
            record.set_time_range(data['start'], data['end'])
        else:
            record.set_hours(data['hours'])
        
        return record
