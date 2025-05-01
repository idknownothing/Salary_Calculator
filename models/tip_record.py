"""
TipRecord model for storing daily tips.
"""
from datetime import datetime
from typing import Dict, List, Optional

class TipRecord:
    """Manages tip records for the store."""
    
    def __init__(self):
        """Initialize the tip record."""
        self.daily_tips = {}  # {date_str: amount}
    
    def add_tips(self, date: str, amount: float) -> None:
        """
        Add tips for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            amount: Tip amount
        """
        self.daily_tips[date] = amount
    
    def get_tips_for_date(self, date: str) -> Optional[float]:
        """
        Get tips for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Tip amount or None if not found
        """
        return self.daily_tips.get(date)
    
    def get_tips_for_month(self, year: int, month: int) -> float:
        """
        Calculate total tips for a specific month.
        
        Args:
            year: Year as integer
            month: Month as integer (1-12)
            
        Returns:
            Total tips for the month
        """
        total_tips = 0.0
        for date_str, amount in self.daily_tips.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.year == year and date_obj.month == month:
                total_tips += amount
        return total_tips
    
    def get_dates_with_tips(self) -> List[str]:
        """
        Get all dates that have tips recorded.
        
        Returns:
            List of date strings
        """
        return list(self.daily_tips.keys())
    
    def to_dict(self) -> Dict:
        """
        Convert tip record data to dictionary for serialization.
        
        Returns:
            Dictionary representation of tip record data
        """
        return {
            'daily_tips': self.daily_tips
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TipRecord':
        """
        Create a TipRecord instance from dictionary data.
        
        Args:
            data: Dictionary containing tip record data
            
        Returns:
            TipRecord instance
        """
        tip_record = cls()
        tip_record.daily_tips = data.get('daily_tips', {})
        return tip_record
