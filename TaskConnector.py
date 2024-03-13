from GeneralVariables import GeneralVariables

class TaskConnector:
    def __init__(self, name, semaphore_value=0, activity_connection=False, offset=0):
        self.name = name
        self.circle_radius = 50
        self.line = GeneralVariables.canvas.create_line(0, 0, 0, 0, width=5, fill="#ff335c", arrow="last", arrowshape=(25, 25, 10)) \
            if not activity_connection \
            else GeneralVariables.canvas.create_line(0, 0, 0, 0, width=2, fill="#ff9233", arrow="last",arrowshape=(10, 25, 10))
        self.end_x = 0
        self.end_y = 0
        self.semaphore_value = semaphore_value
        self.last_change = 0

        self.offset = offset

        self.semaphore_text = GeneralVariables.canvas.create_text(0, 0, text=str(semaphore_value), fill=GeneralVariables.root['bg'], font=("Arial", 12, "bold"))
        self.semaphore_bg = GeneralVariables.canvas.create_oval(0, 0, 0, 0, fill="#ff335c", outline="#ff335c")

        GeneralVariables.canvas.pack()

    def decrement_semaphore(self, change_time):
        self.last_change = change_time

        self.semaphore_value -= 1
        GeneralVariables.canvas.itemconfig(self.semaphore_text, text=str(self.semaphore_value))

    def increment_semaphore(self, change_time):
        self.last_change = change_time

        self.semaphore_value += 1
        GeneralVariables.canvas.itemconfig(self.semaphore_text, text=str(self.semaphore_value))

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
