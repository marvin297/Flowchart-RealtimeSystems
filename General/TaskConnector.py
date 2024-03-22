from General.GeneralVariables import GeneralVariables


class TaskConnector:
    def __init__(self, name, semaphore_value=0, activity_connection=False, offset=0):
        self.name = name
        self.circle_radius = 50
        self.line = GeneralVariables.canvas.create_line(0, 0, 0, 0, width=5, fill=GeneralVariables.arrow_color, arrow="last", arrowshape=(25, 25, 10), smooth=True) \
            if not activity_connection \
            else GeneralVariables.canvas.create_line(0, 0, 0, 0, width=2, fill=GeneralVariables.activity_arrow_color, arrow="last", arrowshape=(10, 25, 10), smooth=True)
        self.end_x = 0
        self.end_y = 0
        self.semaphore_value = semaphore_value
        self.last_change = 0
        self.activity_connection = activity_connection
        self.selected = False

        self.or_connections = {}  # TASKS THAT ALSO INCREASE THIS SEMAPHORE (OR) // STRUCTURE: {taskObject: lineObject}

        self.offset = offset

        self.semaphore_text = GeneralVariables.canvas.create_text(0, 0, text=str(semaphore_value), fill=GeneralVariables.root['bg'], font=("Montserrat Light", 12, "bold"))
        self.semaphore_bg = GeneralVariables.canvas.create_oval(0, 0, 0, 0, fill=GeneralVariables.arrow_color if not activity_connection else GeneralVariables.activity_arrow_color, outline=GeneralVariables.arrow_color if not activity_connection else GeneralVariables.activity_arrow_color)

        GeneralVariables.canvas.tag_bind(self.line, "<Button-1>", lambda event: self.on_click())

        GeneralVariables.canvas.pack()

    def decrement_semaphore(self, change_time):
        self.last_change = change_time

        self.semaphore_value -= 1
        GeneralVariables.canvas.itemconfig(self.semaphore_text, text=str(self.semaphore_value))

    def increment_semaphore(self, change_time):
        self.last_change = change_time

        self.semaphore_value += 1
        GeneralVariables.canvas.itemconfig(self.semaphore_text, text=str(self.semaphore_value))

    def on_click(self):
        print("selected")
        if GeneralVariables.selected_connection != self:
            if GeneralVariables.selected_connection is not None:
                GeneralVariables.selected_connection.selected = False
                GeneralVariables.selected_connection.update_visuals()

            GeneralVariables.selected_connection = self
            self.selected = True
        else:
            GeneralVariables.selected_connection = None
            self.selected = False

        self.update_visuals()

        GeneralVariables._update_sidebar()

    def update_visuals(self):
        selected_color = None
        reset_color = None

        if self.activity_connection:
            selected_color = GeneralVariables.activity_arrow_color_selected
            reset_color = GeneralVariables.activity_arrow_color
        else:
            selected_color = GeneralVariables.arrow_color_selected
            reset_color = GeneralVariables.arrow_color

        if self.selected:
            GeneralVariables.canvas.itemconfig(self.line, fill=selected_color)
            GeneralVariables.canvas.itemconfig(self.semaphore_bg, fill=selected_color, outline=selected_color)
        else:
            GeneralVariables.canvas.itemconfig(self.line, fill=reset_color)
            GeneralVariables.canvas.itemconfig(self.semaphore_bg, fill=reset_color, outline=reset_color)

    def update_start(self, new_x, new_y):
        x1, y1, x2, y2 = GeneralVariables.canvas.coords(self.line)
        GeneralVariables.canvas.coords(self.line, new_x, new_y + self.offset, x2, y2 + self.offset)

    def update_end(self, new_x, new_y, override_end=False):
        x1, y1, x2, y2 = GeneralVariables.canvas.coords(self.line)

        if not override_end:
            self.end_x = new_x
            self.end_y = new_y
        else:
            new_x = self.end_x
            new_y = self.end_y

        self.update_semaphore(new_x, new_y)

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

        GeneralVariables.canvas.coords(self.line, x1, y1, end_x, end_y)

        self.update_or_connections()

    def update_semaphore(self, new_x, new_y):
        x1, y1, x2, y2 = GeneralVariables.canvas.coords(self.line)
        sx1, sy1, sx2, sy2 = GeneralVariables.canvas.bbox(self.semaphore_text)

        text_width = sx2 - sx1

        GeneralVariables.canvas.coords(self.semaphore_text, (x1 + new_x) / 2, (y1 + new_y) / 2)

        GeneralVariables.canvas.coords(self.semaphore_bg, (x1 + new_x) / 2 - text_width / 2 - 5,
                           (y1 + new_y) / 2 - text_width / 2 - 5,
                           (x1 + new_x) / 2 + text_width / 2 + 5,
                           (y1 + new_y) / 2 + text_width / 2 + 5)

        GeneralVariables.canvas.tag_raise(self.semaphore_text)

        self.update_or_connections()

    def add_or_connection(self, task):
        line_object = GeneralVariables.canvas.create_line(0, 0, 0, 0, width=5, fill=GeneralVariables.arrow_color, smooth=True) \
            if not self.activity_connection \
            else GeneralVariables.canvas.create_line(0, 0, 0, 0, width=2, fill=GeneralVariables.activity_arrow_color, smooth=True)

        self.or_connections[task] = line_object

    def update_single_or_connection(self, task):
        x1, y1, x2, y2 = GeneralVariables.canvas.coords(self.line)

        x_end = x2 + (x1 - x2) / 2
        y_end = y2 + (y1 - y2) / 2

        x1_task, y1_task, x2_task, y2_task = GeneralVariables.canvas.coords(task.oval)
        connection_line = self.or_connections[task]
        GeneralVariables.canvas.coords(connection_line, x1_task + 50, y1_task + 50, x_end, y_end)

    def update_or_connections(self):
        for task in self.or_connections:
            self.update_single_or_connection(task)