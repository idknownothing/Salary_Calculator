"""
Controller for managing staff operations.
"""
from typing import Dict, List, Optional
from models.staff import Staff

class StaffController:
    """Controller for staff-related operations."""
    
    def __init__(self):
        """Initialize the staff controller."""
        self.staff_members = {}  # {name: Staff}
    
    def add_staff(self, name: str) -> bool:
        """
        Add a new staff member.
        
        Args:
            name: Name of the staff member
            
        Returns:
            True if added successfully, False if already exists
        """
        if name in self.staff_members:
            return False
        
        self.staff_members[name] = Staff(name)
        return True
    
    def remove_staff(self, name: str) -> bool:
        """
        Remove a staff member.
        
        Args:
            name: Name of the staff member
            
        Returns:
            True if removed successfully, False if not found
        """
        if name not in self.staff_members:
            return False
        
        del self.staff_members[name]
        return True
    
    def get_staff_list(self) -> List[str]:
        """
        Get a list of all staff names.
        
        Returns:
            List of staff names
        """
        return sorted(self.staff_members.keys())
    
    def get_staff(self, name: str) -> Optional[Staff]:
        """
        Get a staff member by name.
        
        Args:
            name: Name of the staff member
            
        Returns:
            Staff object or None if not found
        """
        return self.staff_members.get(name)
    
    def add_hours(self, name: str, date: str, hours: float) -> bool:
        """
        Add hours for a staff member on a specific date.
        
        Args:
            name: Name of the staff member
            date: Date string in YYYY-MM-DD format
            hours: Hours worked
            
        Returns:
            True if added successfully, False if staff not found
        """
        staff = self.get_staff(name)
        if not staff:
            return False
        
        staff.add_hours(date, hours)
        return True
    
    def add_time_range(self, name: str, date: str, start_time: str, end_time: str) -> bool:
        """
        Add time range for a staff member on a specific date.
        
        Args:
            name: Name of the staff member
            date: Date string in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            
        Returns:
            True if added successfully, False if staff not found
        """
        staff = self.get_staff(name)
        if not staff:
            return False
        
        staff.add_time_range(date, start_time, end_time)
        return True
    
    def to_dict(self) -> Dict:
        """
        Convert all staff data to dictionary for serialization.
        
        Returns:
            Dictionary representation of all staff data
        """
        return {
            name: staff.to_dict() for name, staff in self.staff_members.items()
        }
    
    def load_from_dict(self, data: Dict) -> None:
        """
        Load staff data from dictionary.
        
        Args:
            data: Dictionary containing staff data
        """
        self.staff_members = {}
        for name, staff_data in data.items():
            self.staff_members[name] = Staff.from_dict(staff_data)
