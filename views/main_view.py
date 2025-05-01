"""
Main application window.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from controllers.data_controller import DataController
from views.staff_view import StaffView
from views.hours_tips_view import HoursTipsView
from views.summary_view import SummaryView
from utils.config import APP_TITLE, APP_WIDTH, APP_HEIGHT, PADDING

class MainView:
    """Main application window."""
    
    def __init__(self, root: tk.Tk, data_controller: DataController):
        """
        Initialize the main view.
        
        Args:
            root: Tkinter root window
            data_controller: DataController instance
        """
        self.root = root
        self.data_controller = data_controller
        
        self.setup_window()
        self.create_menu()
        self.create_notebook()
        self.create_status_bar()
        
        # Set up auto-save
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_window(self) -> None:
        """Set up the main window."""
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(800, 600)
        
        # Configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def create_menu(self) -> None:
        """Create the application menu."""
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Save Monthly Data", command=self.save_monthly_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Monthly Summary", command=self.show_monthly_summary)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        
        self.root.config(menu=self.menu_bar)
    
    def create_notebook(self) -> None:
        """Create the main notebook with tabs."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
        
        # Create tabs
        self.hours_tips_view = HoursTipsView(self.notebook, self.data_controller)
        self.staff_view = StaffView(self.notebook, self.data_controller, self.on_staff_changed)
        self.summary_view = SummaryView(self.notebook, self.data_controller)
        
        # Add tabs to notebook
        self.notebook.add(self.staff_view.frame, text="Staff Management")
        self.notebook.add(self.hours_tips_view.frame, text="Hours & Tips Entry")
        self.notebook.add(self.summary_view.frame, text="Monthly Summary")
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def on_staff_changed(self) -> None:
        """Handle staff list changes."""
        # Refresh the hours and tips view
        self.hours_tips_view.refresh()
        
        # Also refresh the summary view
        self.summary_view.refresh()
    
    def create_status_bar(self) -> None:
        """Create the status bar."""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")
    
    def on_tab_changed(self, event=None) -> None:
        """
        Handle tab change event.
        
        Args:
            event: Event object
        """
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text")
        
        # Refresh the current tab
        if tab_name == "Staff Management":
            self.staff_view.refresh()
        elif tab_name == "Hours & Tips Entry":
            self.hours_tips_view.refresh()
        elif tab_name == "Monthly Summary":
            self.summary_view.refresh()
    
    def save_data(self) -> None:
        """Save current data."""
        self.data_controller.save_data()
        self.status_var.set(f"Data saved at {datetime.now().strftime('%H:%M:%S')}")
    
    def save_monthly_data(self) -> None:
        """Save monthly data."""
        now = datetime.now()
        year = now.year
        month = now.month
        
        success = self.data_controller.save_monthly_data(year, month)
        if success:
            self.status_var.set(f"Monthly data saved for {year}-{month:02d}")
        else:
            self.status_var.set("Error saving monthly data")
    
    def show_monthly_summary(self) -> None:
        """Show monthly summary."""
        self.notebook.select(2)  # Select the Monthly Summary tab
        self.summary_view.refresh()
    
    def on_close(self) -> None:
        """Handle window close event."""
        self.save_data()
        self.root.destroy()
