from tkinter import *
import customtkinter


class CustomButton(customtkinter.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = self

    def on_release(self, event):
        pass
        # self.configure(fg_color="blue", text="Released")

    def on_drag(self, event):
        self.place(x=self.root.winfo_pointerx() - self.root.winfo_rootx() - self.winfo_width() / 2,
                   y=self.root.winfo_pointery() - self.root.winfo_rooty() - self.winfo_height() / 2)
        # self.configure(fg_color="red", text="Dragging")


class CustomCanvas(Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = self

    def on_release(self, event):
        pass
        # self.configure(fg_color="blue", text="Released")

    def on_drag(self, event):
        self.place(x=self.root.winfo_pointerx() - self.root.winfo_rootx() - self.winfo_width() / 2,
                   y=self.root.winfo_pointery() - self.root.winfo_rooty() - self.winfo_height() / 2)
        # self.configure(fg_color="red", text="Dragging")


class TaskConnector:
    def __init__(self, canvas, name, activity_connection=False):
        self.name = name
        self.canvas = canvas
        self.circle_radius = 50
        self.line = canvas.create_line(0, 0, 0, 0, width=5, fill="#ff335c", arrow="last", arrowshape=(25, 25, 10)) \
            if not activity_connection \
            else canvas.create_line(0, 0, 0, 0, width=2, fill="#ff9233", arrow="last",arrowshape=(10, 25, 10))
        self.canvas.pack()
        self.end_x = 0
        self.end_y = 0

    def update_start(self, new_x, new_y):
        x1, y1, x2, y2 = self.canvas.coords(self.line)
        self.canvas.coords(self.line, new_x, new_y, x2, y2)

    def update_end(self, new_x, new_y, test=False):
        x1, y1, x2, y2 = self.canvas.coords(self.line)

        if not test:
            self.end_x = new_x
            self.end_y = new_y
        else:
            new_x = self.end_x
            new_y = self.end_y

        if x1 == new_x:
            x1 = new_x + 0.000000001

        import math
        slope = (y1 - new_y) / (x1 - new_x)

        angle = math.atan(slope)
        angle = math.degrees(angle)
        c = math.sqrt((x1 - new_x) ** 2 + (y1 - new_y) ** 2)
        new_distance = c - self.circle_radius

        if x1 <= new_x:
            end_x = x1 + new_distance * math.cos(math.radians(angle))
            end_y = y1 + new_distance * math.sin(math.radians(angle))
        else:
            end_x = x1 - new_distance * math.cos(math.radians(angle))
            end_y = y1 - new_distance * math.sin(math.radians(angle))

        self.canvas.coords(self.line, x1, y1, end_x, end_y)


class DraggableTask:
    def __init__(self, canvas, task_name, activity_name, x, y, radius, root):
        self.canvas = canvas
        self.oval = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=root['bg'],
                                       outline="#ff335c", width=5)
        self.connectors = {}
        self.task_name = task_name
        self.activity_name = activity_name

        self.name = canvas.create_text(x, y, text=task_name, fill="#ff335c", font=("Arial", 12))

        # self.canvas.tag_bind(self.oval, "<Button-1>", self.on_drag_start)
        self.canvas.tag_bind(self.oval, "<B1-Motion>", lambda event: self.on_drag(event))
        self.canvas.tag_bind(self.name, "<B1-Motion>", lambda event: self.on_drag(event))
        # self.canvas.tag_bind(self.oval, "<ButtonRelease-1>", self.on_drag_stop)

        self.canvas.pack()

    def on_drag(self, event):
        x = event.x - 50
        y = event.y - 50
        self.canvas.coords(self.oval, x, y, x + 100, y + 100)  # Adjust 100 according to your oval size
        self.canvas.coords(self.name, x + 50, y + 50)
        self.update_connections()

    def update_connections(self):
        for connection in self.connectors:
            self.canvas.tag_raise(self.oval, connection.line)
            self.canvas.tag_raise(self.name, self.oval)
            if self.connectors[connection] == "start":
                connection.update_start(self.get_position()[0] + 50, self.get_position()[1] + 50)
                connection.update_end(0, 0, True)

            elif self.connectors[connection] == "end":
                end_x = self.get_position()[0] + 50
                end_y = self.get_position()[1] + 50
                connection.update_end(end_x, end_y)

    def get_position(self):
        return self.canvas.coords(self.oval)

    def set_connectors(self, connectors):
        self.connectors = connectors

    def add_connector(self, connector, position):
        self.connectors[connector] = position


from tkinter import filedialog
import pandas as pd


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
        col_index: int = 0

        for column, cell_value in row.items():
            if str(column).startswith("Unnamed: "):
                break

            if col_index < 6:
                print(f"Row: {index}, Column: {column}, Value: {cell_value}")

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

            col_index += 1

        if task_name == "Undefined":
            break
        task = DraggableTask(canvas, task_name, activity_name, pos_x, pos_y, 50, root)

        task_objects.append(task)

    for index, row in table_of_content.iterrows():
        col_index: int = 0
        start_task_name = "Undefined"
        connector_name = "Undefined"
        end_task_name = "Undefined"
        for column, cell_value in row.items():
            if col_index > 6:
                print(f"Row: {index}, Column: {column}, Value: {cell_value}")
                if type(cell_value) is float:
                    continue
                match column:
                    case "START":
                        print(cell_value)
                        start_task_name = str(cell_value)
                    case "CON_NAME":
                        connector_name = str(cell_value)
                    case "END":
                        end_task_name = str(cell_value)
            col_index += 1

        if connector_name == "Undefined":
            continue

        print("create")

        import re
        start_task_id = re.findall('\d+', start_task_name)
        end_task_id = re.findall('\d+', end_task_name)

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
    if f == "":  # asksaveasfile return `None` if dialog closed with "cancel".
        return

    file_name = f

    if not f.endswith(".xlsx"):
        file_name += ".xlsx"

    df.to_excel(file_name, index=False)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")
        self.geometry("800x800")

        # configure window
        self.title("Flowchart Editor")

        # Create a canvas object
        c = Canvas(self, bd=0, highlightthickness=0, background=self['bg'])
        c.pack(fill=BOTH, expand=True)

        load_file_btn = customtkinter.CTkButton(c, text="Load file", command=lambda: browseFiles(c, self)).pack()
        store_file_btn = customtkinter.CTkButton(c, text="Store file", command=saveFile).pack()
        next_step_btn = customtkinter.CTkButton(c, text="Next step", command=lambda: print("Stepping...")).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
