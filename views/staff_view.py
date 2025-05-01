"""
Staff management view.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Callable, Optional

from controllers.data_controller import DataController
from utils.config import PADDING, BUTTON_WIDTH

class StaffView:
    """View for staff management."""
    
    def __init__(self, parent, data_controller: DataController, on_staff_changed: Optional[Callable] = None):
        """
        Initialize the staff view.
        
        Args:
            parent: Parent widget
            data_controller: DataController instance
            on_staff_changed: Callback function to notify when staff list changes
        """
        self.parent = parent
        self.data_controller = data_controller
        self.staff_controller = data_controller.staff_controller
        self.on_staff_changed = on_staff_changed
        
        self.frame = ttk.Frame(parent, padding=PADDING)
        self.create_widgets()
    
    def create_widgets(self) -> None:
        """Create the widgets for the staff view."""
        # Configure the grid
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            self.frame, 
            text="Staff Management", 
            font=("TkDefaultFont", 14, "bold")
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, PADDING))
        
        # Staff list frame
        staff_frame = ttk.LabelFrame(self.frame, text="Staff List", padding=PADDING)
        staff_frame.grid(row=1, column=0, sticky="nsew")
        
        staff_frame.columnconfigure(0, weight=1)
        staff_frame.rowconfigure(0, weight=1)
        
        # Staff listbox with scrollbar
        self.staff_listbox = tk.Listbox(staff_frame, selectmode=tk.SINGLE)
        self.staff_listbox.grid(row=0, column=0, sticky="nsew")
        
        staff_scrollbar = ttk.Scrollbar(
            staff_frame, 
            orient=tk.VERTICAL, 
            command=self.staff_listbox.yview
        )
        staff_scrollbar.grid(row=0, column=1, sticky="ns")
        self.staff_listbox.config(yscrollcommand=staff_scrollbar.set)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.frame, padding=PADDING)
        buttons_frame.grid(row=2, column=0, sticky="ew")
        
        add_button = ttk.Button(
            buttons_frame, 
            text="Add Staff", 
            command=self.add_staff,
            width=BUTTON_WIDTH
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING))
        
        remove_button = ttk.Button(
            buttons_frame, 
            text="Remove Staff", 
            command=self.remove_staff,
            width=BUTTON_WIDTH
        )
        remove_button.pack(side=tk.LEFT)
        
        # Populate the listbox
        self.refresh()
    
    def refresh(self) -> None:
        """Refresh the staff list."""
        self.staff_listbox.delete(0, tk.END)
        for name in self.staff_controller.get_staff_list():
            self.staff_listbox.insert(tk.END, name)
    
    def add_staff(self) -> None:
        """Add a new staff member."""
        name = simpledialog.askstring("Add Staff", "Enter staff name:")
        if name and name.strip():
            name = name.strip()
            success = self.staff_controller.add_staff(name)
            if success:
                self.refresh()
                self.data_controller.save_data()
                messagebox.showinfo("Success", f"{name} added to staff list")
                
                # Notify that staff list has changed
                if self.on_staff_changed:
                    self.on_staff_changed()
            else:
                messagebox.showwarning("Warning", f"{name} is already in the staff list")
    
    def remove_staff(self) -> None:
        """Remove a staff member."""
        selected = self.staff_listbox.curselection()
        if selected:
            name = self.staff_listbox.get(selected[0])
            confirm = messagebox.askyesno(
                "Confirm", 
                f"Are you sure you want to remove {name}?\n\nThis will delete all their work records."
            )
            if confirm:
                success = self.staff_controller.remove_staff(name)
                if success:
                    self.refresh()
                    self.data_controller.save_data()
                    messagebox.showinfo("Success", f"{name} removed from staff list")
                    
                    # Notify that staff list has changed
                    if self.on_staff_changed:
                        self.on_staff_changed()
        else:
            messagebox.showwarning("Warning", "Please select a staff member to remove")
