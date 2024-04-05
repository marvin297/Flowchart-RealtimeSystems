# -*- coding: utf-8 -*-
# Import necessary modules
from General.Configuration import Configuration, SystemFunctions
import time
import math
from abc import ABC


class ConnectionBase(ABC):
    """
    A class representing a connector between tasks in a workflow.

    This class creates a line on a canvas that connects two tasks and represents
    a dependency or relationship between them. It displays a semaphore value and
    allows for visual customization based on the type of connection (regular or
    activity). The connector can be selected and updated dynamically as the tasks
    are moved or modified.
    """

    def __init__(self, name, arrow_color, arrow_color_selected, arrow_head_style, line_width, semaphore_value=0, offset=0):
        """
        Initialize a new instance of the TaskConnector class.

        Args:
            name (str): The name of the connector.
            arrow_color (str): The color of the connector.
            arrow_color_selected (str): The color of the connector when selected.
            arrow_head_style (tuple): The style of the arrow head.
            semaphore_value (int, optional): The initial semaphore value. Defaults to 0.
            offset (int, optional): The offset value for positioning the connector. Defaults to 0.
        """
        self.name = name
        self.circle_radius = 50
        self.arrow_color = arrow_color
        self.arrow_color_selected = arrow_color_selected
        self.arrow_head_style = arrow_head_style
        self.line = Configuration.canvas.create_line(0, 0, 0, 0,
                                                     width=line_width,
                                                     fill=self.arrow_color,
                                                     arrow="last",
                                                     arrowshape=self.arrow_head_style,
                                                     smooth=True)
        self.end_x = 0
        self.end_y = 0
        self.semaphore_value = semaphore_value
        self.last_change = 0
        self.selected = False

        self.or_connections = {}  # TASKS THAT ALSO INCREASE THIS SEMAPHORE (OR) // STRUCTURE: {taskObject: lineObject}

        self.offset = offset

        self.semaphore_text = Configuration.canvas.create_text(0, 0, text=str(semaphore_value), fill=Configuration.root['bg'], font=("Montserrat Light", 12, "bold"))
        self.semaphore_bg = Configuration.canvas.create_oval(0, 0, 0, 0, fill=self.arrow_color, outline="")

        Configuration.canvas.tag_bind(self.line, "<Button-1>", lambda event: self.on_click())

    def delete(self):
        """Delete the connector and its associated objects from the canvas."""
        Configuration.canvas.delete(self.line)
        Configuration.canvas.delete(self.semaphore_text)
        Configuration.canvas.delete(self.semaphore_bg)

        for task in self.or_connections:
            Configuration.canvas.delete(self.or_connections[task])

    def decrement_semaphore(self, change_time):
        """
        Decrement the semaphore value and update the visual representation.

        Args:
            change_time (int): The timestamp of the change.
        """
        self.last_change = change_time

        self.semaphore_value -= 1
        Configuration.canvas.itemconfig(self.semaphore_text, text=str(self.semaphore_value))

        from threading import Thread
        t = Thread(target=self.visualise_semaphore_change, args=(True,))
        t.start()

    def increment_semaphore(self, change_time):
        """
        Increment the semaphore value and update the visual representation.

        Args:
            change_time (int): The timestamp of the change.
        """
        self.last_change = change_time

        self.semaphore_value += 1
        Configuration.canvas.itemconfig(self.semaphore_text, text=str(self.semaphore_value))

        from threading import Thread
        t = Thread(target=self.visualise_semaphore_change, args=(False,))
        t.start()

    def visualise_semaphore_change(self, decrement=False):
        x1, y1, x2, y2 = Configuration.canvas.coords(self.line)
        slope = (y1 - y2) / (x1 - x2)

        angle = math.atan(slope)
        angle = math.degrees(angle)
        c = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        arrow_length = 15
        max_length = (c - self.circle_radius) / 2 - arrow_length

        color = "red" if decrement else "green"
        highlight_color = "#f74545" if decrement else "#61ff4a"

        line = Configuration.canvas.create_line(0, 0, 0, 0, width=5, fill=highlight_color, arrow="last",
                                                arrowshape=(arrow_length, arrow_length, 1.5), smooth=True)
        Configuration.canvas.itemconfig(self.semaphore_bg, fill=color)
        Configuration.canvas.itemconfig(self.line, fill=color)

        for i in range(0, 100, 1):
            if decrement:
                current_length = max_length + (max_length / 100) * i + self.circle_radius + arrow_length
            else:
                current_length = (max_length / 100) * i + self.circle_radius + arrow_length

            if x1 <= x2:
                start_x = x1 + (current_length - 10) * math.cos(math.radians(angle))
                start_y = y1 + (current_length - 10) * math.sin(math.radians(angle))

                end_x = x1 + current_length * math.cos(math.radians(angle))
                end_y = y1 + current_length * math.sin(math.radians(angle))
            else:
                start_x = x1 - (current_length - 10) * math.cos(math.radians(angle))
                start_y = y1 - (current_length - 10) * math.sin(math.radians(angle))

                end_x = x1 - current_length * math.cos(math.radians(angle))
                end_y = y1 - current_length * math.sin(math.radians(angle))

            Configuration.canvas.coords(line, start_x, start_y, end_x, end_y)
            Configuration.canvas.update()

            if Configuration.auto_run:
                time.sleep(Configuration.current_delay / 1000 / 100 / 2)
            else:
                time.sleep(0.005)

        Configuration.canvas.delete(line)

        Configuration.canvas.itemconfig(self.semaphore_bg, fill=self.arrow_color)
        Configuration.canvas.itemconfig(self.line, fill=self.arrow_color)

    def on_click(self):
        """Handle the click event on the connector."""
        print("selected")
        if not Configuration.edit_mode:
            return

        if Configuration.selected_connection != self:
            if Configuration.selected_connection is not None:
                Configuration.selected_connection.selected = False
                Configuration.selected_connection.update_visuals()

            Configuration.selected_connection = self
            self.selected = True
        else:
            Configuration.selected_connection = None
            self.selected = False

        self.update_visuals()

        SystemFunctions._update_sidebar()

    def update_visuals(self):
        """Update the visual appearance of the connector based on its selection state."""
        if self.selected:
            Configuration.canvas.itemconfig(self.line, fill=self.arrow_color_selected)
            Configuration.canvas.itemconfig(self.semaphore_bg, fill=self.arrow_color_selected, outline=self.arrow_color_selected)
        else:
            Configuration.canvas.itemconfig(self.line, fill=self.arrow_color)
            Configuration.canvas.itemconfig(self.semaphore_bg, fill=self.arrow_color, outline=self.arrow_color)

    def update_start(self, new_x, new_y):
        """
        Update the start coordinates of the connector.

        Args:
            new_x (int): The new x-coordinate of the start point.
            new_y (int): The new y-coordinate of the start point.
        """
        x1, y1, x2, y2 = Configuration.canvas.coords(self.line)
        Configuration.canvas.coords(self.line, new_x, new_y + self.offset, x2, y2 + self.offset)

    def update_end(self, new_x, new_y, override_end=False):
        """
        Update the end coordinates of the connector.

        Args:
            new_x (int): The new x-coordinate of the end point.
            new_y (int): The new y-coordinate of the end point.
            override_end (bool, optional): Indicates if the end coordinates should be overridden. Defaults to False.
        """
        x1, y1, x2, y2 = Configuration.canvas.coords(self.line)

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

        Configuration.canvas.coords(self.line, x1, y1, end_x, end_y)

        self.update_or_connections()

    def update_semaphore(self, new_x, new_y):
        """
        Update the position of the semaphore text and background.

        Args:
            new_x (int): The new x-coordinate of the semaphore.
            new_y (int): The new y-coordinate of the semaphore.
        """
        x1, y1, x2, y2 = Configuration.canvas.coords(self.line)
        sx1, sy1, sx2, sy2 = Configuration.canvas.bbox(self.semaphore_text)

        text_width = sx2 - sx1

        Configuration.canvas.coords(self.semaphore_text, (x1 + new_x) / 2, (y1 + new_y) / 2)

        Configuration.canvas.coords(self.semaphore_bg, (x1 + new_x) / 2 - text_width / 2 - 5,
                                    (y1 + new_y) / 2 - text_width / 2 - 5,
                                    (x1 + new_x) / 2 + text_width / 2 + 5,
                                    (y1 + new_y) / 2 + text_width / 2 + 5)

        Configuration.canvas.tag_raise(self.semaphore_text)

        self.update_or_connections()

    def add_or_connection(self, task):
        """
        Add an OR connection to the specified task.

        Args:
            task (Task): The task to add the OR connection to.
        """
        line_object = Configuration.canvas.create_line(0, 0, 0, 0, width=5, fill=self.arrow_color, smooth=True)

        self.or_connections[task] = line_object

    def update_single_or_connection(self, task):
        """
        Update the OR connection to the specified task.

        Args:
            task (Task): The task to update the OR connection for.
        """
        x1, y1, x2, y2 = Configuration.canvas.coords(self.line)

        x_end = x2 + (x1 - x2) / 2
        y_end = y2 + (y1 - y2) / 2

        x1_task, y1_task, x2_task, y2_task = Configuration.canvas.coords(task.oval)
        connection_line = self.or_connections[task]
        Configuration.canvas.coords(connection_line, x1_task + 50, y1_task + 50, x_end, y_end)

    def update_or_connections(self):
        """Update all OR connections associated with the connector."""
        for task in self.or_connections:
            self.update_single_or_connection(task)
