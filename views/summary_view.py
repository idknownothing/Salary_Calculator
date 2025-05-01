"""
Summary display view with larger text.
"""
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import calendar

from controllers.data_controller import DataController
from utils.config import PADDING, BUTTON_WIDTH
from utils.time_utils import format_hours, get_month_name

class SummaryView:
    """View for summary display."""
    
    def __init__(self, parent, data_controller: DataController):
        """
        Initialize the summary view.
        
        Args:
            parent: Parent widget
            data_controller: DataController instance
        """
        self.parent = parent
        self.data_controller = data_controller
        self.tips_controller = data_controller.tips_controller
        
        # Current month and year
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        
        # Define font sizes
        self.title_font = ("TkDefaultFont", 14, "bold")
        self.header_font = ("TkDefaultFont", 12, "bold")
        self.text_font = ("TkDefaultFont", 11)  # Larger text font
        self.bold_text_font = ("TkDefaultFont", 11, "bold")
        
        self.frame = ttk.Frame(parent, padding=PADDING)
        self.create_widgets()
    
    def create_widgets(self) -> None:
        """Create the widgets for the summary view."""
        # Configure the grid
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            self.frame, 
            text="Monthly Summary", 
            font=self.title_font
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, PADDING))
        
        # Month selection
        month_frame = ttk.Frame(self.frame)
        month_frame.grid(row=1, column=0, sticky="ew", pady=(0, PADDING))
        
        ttk.Label(month_frame, text="Year:", font=self.text_font).pack(side=tk.LEFT, padx=(0, PADDING))
        
        self.year_var = tk.StringVar(value=str(self.current_year))
        year_spinbox = ttk.Spinbox(
            month_frame, 
            from_=2000, 
            to=2100, 
            textvariable=self.year_var, 
            width=6,
            font=self.text_font
        )
        year_spinbox.pack(side=tk.LEFT, padx=(0, PADDING))
        
        ttk.Label(month_frame, text="Month:", font=self.text_font).pack(side=tk.LEFT, padx=(0, PADDING))
        
        self.month_var = tk.StringVar(value=str(self.current_month))
        month_spinbox = ttk.Spinbox(
            month_frame, 
            from_=1, 
            to=12, 
            textvariable=self.month_var, 
            width=4,
            font=self.text_font
        )
        month_spinbox.pack(side=tk.LEFT, padx=(0, PADDING))
        
        # Month name label
        self.month_name_var = tk.StringVar()
        self.update_month_name()
        month_name_label = ttk.Label(
            month_frame, 
            textvariable=self.month_name_var,
            font=self.bold_text_font
        )
        month_name_label.pack(side=tk.LEFT, padx=(PADDING, 0))
        
        # Refresh button
        refresh_button = ttk.Button(
            month_frame, 
            text="Refresh Summary", 
            command=self.show_monthly_summary,
            width=BUTTON_WIDTH
        )
        refresh_button.pack(side=tk.LEFT, padx=(PADDING, 0))
        
        # Save button
        save_button = ttk.Button(
            month_frame, 
            text="Save Monthly Data", 
            command=self.save_monthly_data,
            width=BUTTON_WIDTH
        )
        save_button.pack(side=tk.RIGHT)
        
        # Summary frame - Remove font option from LabelFrame
        self.summary_frame = ttk.LabelFrame(
            self.frame, 
            text=f"Summary for {get_month_name(self.current_month)} {self.current_year}", 
            padding=PADDING
        )
        self.summary_frame.grid(row=2, column=0, sticky="nsew")
        
        # Create summary text widget with larger font
        self.summary_text = tk.Text(
            self.summary_frame, 
            wrap=tk.WORD, 
            height=20,
            font=self.text_font  # Use larger font
        )
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        summary_scrollbar = ttk.Scrollbar(
            self.summary_frame,
            orient=tk.VERTICAL,
            command=self.summary_text.yview
        )
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.config(yscrollcommand=summary_scrollbar.set)
        
        # Show initial summary
        self.show_monthly_summary()
    
    def update_month_name(self) -> None:
        """Update the month name label."""
        try:
            month = int(self.month_var.get())
            if 1 <= month <= 12:
                self.month_name_var.set(get_month_name(month))
        except ValueError:
            self.month_name_var.set("")
    
    def on_month_changed(self) -> None:
        """Handle month change event."""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            if 2000 <= year <= 2100 and 1 <= month <= 12:
                self.current_year = year
                self.current_month = month
                self.update_month_name()
                self.summary_frame.config(text=f"Summary for {get_month_name(month)} {year}")
                self.show_monthly_summary()
        except ValueError:
            pass
    
    def show_monthly_summary(self) -> None:
        """Show the monthly summary."""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            # Update current values
            self.current_year = year
            self.current_month = month
            self.update_month_name()
            self.summary_frame.config(text=f"Summary for {get_month_name(month)} {year}")
        except ValueError:
            messagebox.showerror("Error", "Invalid year or month")
            return
        
        # Get monthly summary
        summary = self.tips_controller.get_monthly_summary(year, month)
        
        # Display the summary
        self.summary_text.config(state=tk.NORMAL)  # Make text editable
        self.summary_text.delete(1.0, tk.END)
        
        # Header
        self.summary_text.insert(tk.END, f"Monthly Summary for {get_month_name(month)} {year}\n", "header")
        self.summary_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Overall statistics
        self.summary_text.insert(tk.END, "Overall Statistics:\n", "section")
        self.summary_text.insert(tk.END, "-" * 50 + "\n")
        self.summary_text.insert(tk.END, f"Total Tips: ${summary['total_tips']:.2f}\n")
        self.summary_text.insert(tk.END, f"Total Hours: {format_hours(summary['total_hours'])}\n")
        
        if summary['total_hours'] > 0:
            self.summary_text.insert(tk.END, f"Average Tip per Hour: ${summary['avg_tip_per_hour']:.2f}\n\n")
        else:
            self.summary_text.insert(tk.END, f"Average Tip per Hour: $0.00\n\n")
        
        # Staff breakdown
        self.summary_text.insert(tk.END, "Staff Breakdown:\n", "section")
        self.summary_text.insert(tk.END, "-" * 50 + "\n")
        
        if summary['staff_data']:
            self.summary_text.insert(tk.END, f"{'Name':<13} {'Hours':<12} {'Tips':<12} {'Percentage':<15}\n", "table_header")
            self.summary_text.insert(tk.END, "-" * 50 + "\n")
            
            for name, data in sorted(summary['staff_data'].items()):
                hours = data['hours']
                percentage = data['percentage']
                tips = data['tips']
                
                self.summary_text.insert(
                    tk.END, 
                    f"{name:<15} {format_hours(hours):<12} ${tips:.2f}{' ':<12}  {percentage:.2f}%\n"
                )
        else:
            self.summary_text.insert(tk.END, "No staff data available for this month.\n")
        
        # Configure text tags for styling
        self.summary_text.tag_configure("header", font=("TkDefaultFont", 14, "bold"))
        self.summary_text.tag_configure("section", font=("TkDefaultFont", 12, "bold"))
        self.summary_text.tag_configure("table_header", font=("TkDefaultFont", 11, "bold"))
        
        # Make the text read-only
        self.summary_text.config(state=tk.DISABLED)
    
    def save_monthly_data(self) -> None:
        """Save the monthly data to a file."""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid year or month")
            return
        
        success = self.data_controller.save_monthly_data(year, month)
        if success:
            messagebox.showinfo(
                "Success", 
                f"Monthly data for {get_month_name(month)} {year} saved successfully"
            )
        else:
            messagebox.showerror(
                "Error", 
                f"Failed to save monthly data for {get_month_name(month)} {year}"
            )
    
    def refresh(self) -> None:
        """Refresh the summary view."""
        self.show_monthly_summary()
