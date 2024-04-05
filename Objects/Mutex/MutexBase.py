from abc import ABC, abstractmethod
from General.Configuration import Configuration


class MutexBase(ABC):
    def __init__(self):
        self.name = "unnamed"
        self.algorithm_type = "No description"
        self.lock = False
        self.connected_tasks = []
        self.lines = []

        self.holder = None
        self.attendees = []

        self.mutex_text = Configuration.canvas.create_text(0, 0, text=self.name, fill="white",
                                                           font=("Montserrat Black", 12, "bold"))
        self.locked_text = Configuration.canvas.create_text(0, 0, text=("Locked" if self.lock else "Unlocked"),
                                                            fill="white",
                                                            font=("Montserrat Light", 8, "bold"))

        self.mutex_bg = Configuration.canvas.create_polygon([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            fill=Configuration.mutex_color,
                                                            outline=Configuration.mutex_color)

        #Configuration.canvas.pack()

    def add_task(self, task):
        self.connected_tasks.append(task)
        self.lines.append(Configuration.canvas.create_line(0, 0, 0, 0, fill=Configuration.mutex_color, width=5))

    @abstractmethod
    def attend(self, task):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def release(self, task):
        pass

    def update_visuals(self):
        # TODO: display current algorithm type with 'algorithm_type' variable

        # iterate over connected tasks name
        mutex_name = "m" + "".join([task.task_name for task in self.connected_tasks])
        if mutex_name != self.name:
            print(Configuration.mutex_objects.keys())
            Configuration.mutex_objects.pop(self.name)
            self.name = mutex_name
            Configuration.mutex_objects.update({self.name: self})

        Configuration.canvas.itemconfig(self.mutex_text, text=self.name)
        Configuration.canvas.itemconfig(self.locked_text, text=("Locked" if self.lock else "Unlocked"))

        sx1, sy1, sx2, sy2 = Configuration.canvas.bbox(self.mutex_text)
        text_width = sx2 - sx1
        text_height = sy2 - sy1

        if text_width < 100:
            text_width = 100

        new_x = 0
        new_y = 0
        for task in self.connected_tasks:
            new_x += Configuration.canvas.coords(task.oval)[0] + 50
            new_y += Configuration.canvas.coords(task.oval)[1] + 50

        new_x /= len(self.connected_tasks)
        new_y /= len(self.connected_tasks)

        Configuration.canvas.coords(self.mutex_text, new_x, new_y - 10)
        Configuration.canvas.coords(self.locked_text, new_x, new_y + 10)
        padding = 20
        edge_padding = -5
        #GeneralVariables.canvas.coords(self.mutex_bg, new_x - text_width / 2, new_y - text_width / 2, new_x + text_width / 2, new_y + text_width / 2)
        Configuration.canvas.coords(self.mutex_bg, [
                                            new_x - text_width / 2 - padding, new_y,
                                            new_x - text_width / 2 + edge_padding,  new_y + text_height / 2 + padding,
                                            new_x + text_width / 2 - edge_padding,  new_y + text_height / 2 + padding,
                                            new_x + text_width / 2 + padding, new_y,
                                            new_x + text_width / 2 - edge_padding,  new_y - text_height / 2 - padding,
                                            new_x - text_width / 2 + edge_padding,  new_y - text_height / 2 - padding
                                        ])

        Configuration.canvas.tag_raise(self.mutex_text, self.mutex_bg)
        Configuration.canvas.tag_raise(self.locked_text)

        task_index = 0
        for line in self.lines:
            Configuration.canvas.coords(line,
                                        new_x,
                                        new_y,
                                        Configuration.canvas.bbox(self.connected_tasks[task_index].oval)[0] + 50,
                                        Configuration.canvas.bbox(self.connected_tasks[task_index].oval)[1] + 50
                                        )

            Configuration.canvas.tag_lower(line)
            task_index += 1

