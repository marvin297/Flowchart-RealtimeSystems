# -*- coding: utf-8 -*-
"""
Module for loading and saving flowchart data to/from Excel files.

This module provides functions to load task and connector data from an Excel
file to create a visual flowchart, as well as save the current flowchart
state to an Excel file.

The main functions are:

load_files(show_file_dialog=False):
    Loads flowchart data from an Excel file. If show_file_dialog is True,
    opens a dialog to select the file. Otherwise, loads from a predefined
    file path.

save_file():
    Saves the current flowchart state, including task and connector
    information, to an Excel file selected via a file dialog.

The module relies on the following classes to represent flowchart components:
- DraggableTask: Represents a task in the flowchart
- MutexPriorityInversion: Represents a mutex
- TaskConnector: Represents a connector between tasks

It also utilizes the pandas library to read from and write to Excel files.
"""

# Import necessary modules
from tkinter import filedialog
import pandas as pd
from Objects.DraggableTask import DraggableTask
from Objects.Connection.TaskConnection import TaskConnector
from General.Configuration import Configuration

# Import available mutex types
from Objects.Mutex.MutexPriorityInversion import MutexPriorityInversion
from Objects.Mutex.MutexPriorityCeiling import MutexPriorityCeiling
from Objects.Mutex.MutexTicketLock import MutexTicketLock
from Objects.Mutex.MutexFirstComeFirstServe import MutexFirstComeFirstServe


# Function to load files from a file dialog or a predefined path
def load_files(show_file_dialog=False):
    """
    Load flowchart data from an Excel file.

    If show_file_dialog is True, open a dialog to select the file.
    Otherwise, load from a predefined file path.
    """
    if show_file_dialog:
        # Open file dialog to select Excel file
        Configuration.last_import_file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("Excel :)", "*.xlsx"), ("all files", "*.*"))
        )

    # If no file path is provided, return without doing anything
    if Configuration.last_import_file_path == "":
        return

    import math

    # Read the first sheet of the Excel file into a pandas DataFrame
    table_of_content = pd.read_excel(Configuration.last_import_file_path)

    # Clear general variables and canvas
    Configuration.clear_general_variables()
    Configuration.canvas.delete("all")

    selected_mutex_class_name = "Mutex" + Configuration.selected_mutex_type.replace(' ', '')
    selected_mutex_class = globals()[selected_mutex_class_name]

    # Iterate over rows in the DataFrame
    for index, row in table_of_content.iterrows():
        task_name = "Undefined"
        activity_name = ""
        pos_x = 50
        pos_y = 50
        cycles = 1
        mutexes = []
        priority = 0

        # Iterate over the first 8 columns of the row
        for column, cell_value in row.iloc[:8].items():  # stop after index 6
            if str(column).startswith("Unnamed: "):
                break

            # Check if the cell value is NaN (Not a Number) and skip if it is
            if type(cell_value) is float:
                if math.isnan(cell_value):
                    continue

            # Assign values to variables based on the column name
            match column:
                case "TASK":
                    task_name = str(int(cell_value))

                case "ACTIVITY":
                    if type(cell_value) is not float:
                        activity_name = str(cell_value)

                case "CYCLES":
                    cycles = int(cell_value)

                case "PRIORITY":
                    priority = int(cell_value)

                case "MUTEX_LIST":
                    if type(cell_value) is not float:
                        mutex_string = str(cell_value)
                        mutex_names = mutex_string.split(",")
                        for mutex_name in mutex_names:
                            if mutex_name not in Configuration.mutex_objects:
                                new_mutex_object = selected_mutex_class()
                                Configuration.mutex_objects.update({
                                    mutex_name: new_mutex_object
                                })
                                new_mutex_object.name = mutex_name

                            mutexes.append(Configuration.mutex_objects[mutex_name])
                    else:
                        pass
                    print("Mutex")

                case "POSX":
                    if not math.isnan(cell_value):
                        pos_x = cell_value
                    print("Position X")

                case "POSY":
                    if not math.isnan(cell_value):
                        pos_y = cell_value
                    print("Position Y")

        # If task_name is still "Undefined", break out of the loop
        if task_name == "Undefined":
            break

        # Create a new DraggableTask object with the extracted values
        task = DraggableTask(task_name, activity_name, pos_x, pos_y, 50, cycles, priority)

        # Add mutexes to the task and task to the mutexes
        if len(mutexes) > 0:
            for mutex in mutexes:
                task.add_mutex(mutex)
                mutex.add_task(task)

        # Add the task to the list of task objects
        Configuration.task_objects.append(task)

    # List to store semaphore information
    semaphores = []

    # Iterate over remaining columns in the DataFrame
    for index, row in table_of_content.iterrows():
        start_task_name = "Undefined"
        connector_name = "Undefined"
        end_task_name = "Undefined"
        initial_value = 0

        # Iterate over columns starting from index 8
        for column, cell_value in row.iloc[8:].items():  # Start from index 7
            if type(cell_value) is float:
                continue

            # Assign values to variables based on the column name
            match column:
                case "START":
                    start_task_name = str(cell_value)
                case "CON_NAME":
                    connector_name = str(cell_value)
                case "END":
                    end_task_name = str(cell_value)
                case "INITIAL_VALUE":
                    initial_value = int(cell_value)

        # Add semaphore information to the list
        semaphores.append([start_task_name, connector_name, end_task_name, initial_value, 0])

    # List to store duplicate semaphore indices
    duplicates = []

    # Iterate over semaphores and handle connections
    for i in range(len(semaphores)):
        semaphore = semaphores[i]
        start_task_name = semaphore[0]
        connector_name = semaphore[1]
        end_task_name = semaphore[2]
        initial_value = semaphore[3]
        offset = semaphore[4]

        # If end_task_name is "Undefined", handle OR connection
        if end_task_name == "Undefined":
            needed_connector = None
            for task in Configuration.task_objects:
                for connector in task.connectors:
                    if connector.name == connector_name:
                        needed_connector = connector
                        break
                if needed_connector is not None:
                    break

            for task in Configuration.task_objects:
                if start_task_name == task.task_name + task.activity_name:
                    needed_connector.add_or_connection(task)
                    task.add_connector(needed_connector, "or")
                    task.update_connections()
            break

        # Handle duplicate semaphores
        for j in range(len(semaphores)):
            semaphore2 = semaphores[j]
            if semaphore2[0] == end_task_name:
                if semaphore2[2] == start_task_name:
                    if i not in duplicates and j not in duplicates:
                        duplicates.append(i)
                        duplicates.append(j)
                        print("duplicate")
                        semaphore2[4] = 50
                        offset = -50

        # Skip if connector_name is "Undefined"
        if connector_name == "Undefined":
            continue

        import re
        start_task_id = re.findall(r'\d+', start_task_name)
        end_task_id = re.findall(r'\d+', end_task_name)

        activity_connection = False

        # Check if start and end tasks have the same ID
        if len(end_task_id) > 0:
            if start_task_id[0] == end_task_id[0]:
                activity_connection = True

        # Create a new TaskConnector object
        connector = TaskConnector(connector_name, semaphore_value=initial_value, activity_connection=activity_connection, offset=offset)
        Configuration.connector_objects.append([start_task_name, connector_name, end_task_name, initial_value])

        # Add connector to start and end tasks
        for task in Configuration.task_objects:
            if (task.task_name + task.activity_name) == start_task_name:
                if end_task_name != "":
                    task.add_connector(connector, "start")
        for task in Configuration.task_objects:
            if (task.task_name + task.activity_name) == end_task_name:
                task.add_connector(connector, "end")

    # Update connections for all tasks
    for task in Configuration.task_objects:
        task.update_connections()

    # Update visuals for all mutexes
    for mutex in Configuration.mutex_objects:
        Configuration.mutex_objects[mutex].update_visuals()


# Function to save the current state to a file
def save_file():
    """Saves the current state of the program to an Excel file."""
    # Extract task information from Configuration.task_objects
    task_values = [task.task_name for task in Configuration.task_objects]
    activity_values = [task.activity_name for task in Configuration.task_objects]
    cycle_values = [task.task_max_cycles for task in Configuration.task_objects]
    priority_values = [0 for i in range(len(Configuration.task_objects))]
    mutex_values = [",".join([mutex.name for mutex in task.mutexes]) for task in Configuration.task_objects]
    pos_x_values = [task.get_position()[0] + 50 for task in Configuration.task_objects]
    pos_y_values = [task.get_position()[1] + 50 for task in Configuration.task_objects]

    # Extract connector information from Configuration.connector_objects
    start_values = [connector[0] for connector in Configuration.connector_objects]
    con_values = [connector[1] for connector in Configuration.connector_objects]
    end_values = [connector[2] for connector in Configuration.connector_objects]
    initial_values = [connector[3] for connector in Configuration.connector_objects]

    # Ensure all lists have the same length by padding with None
    if len(Configuration.task_objects) > len(Configuration.connector_objects):
        for i in range(len(Configuration.task_objects) - len(Configuration.connector_objects)):
            start_values.append(None)
            con_values.append(None)
            end_values.append(None)
            initial_values.append(None)

    elif len(Configuration.task_objects) < len(Configuration.connector_objects):
        for i in range(len(Configuration.connector_objects) - len(Configuration.task_objects)):
            task_values.append(None)
            activity_values.append(None)
            cycle_values.append(None)
            mutex_values.append(None)
            priority_values.append(None)
            pos_x_values.append(None)
            pos_y_values.append(None)

    # Create a pandas DataFrame from the extracted data
    data = {
        'TASK': task_values,
        'ACTIVITY': activity_values,
        'CYCLES': cycle_values,
        'PRIORITY': priority_values,
        'MUTEX_LIST': mutex_values,
        'POSX': pos_x_values,
        'POSY': pos_y_values,
        '': [None for i in range(len(task_values))],
        'START': start_values,
        'CON_NAME': con_values,
        'END': end_values,
        'INITIAL_VALUE': initial_values
    }
    df = pd.DataFrame(data)

    # Open a file dialog to save the Excel file
    f = filedialog.asksaveasfilename(filetypes=(("Excel :)", "*.xlsx"), ("all files", "*.*")))
    if f == "":
        return

    file_name = f

    # Append .xlsx extension if not present
    if not f.endswith(".xlsx"):
        file_name += ".xlsx"

    # Save the DataFrame to the selected file
    df.to_excel(file_name, index=False)