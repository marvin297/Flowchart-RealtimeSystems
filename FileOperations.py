from tkinter import filedialog
import pandas as pd
from DraggableTask import DraggableTask
from TaskConnector import TaskConnector


task_objects = []
connector_objects = []


def browseFiles(canvas, root):
    filename = filedialog.askopenfilename(title="Select a File", filetypes=(("Excel :)", "*.xlsx"), ("all files", "*.*")))
    import math

    # read by default 1st sheet of an excel file
    table_of_content = pd.read_excel(filename)

    global task_objects
    global connector_objects
    task_objects = []
    connector_objects = []
    canvas.delete("all")

    for index, row in table_of_content.iterrows():
        task_name = "Undefined"
        activity_name = ""
        pos_x = 50
        pos_y = 50

        for column, cell_value in row.iloc[:7].items():  # stop after index 6
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
                    print("Cycles")

                case "PRIORITY":
                    print("Priority")

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
        task = DraggableTask(canvas, task_name, activity_name, pos_x, pos_y, 50, root)

        task_objects.append(task)

    for index, row in table_of_content.iterrows():
        start_task_name = "Undefined"
        connector_name = "Undefined"
        end_task_name = "Undefined"
        for column, cell_value in row.iloc[7:].items():  # Start from index 7
            if type(cell_value) is float:
                continue
            match column:
                case "START":
                    start_task_name = str(cell_value)
                case "CON_NAME":
                    connector_name = str(cell_value)
                case "END":
                    end_task_name = str(cell_value)

        if connector_name == "Undefined":
            continue

        import re
        start_task_id = re.findall(r'\d+', start_task_name)
        end_task_id = re.findall(r'\d+', end_task_name)

        activity_connection = False

        if start_task_id[0] == end_task_id[0]:
            activity_connection = True

        connector = TaskConnector(canvas, connector_name, activity_connection)
        connector_objects.append([start_task_name, connector_name, end_task_name])

        for task in task_objects:
            if (task.task_name + task.activity_name) == start_task_name:
                task.add_connector(connector, "start")
        for task in task_objects:
            if (task.task_name + task.activity_name) == end_task_name:
                task.add_connector(connector, "end")

    for task in task_objects:
        task.update_connections()


def saveFile():
    task_values = [task.task_name for task in task_objects]
    activity_values = [task.activity_name for task in task_objects]
    cycle_values = [0 for i in range(len(task_objects))]
    priority_values = [0 for i in range(len(task_objects))]
    pos_x_values = [task.get_position()[0]+50 for task in task_objects]
    pos_y_values = [task.get_position()[1]+50 for task in task_objects]

    start_values = [connector[0] for connector in connector_objects]
    con_values = [connector[1] for connector in connector_objects]
    end_values = [connector[2] for connector in connector_objects]

    if len(task_objects) > len(connector_objects):
        for i in range(len(task_objects) - len(connector_objects)):
            start_values.append(None)
            con_values.append(None)
            end_values.append(None)
    elif len(task_objects) < len(connector_objects):
        for i in range(len(connector_objects) - len(task_objects)):
            task_values.append(None)
            activity_values.append(None)
            cycle_values.append(None)
            priority_values.append(None)
            pos_x_values.append(None)
            pos_y_values.append(None)

    data = {
        'TASK': task_values,
        'ACTIVITY': activity_values,
        'CYCLES': cycle_values,
        'PRIORITY': priority_values,
        'POSX': pos_x_values,
        'POSY': pos_y_values,
        '': [None for i in range(len(task_values))],
        'START': start_values,
        'CON_NAME': con_values,
        'END': end_values
    }
    df = pd.DataFrame(data)

    f = filedialog.asksaveasfilename(filetypes=(("Excel :)", "*.xlsx"), ("all files", "*.*")))
    if f == "":
        return

    file_name = f

    if not f.endswith(".xlsx"):
        file_name += ".xlsx"

    df.to_excel(file_name, index=False)