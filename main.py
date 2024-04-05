# -*- coding: utf-8 -*-
"""
A graphical user interface (GUI) application for creating, editing, and simulating flowcharts.

The application allows users to:
- Create and edit tasks with customizable names, activities, and cycle counts
- Connect tasks using connectors and OR connections
- Simulate the execution of the flowchart with adjustable speed
- Save and load flowcharts from XLSX files
- Clear the canvas and delete selected tasks

The main class `App` sets up the GUI window, menus, sidebars, and canvas using the Tkinter and customtkinter libraries.
The `DraggableTask` class represents a task in the flowchart, which can be dragged and edited on the canvas.
The `TaskConnector` class represents a connection between tasks in the flowchart.
The `Configuration` class holds general variables and objects used throughout the application.

Additional features include:
- Editing task properties in the sidebar
- Adding mutexes and OR connections between tasks
- Controlling the simulation speed with a slider
- Showing/hiding the simulation sidebar

This module provides a comprehensive GUI for creating, editing, and simulating flowcharts with various features
for task management, connections, mutexes, and simulation control.
"""

# Import necessary modules
from tkinter import *
import customtkinter
from General.FileOperations import load_files, save_file
from Objects.DraggableTask import DraggableTask
from CTkMenuBar import *
from General.Configuration import Configuration

# Import available mutex types
from Objects.Mutex.MutexPriorityInversion import MutexPriorityInversion
from Objects.Mutex.MutexPriorityCeiling import MutexPriorityCeiling
from Objects.Mutex.MutexTicketLock import MutexTicketLock
from Objects.Mutex.MutexFirstComeFirstServe import MutexFirstComeFirstServe


class App(customtkinter.CTk):
    """Main application class."""
    sidebar = None
    show_sim_sidebar = False

    def __init__(self):
        super().__init__()

        Configuration.root = self

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")
        self.geometry("800x800")

        # Configure window
        self.title("Flowchart Editor")

        # Load custom fonts
        from tkextrafont import Font
        Configuration.font_black = Font(file="fonts/Montserrat-Black.ttf", family="Montserrat")
        Configuration.font_light_normal = Font(file="fonts/Montserrat-Light.ttf", family="Montserrat")

        # Create a canvas object
        canvas = Canvas(self, bd=0, highlightthickness=0, background=self['bg'])
        canvas.pack(fill=BOTH, expand=True)
        Configuration.canvas = canvas

        # Create menu bar
        menubar = CTkTitleMenu(master=self)
        button_file_menu = menubar.add_cascade("File")
        button_edit_menu = menubar.add_cascade("Edit")
        button_run_menu = menubar.add_cascade("Run")
        button_mutex_menu = menubar.add_cascade("Mutex")

        # Create file menu
        filemenu = CustomDropdownMenu(widget=button_file_menu, border_color="")
        filemenu.add_option(option="Save as xslx", command=lambda: save_file())
        filemenu.add_option(option="Load from xslx", command=lambda: load_files(show_file_dialog=True) or Configuration.stop_simulation())
        filemenu.add_option(option="Reload file", command=lambda: load_files(show_file_dialog=False) or Configuration.stop_simulation())
        filemenu.add_separator()
        filemenu.add_option(option="Clear chart", command=lambda: Configuration.clear_canvas() or Configuration.stop_simulation())
        filemenu.add_option(option="Exit to desktop", command=self.quit)

        # Create edit menu
        editmenu = CustomDropdownMenu(widget=button_edit_menu, border_color="")
        editmenu.add_option(option="Edit mode", command=lambda: DraggableTask.switch_selection())
        editmenu.add_option(option="Add new task", command=lambda: Configuration.add_task())
        editmenu.add_option(option="Delete selected task", command=lambda: Configuration.delete_selection())

        # Create run menu
        runmenu = CustomDropdownMenu(widget=button_run_menu, border_color="")
        runmenu.add_option(option="Next step", command=Configuration.step)
        runmenu.add_option(option="Hide/Show Simulation Sidebar", command=Configuration.toggle_simulation_sidebar)

        # Create mutex selection menu
        mutexmenu = CustomDropdownMenu(widget=button_mutex_menu, border_color="")
        for available_mutex_type_name in Configuration.available_mutex_types:
            mutexmenu.add_option(option="Load using " + available_mutex_type_name, command=lambda: Configuration.set_mutex_type(available_mutex_type_name))

        # Create sidebars
        Configuration.create_sidebar()


if __name__ == "__main__":
    app = App()
    app.mainloop()
