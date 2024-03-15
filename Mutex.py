from GeneralVariables import GeneralVariables


class Mutex:
    def __init__(self, name):
        self.name = name
        self.lock = False
        self.connected_tasks = []
        self.lines = []

        self.attendees = []

        self.mutex_text = GeneralVariables.canvas.create_text(0, 0, text=self.name, fill="white",
                                                 font=("Montserrat Black", 12, "bold"))
        self.locked_text = GeneralVariables.canvas.create_text(0, 0, text=("Locked" if self.lock else "Unlocked"), fill="white",
                                                 font=("Montserrat Light", 8, "bold"))

        self.mutex_bg = GeneralVariables.canvas.create_polygon([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], fill=GeneralVariables.mutex_color, outline=GeneralVariables.mutex_color)

        GeneralVariables.canvas.pack()

    def add_task(self, task):
        self.connected_tasks.append(task)
        self.lines.append(GeneralVariables.canvas.create_line(0, 0, 0, 0, fill=GeneralVariables.mutex_color, width=5))

    def attend(self, attendee):
        self.attendees.append(attendee)

    def evaluate(self):
        if self.lock or len(self.attendees) == 0:
            return
        self.lock = True
        print("Mutex locked for " + self.attendees[0].task_name + self.attendees[0].activity_name)
        self.attendees[0].grant_access()

        self.attendees.clear()

    def release(self):
        print("Mutex released")
        self.lock = False

    def update_visuals(self):
        GeneralVariables.canvas.itemconfig(self.mutex_text, text=self.name)
        GeneralVariables.canvas.itemconfig(self.locked_text, text=("Locked" if self.lock else "Unlocked"))

        sx1, sy1, sx2, sy2 = GeneralVariables.canvas.bbox(self.mutex_text)
        text_width = sx2 - sx1
        text_height = sy2 - sy1

        if text_width < 100:
            text_width = 100

        new_x = 0
        new_y = 0
        for task in self.connected_tasks:
            new_x += GeneralVariables.canvas.coords(task.oval)[0] + 50
            new_y += GeneralVariables.canvas.coords(task.oval)[1] + 50

        new_x /= len(self.connected_tasks)
        new_y /= len(self.connected_tasks)

        GeneralVariables.canvas.coords(self.mutex_text, new_x, new_y - 10)
        GeneralVariables.canvas.coords(self.locked_text, new_x, new_y + 10)
        padding = 20
        edge_padding = -5
        #GeneralVariables.canvas.coords(self.mutex_bg, new_x - text_width / 2, new_y - text_width / 2, new_x + text_width / 2, new_y + text_width / 2)
        GeneralVariables.canvas.coords(self.mutex_bg, [
                                            new_x - text_width / 2 - padding, new_y,
                                            new_x - text_width / 2 + edge_padding,  new_y + text_height / 2 + padding,
                                            new_x + text_width / 2 - edge_padding,  new_y + text_height / 2 + padding,
                                            new_x + text_width / 2 + padding, new_y,
                                            new_x + text_width / 2 - edge_padding,  new_y - text_height / 2 - padding,
                                            new_x - text_width / 2 + edge_padding,  new_y - text_height / 2 - padding
                                        ])

        GeneralVariables.canvas.tag_raise(self.mutex_text, self.mutex_bg)
        GeneralVariables.canvas.tag_raise(self.locked_text)

        task_index = 0
        for line in self.lines:
            GeneralVariables.canvas.coords(line,
                                           new_x,
                                           new_y,
                                           GeneralVariables.canvas.bbox(self.connected_tasks[task_index].oval)[0] + 50,
                                           GeneralVariables.canvas.bbox(self.connected_tasks[task_index].oval)[1] + 50
                                           )

            GeneralVariables.canvas.tag_lower(line)
            task_index += 1
