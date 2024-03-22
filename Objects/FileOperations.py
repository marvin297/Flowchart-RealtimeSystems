from tkinter import filedialog
import pandas as pd
from Objects.DraggableTask import DraggableTask
from Mutex.MutexPriorityInversion import MutexPriorityInversion
from General.TaskConnector import TaskConnector
from General.GeneralVariables import GeneralVariables


def browse_files():
    filename = filedialog.askopenfilename(title="Select a File", filetypes=(("Excel :)", "*.xlsx"), ("all files", "*.*")))
    if filename == "":
        return

    import math

    # read by default 1st sheet of an excel file
    table_of_content = pd.read_excel(filename)

    GeneralVariables.clear_general_variables()
    GeneralVariables.canvas.delete("all")

    for index, row in table_of_content.iterrows():
        task_name = "Undefined"
        activity_name = ""
        pos_x = 50
        pos_y = 50
        cycles = 1
        mutexes = []
        priority = 0

        for column, cell_value in row.iloc[:8].items():  # stop after index 6
            if str(column).startswith("Unnamed: "):
                break

            if type(cell_value) is float:
                if math.isnan(cell_value):
                    continue

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
                            if mutex_name not in GeneralVariables.mutex_objects:
                                GeneralVariables.mutex_objects.update({
                                    mutex_name: MutexPriorityInversion()
                                })

                            mutexes.append(GeneralVariables.mutex_objects[mutex_name])
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

        if task_name == "Undefined":
            break
        task = DraggableTask(task_name, activity_name, pos_x, pos_y, 50, cycles, priority)
        if len(mutexes) > 0:
            for mutex in mutexes:
                task.add_mutex(mutex)
                mutex.add_task(task)

        GeneralVariables.task_objects.append(task)

    semaphores = []
    for index, row in table_of_content.iterrows():
        start_task_name = "Undefined"
        connector_name = "Undefined"
        end_task_name = "Undefined"
        initial_value = 0
        for column, cell_value in row.iloc[8:].items():  # Start from index 7
            if type(cell_value) is float:
                continue
            match column:
                case "START":
                    start_task_name = str(cell_value)
                case "CON_NAME":
                    connector_name = str(cell_value)
                case "END":
                    end_task_name = str(cell_value)
                case "INITIAL_VALUE":
                    initial_value = int(cell_value)

        semaphores.append([start_task_name, connector_name, end_task_name, initial_value, 0])

    duplicates = []
    for i in range(len(semaphores)):
        semaphore = semaphores[i]
        start_task_name = semaphore[0]
        connector_name = semaphore[1]
        end_task_name = semaphore[2]
        initial_value = semaphore[3]
        offset = semaphore[4]

        if end_task_name == "Undefined":
            needed_connector = None
            for task in GeneralVariables.task_objects:
                for connector in task.connectors:
                    if connector.name == connector_name:
                        needed_connector = connector
                        break
                if needed_connector is not None:
                    break

            for task in GeneralVariables.task_objects:
                if start_task_name == task.task_name + task.activity_name:
                    needed_connector.add_or_connection(task)
                    task.add_connector(needed_connector, "or")
                    task.update_connections()
            break

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

        if connector_name == "Undefined":
            continue

        import re
        start_task_id = re.findall(r'\d+', start_task_name)
        end_task_id = re.findall(r'\d+', end_task_name)

        activity_connection = False

        if len(end_task_id) > 0:
            if start_task_id[0] == end_task_id[0]:
                activity_connection = True

        connector = TaskConnector(connector_name, semaphore_value=initial_value, activity_connection=activity_connection, offset=offset)
        GeneralVariables.connector_objects.append([start_task_name, connector_name, end_task_name, initial_value])

        for task in GeneralVariables.task_objects:
            if (task.task_name + task.activity_name) == start_task_name:
                if end_task_name != "":
                    task.add_connector(connector, "start")
        for task in GeneralVariables.task_objects:
            if (task.task_name + task.activity_name) == end_task_name:
                task.add_connector(connector, "end")

    for task in GeneralVariables.task_objects:
        task.update_connections()

    for mutex in GeneralVariables.mutex_objects:
        GeneralVariables.mutex_objects[mutex].update_visuals()


def save_file():
    task_values = [task.task_name for task in GeneralVariables.task_objects]
    activity_values = [task.activity_name for task in GeneralVariables.task_objects]
    cycle_values = [task.task_max_cycles for task in GeneralVariables.task_objects]
    priority_values = [0 for i in range(len(GeneralVariables.task_objects))]
    mutex_values = [",".join([mutex.name for mutex in task.mutexes]) for task in GeneralVariables.task_objects]
    pos_x_values = [task.get_position()[0]+50 for task in GeneralVariables.task_objects]
    pos_y_values = [task.get_position()[1]+50 for task in GeneralVariables.task_objects]

    start_values = [connector[0] for connector in GeneralVariables.connector_objects]
    con_values = [connector[1] for connector in GeneralVariables.connector_objects]
    end_values = [connector[2] for connector in GeneralVariables.connector_objects]
    initial_values = [connector[3] for connector in GeneralVariables.connector_objects]

    if len(GeneralVariables.task_objects) > len(GeneralVariables.connector_objects):
        for i in range(len(GeneralVariables.task_objects) - len(GeneralVariables.connector_objects)):
            start_values.append(None)
            con_values.append(None)
            end_values.append(None)
            initial_values.append(None)

    elif len(GeneralVariables.task_objects) < len(GeneralVariables.connector_objects):
        for i in range(len(GeneralVariables.connector_objects) - len(GeneralVariables.task_objects)):
            task_values.append(None)
            activity_values.append(None)
            cycle_values.append(None)
            mutex_values.append(None)
            priority_values.append(None)
            pos_x_values.append(None)
            pos_y_values.append(None)

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

    f = filedialog.asksaveasfilename(filetypes=(("Excel :)", "*.xlsx"), ("all files", "*.*")))
    if f == "":
        return

    file_name = f

    if not f.endswith(".xlsx"):
        file_name += ".xlsx"

    df.to_excel(file_name, index=False)