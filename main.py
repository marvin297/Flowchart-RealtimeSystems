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
from Objects.FileOperations import load_files, save_file
from Objects.DraggableTask import DraggableTask
from CTkMenuBar import *
from General.Configuration import Configuration
from Objects.TaskConnector import TaskConnector


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
        filemenu.add_option(option="Load from xslx", command=lambda: load_files(show_file_dialog=True) or self.stop_simulation())
        filemenu.add_option(option="Reload file", command=lambda: load_files(show_file_dialog=False) or self.stop_simulation())
        filemenu.add_separator()
        filemenu.add_option(option="Clear chart", command=lambda: App.clear_canvas())
        filemenu.add_option(option="Exit to desktop", command=self.quit)

        # Create edit menu
        editmenu = CustomDropdownMenu(widget=button_edit_menu, border_color="")
        editmenu.add_option(option="Edit mode", command=lambda: DraggableTask.switch_selection())
        editmenu.add_option(option="Add new task", command=lambda: App.add_task())
        editmenu.add_option(option="Delete selected task", command=lambda: Configuration.delete_selection())

        # Create run menu
        runmenu = CustomDropdownMenu(widget=button_run_menu, border_color="")
        runmenu.add_option(option="Next step", command=App.step)
        runmenu.add_option(option="Hide/Show Simulation Sidebar", command=self.toggle_simulation_sidebar)

        # Create mutex selection menu
        mutexmenu = CustomDropdownMenu(widget=button_mutex_menu, border_color="")
        for available_mutex_type_name in Configuration.available_mutex_types:
            mutexmenu.add_option(option="Load using " + available_mutex_type_name, command=lambda: Configuration.set_mutex_type(available_mutex_type_name))

        # Create sidebars
        self.create_sidebar()

    def toggle_simulation_sidebar(self):
        """Toggle visibility of the simulation sidebar."""
        if Configuration.edit_mode:
            return

        Configuration.show_simulation_container = not Configuration.show_simulation_container
        Configuration.toggle_sidebar(Configuration.show_simulation_container)
        Configuration._update_sidebar()

    def update_simulation_speed(self, value):
        """Update the simulation speed based on the slider value."""
        # Convert slider value to a delay (in milliseconds)
        Configuration.current_delay = int(3000 + 1 - value)
        print(f"Speed set to {value}, delay {Configuration.current_delay} ms")
        self.update_speed_value()

    def start_simulation(self):
        """Start the simulation."""
        if not Configuration.auto_run:
            self.update_simulation_speed(value=1)
            Configuration.auto_run = True
            self.run_periodically()

    def stop_simulation(self):
        """Stop the simulation."""
        Configuration.auto_run = False

    def run_periodically(self):
        """Run the simulation periodically based on the current delay."""
        if Configuration.auto_run:
            self.step()
            # Schedule the next call
            self.after(Configuration.current_delay, self.run_periodically)

    def create_run_container(self):
        """Create the simulation sidebar."""
        Configuration.sidebar_simulation = Frame(Configuration.sidebar, bd=0, bg="#303030")

        sidebar_title = Label(Configuration.sidebar_simulation, text="Simulation", font=("Montserrat Light", 20), bg="#2A2A2A", fg="white", width=15)
        sidebar_title.pack(side=TOP, anchor=N, padx=0, pady=10)

        sim_start_button = customtkinter.CTkButton(Configuration.sidebar_simulation, text="Start", command=self.start_simulation)
        sim_start_button.pack(pady=10, padx=10)

        sim_end_button = customtkinter.CTkButton(Configuration.sidebar_simulation, text="Stop", command=self.stop_simulation)
        sim_end_button.pack(pady=10, padx=10)

        speed_slider = customtkinter.CTkSlider(Configuration.sidebar_simulation, from_=1, to=3000, number_of_steps=3000)
        speed_slider.pack(side=customtkinter.TOP, fill=customtkinter.X, padx=10, pady=10)
        speed_slider.set(1000)  # Set default speed value
        speed_slider.configure(command=self.update_simulation_speed)

        self.dynamic_value_label = customtkinter.CTkLabel(Configuration.sidebar_simulation, text="Period per Cycle: 1000ms", bg_color=self['bg'], fg_color="#303030")
        self.dynamic_value_label.pack(pady=10)

    def update_speed_value(self):
        """Update the displayed speed value."""
        self.dynamic_value_label.configure(text=f"Period per Cycle: {Configuration.current_delay}ms")

    def create_sidebar(self):
        """Create the main sidebar."""
        Configuration.sidebar = Frame(self, width=300, bd=0, bg="#303030")
        Configuration.sidebar.place(relx=0, rely=0, relheight=1, x=-300)

        Configuration.sidebar_task_input = StringVar()
        Configuration.sidebar_activity_input = StringVar()
        Configuration.sidebar_cycles_input = IntVar()

        sidebar_title = Label(Configuration.sidebar, text="Editor", font=("Montserrat Light", 20), bg="#2A2A2A", fg="white",
                              width=15)
        sidebar_title.pack(side=TOP, anchor=N, padx=0, pady=10)
        App.create_edit_task_container()
        App.create_connection_container()
        App.create_mutex_container()
        App.create_or_connection_container()
        self.create_run_container()

    @staticmethod
    def create_edit_task_container():
        """Create the edit task container in the sidebar."""
        Configuration.sidebar_edit_task_container = Frame(Configuration.sidebar, bd=0, bg="#303030")

        task_name_frame = Frame(Configuration.sidebar_edit_task_container, bd=0, bg="#2A2A2A", height=30)
        task_name_frame.place(relx=0, rely=0, x=15, y=100)
        task_name_title = Label(task_name_frame, text="Task name", font=("Montserrat Light", 10), bg="#2A2A2A",
                                fg="white", width=15)
        task_name_title.pack(side=TOP, anchor=N, padx=0, pady=5)
        task_name_input = Entry(task_name_frame, font=("Montserrat Light", 10), bd=0, bg="#303030", fg="white",
                                insertbackground="white", width=20, textvariable=Configuration.sidebar_task_input,
                                borderwidth=10, relief="flat")
        task_name_input.pack(side=TOP, anchor=N, padx=15, pady=15)

        activity_name_frame = Frame(Configuration.sidebar_edit_task_container, bd=0, bg="#2A2A2A", height=30)
        activity_name_frame.place(relx=0, rely=0, x=15, y=210)
        activity_name_title = Label(activity_name_frame, text="Activity name", font=("Montserrat Light", 10),
                                    bg="#2A2A2A",
                                    fg="white", width=15)
        activity_name_title.pack(side=TOP, anchor=N, padx=0, pady=5)
        activity_name_input = Entry(activity_name_frame, font=("Montserrat Light", 10), bd=0, bg="#303030", fg="white",
                                    insertbackground="white", width=20,
                                    textvariable=Configuration.sidebar_activity_input, borderwidth=10, relief="flat")
        activity_name_input.pack(side=TOP, anchor=N, padx=15, pady=15)

        cycles_frame = Frame(Configuration.sidebar_edit_task_container, bd=0, bg="#2A2A2A", height=30)
        cycles_frame.place(relx=0, rely=0, x=15, y=320)
        cycles_title = Label(cycles_frame, text="Amount of cycles", font=("Montserrat Light", 10),
                             bg="#2A2A2A",
                             fg="white", width=15)
        cycles_title.pack(side=TOP, anchor=N, padx=0, pady=5)
        cycles_input = Entry(cycles_frame, font=("Montserrat Light", 10), bd=0, bg="#303030", fg="white",
                             insertbackground="white", width=20, textvariable=Configuration.sidebar_cycles_input,
                             borderwidth=10,
                             relief="flat")
        cycles_input.pack(side=TOP, anchor=N, padx=15, pady=15)

        # Create a frame to simulate the button appearance
        button_confirm_task_frame = Frame(Configuration.sidebar_edit_task_container, bg="#303030", bd=1, relief="solid",
                                          highlightbackground=Configuration.task_color,
                                          highlightthickness=1)
        button_confirm_task_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_confirm_task_frame, text="CONFIRM SETTINGS", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: Configuration.confirm_task_change(),
                              width=20)
        button_label.pack()

    @staticmethod
    def create_connection_container():
        """Create the connection container in the sidebar."""
        Configuration.sidebar_add_connection_container = Frame(Configuration.sidebar, bd=0, bg="#303030")

        # Create a frame to simulate the button appearance
        button_add_mutex_frame = Frame(Configuration.sidebar_add_connection_container, bg="#303030", bd=1,
                                       relief="solid",
                                       highlightbackground=Configuration.task_color,
                                       highlightthickness=1)
        button_add_mutex_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_add_mutex_frame, text="ADD MUTEX", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: print("NOT YET IMPLEMENTED"),
                              width=20)
        button_label.pack()


        # Create a frame to simulate the button appearance
        button_add_connection_frame = Frame(Configuration.sidebar_add_connection_container, bg="#303030", bd=1, relief="solid",
                                            highlightbackground=Configuration.task_color,
                                            highlightthickness=1)
        button_add_connection_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_add_connection_frame, text="ADD CONNECTION", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: App.add_connection(),
                              width=20)
        button_label.pack()

    @staticmethod
    def create_mutex_container():
        """Create the mutex container in the sidebar."""
        Configuration.sidebar_add_mutex_container = Frame(Configuration.sidebar, bd=0, bg="#303030")

        # Create a frame to simulate the button appearance
        button_add_mutex_frame = Frame(Configuration.sidebar_add_mutex_container, bg="#303030", bd=1,
                                       relief="solid",
                                       highlightbackground=Configuration.task_color,
                                       highlightthickness=1)
        button_add_mutex_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_add_mutex_frame, text="ADD MUTEX", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: print("NOT YET IMPLEMENTED"),
                              width=20)
        button_label.pack()

    @staticmethod
    def create_or_connection_container():
        """Create the OR connection container in the sidebar."""
        Configuration.sidebar_add_or_connection_container = Frame(Configuration.sidebar, bd=0, bg="#303030")

        # Create a frame to simulate the button appearance
        button_add_or_connection_frame = Frame(Configuration.sidebar_add_or_connection_container, bg="#303030", bd=1,
                                               relief="solid",
                                               highlightbackground=Configuration.task_color,
                                               highlightthickness=1)
        button_add_or_connection_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_add_or_connection_frame, text="ADD OR CONNECTION", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: App.add_or_connection(),
                              width=20)
        button_label.pack()

    @staticmethod
    def clear_canvas():
        """Clear the canvas and reset general variables."""
        Configuration.clear_general_variables()
        Configuration.canvas.delete("all")

    @staticmethod
    def step():
        """Perform a single step in the simulation."""
        print("Step")
        Configuration.step_number += 1
        for task in Configuration.task_objects:
            task.try_step()

        for mutex in Configuration.mutex_objects:
            Configuration.mutex_objects[mutex].evaluate()
            Configuration.mutex_objects[mutex].update_visuals()

    @staticmethod
    def add_task():
        """Add a new task to the canvas."""
        print("Add task")
        new_task = DraggableTask("?", "?", Configuration.root.winfo_width() / 2, Configuration.root.winfo_height() / 2, 50, 1, 0)
        Configuration.task_objects.append(new_task)

    @staticmethod
    def add_or_connection():
        """Add an OR connection to the canvas."""
        sel_task = [task_object for task_object, position in Configuration.selected_tasks.items() if str(position) == str(1)][0]

        Configuration.selected_connection.add_or_connection(sel_task)
        sel_task.add_connector(Configuration.selected_connection, "or")
        sel_task.update_connections()

        Configuration.connector_objects.append([sel_task.task_name + sel_task.activity_name,
                                                Configuration.selected_connection.name,
                                                "",
                                                0])

    @staticmethod
    def add_connection():
        """Add a new connection to the canvas."""
        print("Add connection")
        origin_task = [task_object for task_object, position in Configuration.selected_tasks.items() if str(position) == str(1)][0]
        target_task = [task_object for task_object, position in Configuration.selected_tasks.items() if str(position) == str(2)][0]

        activity_connection = False
        if origin_task.task_name == target_task.task_name:
            activity_connection = True

        new_offset = 0
        for connection in origin_task.connectors:
            if connection in target_task.connectors:
                connection.offset = 50
                new_offset = -50

        new_connection = TaskConnector("?", 0, activity_connection, new_offset)
        origin_task.add_connector(new_connection, "start")
        target_task.add_connector(new_connection, "end")

        origin_task.update_connections()
        target_task.update_connections()

        start_task_name = origin_task.task_name + origin_task.activity_name
        connector_name = new_connection.name
        end_task_name = target_task.task_name + target_task.activity_name
        initial_value = 0

        Configuration.connector_objects.append([start_task_name, connector_name, end_task_name, initial_value])


if __name__ == "__main__":
    app = App()
    app.mainloop()
