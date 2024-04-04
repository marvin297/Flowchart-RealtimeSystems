"""
This module defines the Configuration class, which manages the configuration
settings and state of the application. It includes methods for handling task
selection, updating the sidebar, and deleting selected tasks.
"""


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

    # Variable to store reference to the simulation sidebar
    simulation_sidebar = None

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

    available_mutex_types = ['Priority Ceiling', 'Priority Inversion', 'Ticket Lock']
    selected_mutex_type = 'Priority Ceiling'

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
        Configuration._update_sidebar()

        return new_number

    @staticmethod
    def remove_selected_task(task):
        """
        Remove a selected task from the selected_tasks dictionary.

        Args:
            task: The task to be removed from the selection.
        """
        Configuration.selected_tasks.pop(task)
        Configuration._update_sidebar()

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
            elif len(Configuration.selected_tasks) == 2:
                Configuration.sidebar_add_connection_container.pack(
                    fill="both", expand=True
                )
                Configuration.sidebar_edit_task_container.pack_forget()
                Configuration.sidebar_add_mutex_container.pack_forget()
                Configuration.sidebar_add_or_connection_container.pack_forget()
            elif len(Configuration.selected_tasks) == 1:
                Configuration.sidebar_edit_task_container.pack(
                    fill="both", expand=True
                )
                Configuration.sidebar_add_connection_container.pack_forget()
                Configuration.sidebar_add_mutex_container.pack_forget()
                Configuration.sidebar_add_or_connection_container.pack_forget()
            else:
                Configuration.sidebar_add_mutex_container.pack(
                    fill="both", expand=True
                )
                Configuration.sidebar_edit_task_container.pack_forget()
                Configuration.sidebar_add_connection_container.pack_forget()
                Configuration.sidebar_add_or_connection_container.pack_forget()

            Configuration.toggle_sidebar(True)

            Configuration.sidebar_task_input.set(
                list(Configuration.selected_tasks.keys())[0].task_name
            )
            Configuration.sidebar_activity_input.set(
                list(Configuration.selected_tasks.keys())[0].activity_name
            )
            Configuration.sidebar_cycles_input.set(
                list(Configuration.selected_tasks.keys())[0].task_max_cycles
            )
        else:
            Configuration.toggle_sidebar(False)

    @staticmethod
    def toggle_sidebar(show=True):
        """
        Toggle the visibility of the sidebar with an animation effect.

        Args:
            show (bool): Whether to show or hide the sidebar. Defaults to True.
        """
        import time

        if Configuration.sidebar.winfo_x() == -300 and show:
            for i in range(0, 301, 10):
                Configuration.sidebar.place(relx=0, rely=0, relheight=1, x=-300 + i)
                Configuration.sidebar.update()
                time.sleep(0.001)
        elif Configuration.sidebar.winfo_x() == 0 and not show:
            for i in range(0, 301, 10):
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