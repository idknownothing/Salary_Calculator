"""
Combined Hours and Tips entry view with dual date selection and enlarged working hours section.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar
from tkcalendar import DateEntry, Calendar

from controllers.data_controller import DataController
from controllers.hours_controller import HoursController
from utils.config import PADDING, BUTTON_WIDTH, ENTRY_WIDTH
from utils.time_utils import format_hours

class HoursTipsView:
    """View for combined hours and tips entry."""
    
    def __init__(self, parent, data_controller: DataController):
        """
        Initialize the hours and tips view.
        
        Args:
            parent: Parent widget
            data_controller: DataController instance
        """
        self.parent = parent
        self.data_controller = data_controller
        self.staff_controller = data_controller.staff_controller
        self.tips_controller = data_controller.tips_controller
        self.hours_controller = HoursController(self.staff_controller)
        
        # Current date
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        
        self.frame = ttk.Frame(parent, padding=PADDING)
        self.create_widgets()
    
    def create_widgets(self) -> None:
        """Create the widgets for the hours and tips view."""
        # Configure the grid
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)  # Calendar column fixed width
        self.frame.rowconfigure(3, weight=1)  # Give more weight to the hours frame
        
        # Title
        title_label = ttk.Label(
            self.frame, 
            text="Hours and Tips Entry", 
            font=("TkDefaultFont", 14, "bold")
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, PADDING))
        
        # Date selection (left side)
        date_frame = ttk.Frame(self.frame)
        date_frame.grid(row=1, column=0, sticky="ew", pady=(0, PADDING))
        
        prev_day_btn = ttk.Button(
            date_frame,
            text="◀ Previous Day",
            command=self.previous_day,
            width=BUTTON_WIDTH
        )
        prev_day_btn.pack(side=tk.LEFT, padx=(0, PADDING))
        
        ttk.Label(date_frame, text="Date:").pack(side=tk.LEFT, padx=(0, PADDING))
        
        self.date_picker = DateEntry(
            date_frame, 
            width=12, 
            background='darkblue',
            foreground='white', 
            borderwidth=2, 
            date_pattern='yyyy-mm-dd'
        )
        self.date_picker.pack(side=tk.LEFT, padx=(0, PADDING))
        self.date_picker.set_date(datetime.now())
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_changed)
        
        next_day_btn = ttk.Button(
            date_frame,
            text="Next Day ▶",
            command=self.next_day,
            width=BUTTON_WIDTH
        )
        next_day_btn.pack(side=tk.LEFT)
        
        # Tips entry
        tips_frame = ttk.Frame(self.frame)
        tips_frame.grid(row=2, column=0, sticky="ew", pady=PADDING)
        
        ttk.Label(tips_frame, text=f"Daily Tips:").pack(side=tk.LEFT, padx=(0, PADDING))
        
        self.tips_var = tk.StringVar()
        tips_entry = ttk.Entry(tips_frame, textvariable=self.tips_var, width=ENTRY_WIDTH)
        tips_entry.pack(side=tk.LEFT)
        
        # Calendar frame (right side)
        calendar_frame = ttk.LabelFrame(self.frame, text="Calendar", padding=PADDING)
        calendar_frame.grid(row=0, column=1, rowspan=4, sticky="ne", padx=(PADDING, 0))
        
        # Create calendar widget
        today = datetime.now()
        self.calendar = Calendar(
            calendar_frame,
            selectmode='day',
            year=today.year,
            month=today.month,
            day=today.day,
            showweeknumbers=False,
            firstweekday='sunday',
            background='white',
            foreground='black',
            borderwidth=1,
            selectbackground='#0078d7',
            normalbackground='white',
            weekendbackground='#f0f0f0',
            weekendforeground='black',
            othermonthforeground='gray',
            othermonthbackground='white',
            othermonthweforeground='gray',
            othermonthwebackground='#f0f0f0',
            font=("TkDefaultFont", 9),
            width=300,
            height=200
        )
        self.calendar.pack(fill=tk.BOTH, expand=True)
        
        # Bind date selection
        self.calendar.bind("<<CalendarSelected>>", self.on_calendar_selected)
        
        # Hours entry frame - Make it larger
        self.hours_frame = ttk.LabelFrame(
            self.frame, 
            text=f"Working Hours", 
            padding=PADDING
        )
        self.hours_frame.grid(row=3, column=0, sticky="nsew")
        
        # Create scrollable frame for hours entries with increased height
        self.canvas = tk.Canvas(self.hours_frame)
        self.scrollbar = ttk.Scrollbar(self.hours_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Set minimum height for the canvas to show more staff
        self.canvas.config(height=400)  # Increased height
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Create hours entries
        self.create_hours_entries()
        
        # Load tips for current date
        self.load_tips_for_date()
    
    def create_hours_entries(self) -> None:
        """Create the hours entry widgets for each staff member."""
        # Clear existing entries and references
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Reset our tracking dictionaries
        self.time_vars = {}
        self.entry_widgets = {}
        
        # Create header with a different style to make it stand out
        header_frame = ttk.Frame(self.scrollable_frame, padding=(0, 5))
        header_frame.grid(row=0, column=0, columnspan=5, sticky="ew")
        header_frame.columnconfigure(0, weight=1)
        
        ttk.Label(header_frame, text="Name", width=15, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, padx=5)
        ttk.Label(header_frame, text="Start Time", width=10, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, padx=5)
        ttk.Label(header_frame, text="End Time", width=10, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, padx=5)
        ttk.Label(header_frame, text="OR", width=5, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=3, padx=5)
        ttk.Label(header_frame, text="Total Hours", width=10, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=4, padx=5)
        
        # Add a separator
        separator = ttk.Separator(self.scrollable_frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", pady=5)
        
        # Get the current staff list
        staff_list = self.staff_controller.get_staff_list()
        
        if not staff_list:
            ttk.Label(
                self.scrollable_frame, 
                text="No staff members. Add staff in the Staff Management tab.",
                font=("TkDefaultFont", 10, "italic")
            ).grid(row=2, column=0, columnspan=5, padx=5, pady=20)
            return
        
        # Create entries for each staff member with more spacing
        for i, name in enumerate(staff_list):
            row = i + 2  # +2 because of header and separator
            
            # Create a frame for each staff member to improve spacing
            staff_frame = ttk.Frame(self.scrollable_frame, padding=(0, 3))
            staff_frame.grid(row=row, column=0, columnspan=5, sticky="ew")
            
            # Name label
            ttk.Label(staff_frame, text=name, width=15).grid(row=0, column=0, padx=5)
            
            # Start time entry with hint and auto-colon
            start_var = tk.StringVar()
            start_entry = ttk.Entry(
                staff_frame, 
                textvariable=start_var, 
                width=ENTRY_WIDTH
            )
            start_entry.grid(row=0, column=1, padx=5)
            
            # Add hint for start time
            start_entry.insert(0, "e.g. 0900")
            start_entry.config(foreground="gray")
            
            def on_start_entry_focus_in(event, var=start_var):
                if var.get() == "e.g. 0900":
                    event.widget.delete(0, tk.END)
                    event.widget.config(foreground="black")
            
            def on_start_entry_focus_out(event, var=start_var):
                if not var.get():
                    event.widget.insert(0, "e.g. 0900")
                    event.widget.config(foreground="gray")
                elif var.get() != "e.g. 0900" and ":" not in var.get():
                    # Format time with colon when focus is lost
                    self.format_time_with_colon(var, event.widget)
            
            def on_start_entry_key_release(event, var=start_var):
                # Auto-format time as user types
                if var.get() != "e.g. 0900" and len(var.get()) == 4 and ":" not in var.get() and var.get().isdigit():
                    self.format_time_with_colon(var, event.widget)
            
            start_entry.bind("<FocusIn>", on_start_entry_focus_in)
            start_entry.bind("<FocusOut>", on_start_entry_focus_out)
            start_entry.bind("<KeyRelease>", on_start_entry_key_release)
            
            # End time entry with hint and auto-colon
            end_var = tk.StringVar()
            end_entry = ttk.Entry(
                staff_frame, 
                textvariable=end_var, 
                width=ENTRY_WIDTH
            )
            end_entry.grid(row=0, column=2, padx=5)
            
            # Add hint for end time
            end_entry.insert(0, "e.g. 1700")
            end_entry.config(foreground="gray")
            
            def on_end_entry_focus_in(event, var=end_var):
                if var.get() == "e.g. 1700":
                    event.widget.delete(0, tk.END)
                    event.widget.config(foreground="black")
            
            def on_end_entry_focus_out(event, var=end_var):
                if not var.get():
                    event.widget.insert(0, "e.g. 1700")
                    event.widget.config(foreground="gray")
                elif var.get() != "e.g. 1700" and ":" not in var.get():
                    # Format time with colon when focus is lost
                    self.format_time_with_colon(var, event.widget)
            
            def on_end_entry_key_release(event, var=end_var):
                # Auto-format time as user types
                if var.get() != "e.g. 1700" and len(var.get()) == 4 and ":" not in var.get() and var.get().isdigit():
                    self.format_time_with_colon(var, event.widget)
            
            end_entry.bind("<FocusIn>", on_end_entry_focus_in)
            end_entry.bind("<FocusOut>", on_end_entry_focus_out)
            end_entry.bind("<KeyRelease>", on_end_entry_key_release)
            
            # OR label
            ttk.Label(staff_frame, text="OR", width=5).grid(row=0, column=3, padx=5)
            
            # Total hours entry with hint
            hours_var = tk.StringVar()
            hours_entry = ttk.Entry(
                staff_frame, 
                textvariable=hours_var, 
                width=ENTRY_WIDTH
            )
            hours_entry.grid(row=0, column=4, padx=5)
            
            # Add hint for hours
            hours_entry.insert(0, "e.g. 8.0")
            hours_entry.config(foreground="gray")
            
            def on_hours_entry_focus_in(event, var=hours_var):
                if var.get() == "e.g. 8.0":
                    event.widget.delete(0, tk.END)
                    event.widget.config(foreground="black")
            
            def on_hours_entry_focus_out(event, var=hours_var):
                if not var.get():
                    event.widget.insert(0, "e.g. 8.0")
                    event.widget.config(foreground="gray")
            
            hours_entry.bind("<FocusIn>", on_hours_entry_focus_in)
            hours_entry.bind("<FocusOut>", on_hours_entry_focus_out)
            
            # Store variables and widgets
            self.time_vars[name] = (start_var, end_var, hours_var)
            self.entry_widgets[name] = (start_entry, end_entry, hours_entry)
            
            # Add a light separator between staff members (except after the last one)
            if i < len(staff_list) - 1:
                separator = ttk.Separator(self.scrollable_frame, orient="horizontal")
                separator.grid(row=row+1, column=0, columnspan=5, sticky="ew", pady=2)
            
            # Load existing data for this date if available
            self.load_hours_for_staff(name)


    def format_time_with_colon(self, var: tk.StringVar, widget: ttk.Entry) -> None:
        """
        Format a 4-digit time string by inserting a colon.
        
        Args:
            var: StringVar containing the time
            widget: Entry widget to update
        """
        time_str = var.get().strip()
        
        # Only process if it's a 4-digit string
        if len(time_str) == 4 and time_str.isdigit():
            # Insert colon after the first two digits
            formatted_time = f"{time_str[:2]}:{time_str[2:]}"
            
            # Update the variable and widget
            var.set(formatted_time)
            
            # Maintain cursor position after the colon
            widget.icursor(len(formatted_time))



    def on_date_changed(self, event=None) -> None:
        """
        Handle date change from DateEntry.
        
        Args:
            event: Event object
        """
        # Save current records
        self.save_all_records()
        
        # Get selected date
        date_obj = self.date_picker.get_date()
        self.current_date = date_obj.strftime("%Y-%m-%d")
        
        # Update calendar selection to match DateEntry
        self.calendar.selection_set(date_obj)
        
        # Update hours frame title
        self.hours_frame.config(text=f"Working Hours")
        
        # Clear all entries first
        self.clear_all_entries()
        
        # Reload hours for all staff
        for name in self.staff_controller.get_staff_list():
            self.load_hours_for_staff(name)
        
        # Load tips for the date
        self.load_tips_for_date()
        
        # Check if total hours is zero and clear tips if needed
        self.check_and_clear_tips_if_zero_hours()

    def on_calendar_selected(self, event=None) -> None:
        """
        Handle date selection from calendar.
        
        Args:
            event: Event object
        """
        # Save current records
        self.save_all_records()
        
        # Get selected date
        selected_date = self.calendar.get_date()
        date_obj = datetime.strptime(selected_date, "%m/%d/%y")
        self.current_date = date_obj.strftime("%Y-%m-%d")
        
        # Update DateEntry to match calendar selection
        self.date_picker.set_date(date_obj)
        
        # Update hours frame title
        self.hours_frame.config(text=f"Working Hours")
        
        # Clear all entries first
        self.clear_all_entries()
        
        # Reload hours for all staff
        for name in self.staff_controller.get_staff_list():
            self.load_hours_for_staff(name)
        
        # Load tips for the date
        self.load_tips_for_date()
        
        # Check if total hours is zero and clear tips if needed
        self.check_and_clear_tips_if_zero_hours()

    def check_and_clear_tips_if_zero_hours(self) -> None:
        """Check if total hours is zero and clear tips if needed."""
        # Calculate total hours for the day
        total_hours = 0
        
        for name in self.staff_controller.get_staff_list():
            success, hours_data = self.hours_controller.get_hours_for_date(name, self.current_date)
            if success and hours_data is not None:
                if isinstance(hours_data, dict):  # Time range
                    from utils.time_utils import calculate_hours_from_range
                    if hours_data.get('start') and hours_data.get('end'):
                        hours = calculate_hours_from_range(hours_data['start'], hours_data['end'])
                        total_hours += hours
                else:  # Direct hours
                    total_hours += float(hours_data)
        
        # If total hours is zero, clear tips
        if total_hours <= 0:
            tips = self.tips_controller.get_tips_for_date(self.current_date)
            if tips > 0:
                self.tips_controller.add_tips(self.current_date, 0)
                self.tips_var.set("")
                self.data_controller.save_data()



    def previous_day(self) -> None:
        """Navigate to the previous day after saving current records."""
        # Save current records
        if self.save_all_records():
            # Navigate to previous day
            current = datetime.strptime(self.current_date, "%Y-%m-%d")
            previous = current - timedelta(days=1)
            self.current_date = previous.strftime("%Y-%m-%d")
            
            # Update both date selection widgets
            self.date_picker.set_date(previous)
            self.calendar.selection_set(previous)
            
            # Update hours frame title
            self.hours_frame.config(text=f"Working Hours")
            
            # Clear all entries first
            self.clear_all_entries()
            
            # Reload hours for all staff
            for name in self.staff_controller.get_staff_list():
                self.load_hours_for_staff(name)
            
            # Load tips for the date
            self.load_tips_for_date()
            
            # Check if total hours is zero and clear tips if needed
            self.check_and_clear_tips_if_zero_hours()

    def next_day(self) -> None:
        """Navigate to the next day after saving current records."""
        # Save current records
        if self.save_all_records():
            # Navigate to next day
            current = datetime.strptime(self.current_date, "%Y-%m-%d")
            next_day = current + timedelta(days=1)
            self.current_date = next_day.strftime("%Y-%m-%d")
            
            # Update both date selection widgets
            self.date_picker.set_date(next_day)
            self.calendar.selection_set(next_day)
            
            # Update hours frame title
            self.hours_frame.config(text=f"Working Hours")
            
            # Clear all entries first
            self.clear_all_entries()
            
            # Reload hours for all staff
            for name in self.staff_controller.get_staff_list():
                self.load_hours_for_staff(name)
            
            # Load tips for the date
            self.load_tips_for_date()
            
            # Check if total hours is zero and clear tips if needed
            self.check_and_clear_tips_if_zero_hours()






    def reset_entry_to_hint(self, entry_widget, hint_text, var):
        """
        Reset an entry widget to show its hint text.
        
        Args:
            entry_widget: The entry widget to reset
            hint_text: The hint text to display
            var: The StringVar associated with the entry
        """
        var.set(hint_text)
        entry_widget.config(foreground="gray")
    

    def load_hours_for_staff(self, name: str) -> None:
        """
        Load existing hours data for a staff member.
        
        Args:
            name: Staff member name
        """
        if name not in self.time_vars or name not in self.entry_widgets:
            return
            
        start_var, end_var, hours_var = self.time_vars[name]
        start_entry, end_entry, hours_entry = self.entry_widgets[name]
        
        # Reset all entries to hint state first
        self.reset_entry_to_hint(start_entry, "e.g. 0900", start_var)
        self.reset_entry_to_hint(end_entry, "e.g. 1700", end_var)
        self.reset_entry_to_hint(hours_entry, "e.g. 8.0", hours_var)
        
        success, hours_data = self.hours_controller.get_hours_for_date(name, self.current_date)
        if success and hours_data is not None:
            if isinstance(hours_data, dict):  # Time range
                # Set actual values and change color
                start_var.set(hours_data.get('start', ''))
                end_var.set(hours_data.get('end', ''))
                start_entry.config(foreground="black")
                end_entry.config(foreground="black")
                
                # Calculate hours from start/end if available
                from utils.time_utils import calculate_hours_from_range
                if hours_data.get('start') and hours_data.get('end'):
                    hours = calculate_hours_from_range(hours_data['start'], hours_data['end'])
                    hours_var.set(f"{hours:.2f}")
                    hours_entry.config(foreground="black")
            else:  # Direct hours
                # Set actual value and change color (including zero)
                hours_var.set(f"{float(hours_data):.2f}")
                hours_entry.config(foreground="black")

  
    def load_tips_for_date(self) -> None:
        """Load tips for the current date."""
        tips = self.tips_controller.get_tips_for_date(self.current_date)
        if tips > 0:
            self.tips_var.set(f"{tips:.2f}")
        else:
            self.tips_var.set("")
    
    def clear_all_entries(self) -> None:
        """Reset all entry fields to their hint state."""
        for name, (start_entry, end_entry, hours_entry) in self.entry_widgets.items():
            start_var, end_var, hours_var = self.time_vars[name]
            
            self.reset_entry_to_hint(start_entry, "e.g. 0900", start_var)
            self.reset_entry_to_hint(end_entry, "e.g. 1700", end_var)
            self.reset_entry_to_hint(hours_entry, "e.g. 8.0", hours_var)
    

    def save_all_records(self) -> bool:
        """
        Save all staff records and tips for the current date.
        If total hours is zero, clear tips as well.
        
        Returns:
            True if saved successfully, False if there were errors
        """
        # First, calculate total hours for the day
        total_hours = 0
        staff_with_hours = 0
        
        for name, (start_var, end_var, hours_var) in self.time_vars.items():
            start = start_var.get().strip()
            end = end_var.get().strip()
            hours = hours_var.get().strip()
            
            # Skip hint text
            if start == "e.g. 0900":
                start = ""
            if end == "e.g. 1700":
                end = ""
            if hours == "e.g. 8.0":
                hours = ""
            
            # Calculate hours from time range or direct hours
            if hours:
                try:
                    hours_float = float(hours)
                    total_hours += hours_float
                    if hours_float > 0:
                        staff_with_hours += 1
                except ValueError:
                    pass
            elif start and end:
                try:
                    from utils.time_utils import calculate_hours_from_range
                    hours_float = calculate_hours_from_range(start, end)
                    total_hours += hours_float
                    if hours_float > 0:
                        staff_with_hours += 1
                except Exception:
                    pass
        
        # If total hours is zero, clear tips
        if total_hours <= 0:
            self.tips_controller.add_tips(self.current_date, 0)
            self.tips_var.set("")
        
        # Save tips if there are working hours
        tips_str = self.tips_var.get().strip()
        if tips_str and tips_str != "0.0" and tips_str != "0":
            try:
                tips_float = float(tips_str)
                if tips_float >= 0:
                    self.tips_controller.add_tips(self.current_date, tips_float)
                else:
                    messagebox.showerror("Error", "Tips amount cannot be negative")
                    return False
            except ValueError:
                messagebox.showerror("Error", "Tips must be a number")
                return False
        else:
            # If empty or zero, set tips to 0
            self.tips_controller.add_tips(self.current_date, 0)
        
        # Save hours for each staff member
        success_count = 0
        error_messages = []
        
        for name, (start_var, end_var, hours_var) in self.time_vars.items():
            start = start_var.get().strip()
            end = end_var.get().strip()
            hours = hours_var.get().strip()
            
            # Skip hint text
            if start == "e.g. 0900":
                start = ""
            if end == "e.g. 1700":
                end = ""
            if hours == "e.g. 8.0":
                hours = ""
            
            # If all fields are empty, skip this staff member
            if not start and not end and not hours:
                continue
            
            if hours:
                try:
                    hours_float = float(hours)
                    # Allow zero hours to be saved (to correct mistakes)
                    success, message = self.hours_controller.add_hours(name, self.current_date, hours_float)
                    if success:
                        success_count += 1
                    else:
                        error_messages.append(f"{name}: {message}")
                except ValueError:
                    error_messages.append(f"{name}: Total hours must be a number")
            elif start and end:
                success, message = self.hours_controller.add_time_range(name, self.current_date, start, end)
                if success:
                    success_count += 1
                else:
                    error_messages.append(f"{name}: {message}")
        
        # Save data
        self.data_controller.save_data()
        
        # Show results
        if error_messages:
            messagebox.showerror("Errors", "\n".join(error_messages))
            return False
        
        return True


  
    def refresh(self) -> None:
        """Refresh the hours and tips view completely."""
        # Recreate the hours entries from scratch
        self.create_hours_entries()
        
        # Load tips for the date
        self.load_tips_for_date()
        
        # Update the hours frame title
        self.hours_frame.config(text=f"Working Hours")
        
        # Make sure the date pickers are in sync
        try:
            date_obj = datetime.strptime(self.current_date, "%Y-%m-%d")
            self.date_picker.set_date(date_obj)
            self.calendar.selection_set(date_obj)
        except ValueError:
            # If there's an issue with the date, reset to today
            today = datetime.now()
            self.current_date = today.strftime("%Y-%m-%d")
            self.date_picker.set_date(today)
            self.calendar.selection_set(today)
