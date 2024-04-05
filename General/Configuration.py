"""
This module defines the Configuration class, which manages the configuration
settings and state of the application. It includes methods for handling task
selection, updating the sidebar, and deleting selected tasks.
"""
from tkinter import *
import customtkinter


class Configuration:
    """
    A class to manage the configuration settings and state of the application.
    """

    # Class variables to store task, connector, and mutex objects
    task_objects = []
    connector_objects = []
    mutex_objects = {}

    # Variable to keep track of the current step number
    step_number = 0

    # Variables to store references to the canvas and root window
    canvas = None
    root = None

    # Variables to store references to sidebar elements
    sidebar = None
    sidebar_edit_task_container = None
    sidebar_add_connection_container = None
    sidebar_add_mutex_container = None
    sidebar_add_or_connection_container = None
    sidebar_task_input = None
    sidebar_activity_input = None
    sidebar_cycles_input = None
    sidebar_simulation = None

    # Variable to store reference to the simulation sidebar
    simulation_sidebar = None
    dynamic_value_label = None

    # Dictionaries to store selected tasks and connection
    selected_tasks = {}
    selected_connection = None

    # Variable to indicate edit mode
    edit_mode = False

    # Variables to store font styles
    font_black = None
    font_light = None

    # Variables to store arrow colors
    arrow_color = "#767676"
    arrow_color_selected = "#464646"
    activity_arrow_color = "#029cff"
    activity_arrow_color_selected = "#0065a6"
    mutex_color = "#464646"

    # Variables to store task colors
    task_color = "#029cff"
    task_color_selected = "#00335c"
    task_color_running = "red"

    # Variable to store the last import file path
    last_import_file_path = ""

    # Variables to store the available mutex types
    available_mutex_types = ['Priority Ceiling', 'Priority Inversion', 'Ticket Lock', 'First Come First Serve']
    selected_mutex_type = 'First Come First Serve'

    # Variables to store auto run settings
    current_delay = 1000
    auto_run = False
    show_simulation_container = False


class SystemFunctions:
    @staticmethod
    def set_mutex_type(new_type_name):
        Configuration.selected_mutex_type = new_type_name

    @staticmethod
    def clear_general_variables():
        """
        Clear the general variables, including task objects, connector objects,
        mutex objects, step number, selected tasks, and selected connection.
        """
        Configuration.task_objects.clear()
        Configuration.connector_objects.clear()
        Configuration.mutex_objects.clear()
        Configuration.step_number = 0
        Configuration.selected_tasks.clear()
        Configuration.selected_connection = None

    @staticmethod
    def clear_canvas():
        """Clear the canvas and reset general variables."""
        SystemFunctions.clear_general_variables()
        Configuration.canvas.delete("all")

    @staticmethod
    def add_task():
        """Add a new task to the canvas."""
        from Objects.DraggableTask import DraggableTask

        print("Add task")
        new_task = DraggableTask("?", "?", Configuration.root.winfo_width() / 2, Configuration.root.winfo_height() / 2,
                                 50, 1, 0)
        Configuration.task_objects.append(new_task)

    @staticmethod
    def add_connection():
        """Add a new connection to the canvas."""
        from Objects.Connection.ConnectionActivity import ConnectionActivity
        from Objects.Connection.ConnectionTask import ConnectionTask

        print("Add connection")
        origin_task = \
        [task_object for task_object, position in Configuration.selected_tasks.items() if str(position) == str(1)][0]
        target_task = \
        [task_object for task_object, position in Configuration.selected_tasks.items() if str(position) == str(2)][0]

        new_offset = 0
        for connection in origin_task.connectors:
            if connection in target_task.connectors:
                connection.offset = 50
                new_offset = -50

        is_activity_connection = origin_task.task_name == target_task.task_name
        if is_activity_connection:
            new_connection = ConnectionActivity("?", 0, new_offset)
        else:
            new_connection = ConnectionTask("?", 0, new_offset)

        origin_task.add_connector(new_connection, "start")
        target_task.add_connector(new_connection, "end")

        origin_task.update_connections()
        target_task.update_connections()

        start_task_name = origin_task.task_name + origin_task.activity_name
        connector_name = new_connection.name
        end_task_name = target_task.task_name + target_task.activity_name
        initial_value = 0

        Configuration.connector_objects.append([start_task_name, connector_name, end_task_name, initial_value])

    @staticmethod
    def add_or_connection():
        """Add an OR connection to the canvas."""
        sel_task = \
        [task_object for task_object, position in Configuration.selected_tasks.items() if str(position) == str(1)][0]

        Configuration.selected_connection.add_or_connection(sel_task)
        sel_task.add_connector(Configuration.selected_connection, "or")
        sel_task.update_connections()

        Configuration.connector_objects.append([sel_task.task_name + sel_task.activity_name,
                                                Configuration.selected_connection.name,
                                                "",
                                                0])

    @staticmethod
    def add_new_mutex():
        selected_mutex_class_name = "Mutex" + Configuration.selected_mutex_type.replace(' ', '')
        selected_mutex_class = globals()[selected_mutex_class_name]

        new_mutex = selected_mutex_class()

        Configuration.mutex_objects.update({
            new_mutex.name: new_mutex
        })

        for task in Configuration.selected_tasks:
            task.add_mutex(new_mutex)
            new_mutex.add_task(task)

        new_mutex.update_visuals()

    @staticmethod
    def select_new_task(new_task):
        """
        Select a new task and assign it a unique number.

        Args:
            new_task: The new task to be selected.

        Returns:
            int: The assigned unique number for the new task.
        """
        new_number = 1
        while True:
            contains = False
            for task in Configuration.selected_tasks:
                task_number = Configuration.selected_tasks[task]
                if task_number == new_number:
                    contains = True

            if not contains:
                break
            new_number += 1

        Configuration.selected_tasks[new_task] = new_number
        SystemFunctions._update_sidebar()

        return new_number

    @staticmethod
    def remove_selected_task(task):
        """
        Remove a selected task from the selected_tasks dictionary.

        Args:
            task: The task to be removed from the selection.
        """
        Configuration.selected_tasks.pop(task)
        SystemFunctions._update_sidebar()

    @staticmethod
    def confirm_task_change():
        """
        Confirm the changes made to a task by updating its properties based on
        the sidebar inputs and update the task's visuals.
        """
        task = list(Configuration.selected_tasks.keys())[0]

        task_input = Configuration.sidebar_task_input.get()
        activity_input = Configuration.sidebar_activity_input.get()
        cycle_input = Configuration.sidebar_cycles_input.get()

        task.task_name = task_input
        task.activity_name = activity_input
        task.task_max_cycles = cycle_input

        task.update_visuals()

    @staticmethod
    def _update_sidebar():
        """
        Update the sidebar based on the currently selected tasks and connection.
        Show/hide the appropriate sidebar containers based on the selection.
        """
        if len(Configuration.selected_tasks) > 0:
            if Configuration.selected_connection is not None:
                Configuration.sidebar_add_or_connection_container.pack(
                    fill="both", expand=True
                )
                Configuration.sidebar_add_connection_container.pack_forget()
                Configuration.sidebar_edit_task_container.pack_forget()
                Configuration.sidebar_add_mutex_container.pack_forget()
                Configuration.sidebar_simulation.pack_forget()
            elif len(Configuration.selected_tasks) == 2:
                Configuration.sidebar_add_connection_container.pack(
                    fill="both", expand=True
                )
                Configuration.sidebar_edit_task_container.pack_forget()
                Configuration.sidebar_add_mutex_container.pack_forget()
                Configuration.sidebar_add_or_connection_container.pack_forget()
                Configuration.sidebar_simulation.pack_forget()
            elif len(Configuration.selected_tasks) == 1:
                Configuration.sidebar_edit_task_container.pack(
                    fill="both", expand=True
                )
                Configuration.sidebar_add_connection_container.pack_forget()
                Configuration.sidebar_add_mutex_container.pack_forget()
                Configuration.sidebar_add_or_connection_container.pack_forget()
                Configuration.sidebar_simulation.pack_forget()
            else:
                Configuration.sidebar_add_mutex_container.pack(
                    fill="both", expand=True
                )
                Configuration.sidebar_edit_task_container.pack_forget()
                Configuration.sidebar_add_connection_container.pack_forget()
                Configuration.sidebar_add_or_connection_container.pack_forget()
                Configuration.sidebar_simulation.pack_forget()

            SystemFunctions.toggle_sidebar(True)

            Configuration.sidebar_task_input.set(
                list(Configuration.selected_tasks.keys())[0].task_name
            )
            Configuration.sidebar_activity_input.set(
                list(Configuration.selected_tasks.keys())[0].activity_name
            )
            Configuration.sidebar_cycles_input.set(
                list(Configuration.selected_tasks.keys())[0].task_max_cycles
            )
        elif Configuration.show_simulation_container:
            Configuration.sidebar_simulation.pack(
                fill="both", expand=True
            )
            Configuration.sidebar_add_connection_container.pack_forget()
            Configuration.sidebar_edit_task_container.pack_forget()
            Configuration.sidebar_add_mutex_container.pack_forget()
            Configuration.sidebar_add_or_connection_container.pack_forget()
        else:
            SystemFunctions.toggle_sidebar(False)

    @staticmethod
    def toggle_sidebar(show=True):
        """
        Toggle the visibility of the sidebar with an animation effect.

        Args:
            show (bool): Whether to show or hide the sidebar. Defaults to True.
        """
        from threading import Thread
        t = Thread(target=SystemFunctions._sidebar_animation, args=(show,))
        t.start()

    @staticmethod
    def _sidebar_animation(show):
        import time

        if Configuration.sidebar.winfo_x() == -300 and show:
            for i in range(0, 301, 10):
                Configuration.canvas.place(x=i, relwidth=1.0, relheight=1.0)
                Configuration.sidebar.place(relx=0, rely=0, relheight=1, x=-300 + i)
                Configuration.sidebar.update()
                time.sleep(0.001)
        elif Configuration.sidebar.winfo_x() == 0 and not show:
            for i in range(0, 301, 10):
                Configuration.canvas.place(x=300 - i)
                Configuration.sidebar.place(relx=0, rely=0, relheight=1, x=-i)
                Configuration.sidebar.update()
                time.sleep(0.001)

    @staticmethod
    def delete_selection():
        """
        Delete the selected tasks and their associated connectors.
        Update the task objects, connector objects, and selected tasks accordingly.
        """
        for task in Configuration.selected_tasks:
            con_cpy = task.connectors.copy()
            for connector in con_cpy:
                for task2 in Configuration.task_objects:
                    if connector in task2.connectors:
                        task2.connectors.pop(connector)
                        task2.update_connections()
                        connector.delete()

            to_del_cons = []
            for con_obj in Configuration.connector_objects:
                if task.task_name + task.activity_name in con_obj:
                    to_del_cons.append(con_obj)

            for con_obj in to_del_cons:
                Configuration.connector_objects.remove(con_obj)

            Configuration.task_objects.remove(task)
            task.delete()

        Configuration.selected_tasks.clear()

    # Simulation sidebar methods
    @staticmethod
    def toggle_simulation_sidebar():
        """Toggle visibility of the simulation sidebar."""
        if Configuration.edit_mode:
            return

        Configuration.show_simulation_container = not Configuration.show_simulation_container
        SystemFunctions.toggle_sidebar(Configuration.show_simulation_container)
        SystemFunctions._update_sidebar()

    @staticmethod
    def update_speed_value():
        """Update the displayed speed value."""
        Configuration.dynamic_value_label.configure(text=f"Period per Cycle: {Configuration.current_delay}ms")

    @staticmethod
    def update_simulation_speed(value):
        """Update the simulation speed based on the slider value."""
        # Convert slider value to a delay (in milliseconds)
        Configuration.current_delay = int(3000 + 1 - value)
        print(f"Speed set to {value}, delay {Configuration.current_delay} ms")
        SystemFunctions.update_speed_value()

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
    def stop_simulation():
        """Stop the simulation."""
        Configuration.auto_run = False

    @staticmethod
    def run_periodically():
        """Run the simulation periodically based on the current delay."""
        if Configuration.auto_run:
            SystemFunctions.step()
            # Schedule the next call
            Configuration.root.after(Configuration.current_delay, SystemFunctions.run_periodically)

    @staticmethod
    def start_simulation():
        """Start the simulation."""
        if not Configuration.auto_run:
            SystemFunctions.update_simulation_speed(value=1)
            Configuration.auto_run = True
            SystemFunctions.run_periodically()

    # Create sidebar containers
    @staticmethod
    def create_sidebar():
        """Create the main sidebar."""
        Configuration.sidebar = Frame(Configuration.root, width=300, bd=0, bg="#303030")
        Configuration.sidebar.place(relx=0, rely=0, relheight=1, x=-300)

        Configuration.sidebar_task_input = StringVar()
        Configuration.sidebar_activity_input = StringVar()
        Configuration.sidebar_cycles_input = IntVar()

        sidebar_title = Label(Configuration.sidebar, text="Editor", font=("Montserrat Light", 20), bg="#2A2A2A", fg="white",
                              width=15)
        sidebar_title.pack(side=TOP, anchor=N, padx=0, pady=10)
        SystemFunctions.create_edit_task_container()
        SystemFunctions.create_connection_container()
        SystemFunctions.create_mutex_container()
        SystemFunctions.create_or_connection_container()
        SystemFunctions.create_run_container()

    @staticmethod
    def create_run_container():
        """Create the simulation sidebar."""
        Configuration.sidebar_simulation = Frame(Configuration.sidebar, bd=0, bg="#303030")

        sidebar_title = Label(Configuration.sidebar_simulation, text="Simulation", font=("Montserrat Light", 20), bg="#2A2A2A", fg="white", width=15)
        sidebar_title.pack(side=TOP, anchor=N, padx=0, pady=10)

        sim_start_button = customtkinter.CTkButton(Configuration.sidebar_simulation, text="Start", command=SystemFunctions.start_simulation)
        sim_start_button.pack(pady=10, padx=10)

        sim_end_button = customtkinter.CTkButton(Configuration.sidebar_simulation, text="Stop", command=SystemFunctions.stop_simulation)
        sim_end_button.pack(pady=10, padx=10)

        speed_slider = customtkinter.CTkSlider(Configuration.sidebar_simulation, from_=1, to=3000, number_of_steps=3000)
        speed_slider.pack(side=customtkinter.TOP, fill=customtkinter.X, padx=10, pady=10)
        speed_slider.set(1000)  # Set default speed value
        speed_slider.configure(command=SystemFunctions.update_simulation_speed)

        Configuration.dynamic_value_label = customtkinter.CTkLabel(Configuration.sidebar_simulation, text="Period per Cycle: 1000ms", bg_color=Configuration.root['bg'], fg_color="#303030")
        Configuration.dynamic_value_label.pack(pady=10)

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
                              font=("Montserrat Light", 12), command=lambda: SystemFunctions.confirm_task_change(),
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
                              font=("Montserrat Light", 12), command=lambda: SystemFunctions.add_new_mutex(),
                              width=20)
        button_label.pack()

        # Create a frame to simulate the button appearance
        button_add_connection_frame = Frame(Configuration.sidebar_add_connection_container, bg="#303030", bd=1,
                                            relief="solid",
                                            highlightbackground=Configuration.task_color,
                                            highlightthickness=1)
        button_add_connection_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_add_connection_frame, text="ADD CONNECTION", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: SystemFunctions.add_connection(),
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
                              font=("Montserrat Light", 12), command=lambda: SystemFunctions.add_new_mutex(),
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
                              font=("Montserrat Light", 12), command=lambda: SystemFunctions.add_or_connection(),
                              width=20)
        button_label.pack()