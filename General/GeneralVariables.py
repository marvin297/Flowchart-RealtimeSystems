from tkinter import StringVar, IntVar


class GeneralVariables:
    task_objects = []
    connector_objects = []
    mutex_objects = {}
    step_number = 0
    canvas = None
    root = None

    sidebar = None
    sidebar_edit_task_container = None
    sidebar_add_connection_container = None
    sidebar_add_mutex_container = None
    sidebar_add_or_connection_container = None
    sidebar_task_input = None
    sidebar_activity_input = None
    sidebar_cycles_input = None

    simulation_sidebar = None

    selected_tasks = {}
    selected_connection = None
    edit_mode = False

    font_black = None
    font_light = None

    arrow_color = "#767676"
    arrow_color_selected = "#464646"
    activity_arrow_color = "#029cff"
    activity_arrow_color_selected = "#0065a6"
    mutex_color = "#464646"

    task_color = "#029cff"
    task_color_selected = "#00335c"
    task_color_running = "red"

    last_import_file_path = ""

    @staticmethod
    def clear_general_variables():
        GeneralVariables.task_objects.clear()
        GeneralVariables.connector_objects.clear()
        GeneralVariables.mutex_objects.clear()
        GeneralVariables.step_number = 0
        GeneralVariables.selected_tasks.clear()
        GeneralVariables.selected_connection = None

    @staticmethod
    def select_new_task(new_task):
        new_number = 1
        while True:
            contains = False
            for task in GeneralVariables.selected_tasks:
                task_number = GeneralVariables.selected_tasks[task]
                if task_number == new_number:
                    contains = True

            if not contains:
                break
            new_number += 1

        GeneralVariables.selected_tasks[new_task] = new_number

        GeneralVariables._update_sidebar()

        return new_number

    @staticmethod
    def remove_selected_task(task):
        GeneralVariables.selected_tasks.pop(task)

        GeneralVariables._update_sidebar()

    @staticmethod
    def confirm_task_change():
        task = list(GeneralVariables.selected_tasks.keys())[0]

        task_input = GeneralVariables.sidebar_task_input.get()
        activity_input = GeneralVariables.sidebar_activity_input.get()
        cycle_input = GeneralVariables.sidebar_cycles_input.get()

        task.task_name = task_input
        task.activity_name = activity_input
        task.task_max_cycles = cycle_input

        task.update_visuals()

    @staticmethod
    def _update_sidebar():
        if len(GeneralVariables.selected_tasks) > 0:
            if GeneralVariables.selected_connection is not None:
                GeneralVariables.sidebar_add_or_connection_container.pack(fill="both", expand=True)
                GeneralVariables.sidebar_add_connection_container.pack_forget()
                GeneralVariables.sidebar_edit_task_container.pack_forget()
                GeneralVariables.sidebar_add_mutex_container.pack_forget()
            elif len(GeneralVariables.selected_tasks) == 2:
                GeneralVariables.sidebar_add_connection_container.pack(fill="both", expand=True)
                GeneralVariables.sidebar_edit_task_container.pack_forget()
                GeneralVariables.sidebar_add_mutex_container.pack_forget()
                GeneralVariables.sidebar_add_or_connection_container.pack_forget()
            elif len(GeneralVariables.selected_tasks) == 1:
                GeneralVariables.sidebar_edit_task_container.pack(fill="both", expand=True)
                GeneralVariables.sidebar_add_connection_container.pack_forget()
                GeneralVariables.sidebar_add_mutex_container.pack_forget()
                GeneralVariables.sidebar_add_or_connection_container.pack_forget()
            else:
                GeneralVariables.sidebar_add_mutex_container.pack(fill="both", expand=True)
                GeneralVariables.sidebar_edit_task_container.pack_forget()
                GeneralVariables.sidebar_add_connection_container.pack_forget()
                GeneralVariables.sidebar_add_or_connection_container.pack_forget()

            GeneralVariables.toggle_sidebar(True)

            GeneralVariables.sidebar_task_input.set(list(GeneralVariables.selected_tasks.keys())[0].task_name)
            GeneralVariables.sidebar_activity_input.set(list(GeneralVariables.selected_tasks.keys())[0].activity_name)
            GeneralVariables.sidebar_cycles_input.set(list(GeneralVariables.selected_tasks.keys())[0].task_max_cycles)
        else:
            GeneralVariables.toggle_sidebar(False)

    @staticmethod
    def toggle_sidebar(show=True):
        import time
        if GeneralVariables.sidebar.winfo_x() == -300 and show:
            for i in range(0, 301, 10):  # Adjust the range and step size for smoother animation
                GeneralVariables.sidebar.place(relx=0, rely=0, relheight=1, x=-300 + i)
                GeneralVariables.sidebar.update()  # Force update to immediately apply changes
                time.sleep(0.001)  # Adjust sleep duration for smoother animation
        elif GeneralVariables.sidebar.winfo_x() == 0 and not show:
            for i in range(0, 301, 10):  # Adjust the range and step size for smoother animation
                GeneralVariables.sidebar.place(relx=0, rely=0, relheight=1, x=-i)
                GeneralVariables.sidebar.update()  # Force update to immediately apply changes
                time.sleep(0.001)  # Adjust sleep duration for smoother animation
