"""
Controller for managing data persistence.
"""
import os
import json
from datetime import datetime
from typing import Dict, Optional
from controllers.staff_controller import StaffController
from controllers.tips_controller import TipsController

class DataController:
    """Controller for data persistence operations."""
    
    def __init__(self):
        """Initialize the data controller."""
        self.data_dir = "data"
        self.ensure_data_dir()
        
        self.staff_controller = StaffController()
        self.tips_controller = TipsController(self.staff_controller)
        
        self.load_data()
    
    def ensure_data_dir(self) -> None:
        """Ensure the data directory exists."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_current_data_file(self) -> str:
        """
        Get the path to the current data file.
        
        Returns:
            Path to the current data file
        """
        return os.path.join(self.data_dir, "current_data.json")
    
    def get_monthly_data_file(self, year: int, month: int) -> str:
        """
        Get the path to a monthly data file.
        
        Args:
            year: Year as integer
            month: Month as integer (1-12)
            
        Returns:
            Path to the monthly data file
        """
        return os.path.join(self.data_dir, f"{year}_{month:02d}_data.json")
    
    def load_data(self) -> None:
        """Load data from the current data file."""
        file_path = self.get_current_data_file()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                    if 'staff' in data:
                        self.staff_controller.load_from_dict(data['staff'])
                    
                    if 'tips' in data:
                        self.tips_controller.load_from_dict(data['tips'])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data: {e}")
    
    def save_data(self) -> None:
        """Save data to the current data file."""
        file_path = self.get_current_data_file()
        try:
            data = {
                'staff': self.staff_controller.to_dict(),
                'tips': self.tips_controller.to_dict()
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def save_monthly_data(self, year: int, month: int) -> bool:
        """
        Save data for a specific month to a dedicated file.
        
        Args:
            year: Year as integer
            month: Month as integer (1-12)
            
        Returns:
            True if saved successfully, False otherwise
        """
        file_path = self.get_monthly_data_file(year, month)
        try:
            # Get monthly summary
            monthly_summary = self.tips_controller.get_monthly_summary(year, month)
            
            # Get all staff data for the month
            staff_data = {}
            for name in self.staff_controller.get_staff_list():
                staff = self.staff_controller.get_staff(name)
                work_records = {}
                
                for date_str, hours in staff.work_records.items():
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    if date_obj.year == year and date_obj.month == month:
                        work_records[date_str] = hours
                
                if work_records:
                    staff_data[name] = work_records
            
            # Get all tips data for the month
            tips_data = {}
            for date_str in self.tips_controller.tip_record.get_dates_with_tips():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj.year == year and date_obj.month == month:
                    tips_data[date_str] = self.tips_controller.get_tips_for_date(date_str)
            
            # Combine all data
            data = {
                'year': year,
                'month': month,
                'summary': monthly_summary,
                'staff_data': staff_data,
                'tips_data': tips_data
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving monthly data: {e}")
            return False
