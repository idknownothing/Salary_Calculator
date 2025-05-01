"""
Controller for managing tips calculations.
"""
from typing import Dict, List, Tuple
from datetime import datetime
from models.tip_record import TipRecord
from controllers.staff_controller import StaffController

class TipsController:
    """Controller for tips-related operations."""
    
    def __init__(self, staff_controller: StaffController):
        """
        Initialize the tips controller.
        
        Args:
            staff_controller: StaffController instance
        """
        self.tip_record = TipRecord()
        self.staff_controller = staff_controller
    
    def add_tips(self, date: str, amount: float) -> None:
        """
        Add tips for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            amount: Tip amount
        """
        self.tip_record.add_tips(date, amount)
    
    def get_tips_for_date(self, date: str) -> float:
        """
        Get tips for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Tip amount or 0.0 if not found
        """
        return self.tip_record.get_tips_for_date(date) or 0.0
    
    def calculate_tips_distribution(self, year: int, month: int) -> Dict[str, Dict]:
        """
        Calculate tips distribution for a specific month.
        
        Args:
            year: Year as integer
            month: Month as integer (1-12)
            
        Returns:
            Dictionary with staff names as keys and their tip info as values
        """
        # Get total tips for the month
        total_tips = self.tip_record.get_tips_for_month(year, month)
        
        # Get total hours for each staff member
        staff_hours = {}
        for name in self.staff_controller.get_staff_list():
            staff = self.staff_controller.get_staff(name)
            hours = staff.get_hours_for_month(year, month)
            staff_hours[name] = hours
        
        # Calculate total hours
        total_hours = sum(staff_hours.values())
        
        # Calculate tips distribution
        result = {}
        for name, hours in staff_hours.items():
            if total_hours > 0:
                tip_share = (hours / total_hours) * total_tips
            else:
                tip_share = 0
                
            result[name] = {
                'hours': hours,
                'tips': tip_share,
                'percentage': (hours / total_hours * 100) if total_hours > 0 else 0
            }
        
        return result
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """
        Get a complete monthly summary.
        
        Args:
            year: Year as integer
            month: Month as integer (1-12)
            
        Returns:
            Dictionary with summary information
        """
        tips_distribution = self.calculate_tips_distribution(year, month)
        total_tips = self.tip_record.get_tips_for_month(year, month)
        
        total_hours = sum(data['hours'] for data in tips_distribution.values())
        avg_tip_per_hour = total_tips / total_hours if total_hours > 0 else 0
        
        return {
            'year': year,
            'month': month,
            'total_tips': total_tips,
            'total_hours': total_hours,
            'avg_tip_per_hour': avg_tip_per_hour,
            'staff_data': tips_distribution
        }
    
    def to_dict(self) -> Dict:
        """
        Convert tip record data to dictionary for serialization.
        
        Returns:
            Dictionary representation of tip record data
        """
        return self.tip_record.to_dict()
    
    def load_from_dict(self, data: Dict) -> None:
        """
        Load tip record data from dictionary.
        
        Args:
            data: Dictionary containing tip record data
        """
        self.tip_record = TipRecord.from_dict(data)
