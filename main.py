#!/usr/bin/env python3
"""
Main entry point for the Staff Wage and Tip Calculator application.
"""
import tkinter as tk
from views.main_view import MainView
from controllers.data_controller import DataController

def main():
    """Initialize and run the application."""
    root = tk.Tk()
    data_controller = DataController()
    app = MainView(root, data_controller)
    root.mainloop()

if __name__ == "__main__":
    main()
