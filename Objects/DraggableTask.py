# -*- coding: utf-8 -*-
# Import necessary modules
from General.Configuration import Configuration


class DraggableTask:
    """
    A class representing a draggable task visualization.

    This class creates an oval shape on a canvas that can be dragged around
    to represent a task. It displays the task name, activity name, and current
    cycle. The task can be connected to other tasks and participate in mutexes.
    """

    def __init__(self, task_name, activity_name, x, y, radius, task_max_cycles, priority):
        """
        Initialize a new DraggableTask instance.

        Args:
            task_name (str): The name of the task.
            activity_name (str): The name of the activity.
            x (int): The x-coordinate of the center of the task oval.
            y (int): The y-coordinate of the center of the task oval.
            radius (int): The radius of the task oval.
            task_max_cycles (int): The maximum number of cycles for the task.
            priority (int): The priority of the task.
        """
        # Create the oval shape representing the task
        self.oval = Configuration.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=Configuration.root['bg'], outline=Configuration.task_color, width=2
        )

        self.connectors = {}
        self.task_name = task_name
        self.activity_name = activity_name
        self.selected = False

        self.mutexes = []
        self.granted_mutexes = 0
        self.priority = priority
        self.original_priority = priority

        # Initialize task cycle attributes
        self.task_current_cycle = 0
        self.task_max_cycles = task_max_cycles

        # Create labels for task name, activity name, and cycle
        self.name_label = Configuration.canvas.create_text(
            x, y - 20, text="Task " + self.task_name, fill="white",
            font=("Montserrat Black", 12)
        )
        self.activity_label = Configuration.canvas.create_text(
            x, y, text="Activity " + (self.activity_name if self.activity_name != "" else self.task_name),
            fill="white", font=("Montserrat Black", 10)
        )
        self.cycle_label = Configuration.canvas.create_text(
            x, y + 20,
            text="Cycle " + str(self.task_current_cycle) + "/" + str(self.task_max_cycles),
            fill="white", font=("Montserrat Light", 8)
        )

        self.selection_text = Configuration.canvas.create_text(
            x, y - radius - 20, text="", fill="#00335c", font=("Arial", 12)
        )

        # Bind mouse events to the task elements
        Configuration.canvas.tag_bind(self.oval, "<Button-1>", lambda event: self.clicked(task_name, activity_name))
        Configuration.canvas.tag_bind(self.name_label, "<Button-1>",
                                      lambda event: self.clicked(task_name, activity_name))
        Configuration.canvas.tag_bind(self.activity_label, "<Button-1>",
                                      lambda event: self.clicked(task_name, activity_name))
        Configuration.canvas.tag_bind(self.cycle_label, "<Button-1>",
                                      lambda event: self.clicked(task_name, activity_name))

        Configuration.canvas.tag_bind(self.oval, "<B1-Motion>", lambda event: self.on_drag(event))
        Configuration.canvas.tag_bind(self.name_label, "<B1-Motion>", lambda event: self.on_drag(event))
        Configuration.canvas.tag_bind(self.activity_label, "<B1-Motion>", lambda event: self.on_drag(event))
        Configuration.canvas.tag_bind(self.cycle_label, "<B1-Motion>", lambda event: self.on_drag(event))

        Configuration.canvas.pack()

    def delete(self):
        """Delete the task and its associated elements from the canvas."""
        Configuration.canvas.delete(self.oval)
        Configuration.canvas.delete(self.name_label)
        Configuration.canvas.delete(self.activity_label)
        Configuration.canvas.delete(self.cycle_label)
        Configuration.canvas.delete(self.selection_text)

        for connector in self.connectors:
            connector.delete()

        print("DELETING TASK")

    def try_step(self):
        """
        Attempt to perform a step of the task.

        This method checks if the task can start a new cycle based on its
        connections and mutexes. If the conditions are met, it starts a new
        cycle or ends the current cycle.
        """
        # Increment the current cycle if not at the maximum
        if self.task_max_cycles > self.task_current_cycle > 0:
            self.task_current_cycle += 1

        # Check if the task can start a new cycle based on connections
        amount_of_needed_connections_to_start = 0
        amount_of_ready_connections_to_start = 0
        for connection in self.connectors:
            if self.connectors[connection] == "end":
                amount_of_needed_connections_to_start += 1
                if connection.semaphore_value > 0 and self.task_current_cycle == 0 and connection.last_change != Configuration.step_number:
                    amount_of_ready_connections_to_start += 1

        self.attend(amount_of_needed_connections_to_start, amount_of_ready_connections_to_start)

        self._end_cycle()

        self.update_status_text()

    def _start_cycle(self):
        """Start a new cycle for the task."""
        for connection in self.connectors:
            if self.connectors[connection] == "end" and connection.semaphore_value > 0:
                self.task_current_cycle = 1
                connection.decrement_semaphore(Configuration.step_number)

        self.update_status_text()
        self.granted_mutexes = 0

        Configuration.canvas.itemconfig(self.oval, outline=Configuration.task_color_running)

    def attend(self, amount_of_needed_connections_to_start, amount_of_ready_connections_to_start):
        """
        Attend to the task based on the number of needed and ready connections.

        If the task has the required number of ready connections and is not
        currently in a cycle, it will attempt to acquire mutexes (if any) and
        start a new cycle.
        """
        if amount_of_needed_connections_to_start == amount_of_ready_connections_to_start and self.task_current_cycle == 0 and amount_of_needed_connections_to_start > 0:
            if len(self.mutexes) > 0:
                for mutex in self.mutexes:
                    mutex.attend(self)
            else:
                self._start_cycle()

    def grant_access(self):
        """
        Grant mutex access to the task.

        This method is called when the task acquires a mutex. If all required
        mutexes are granted, the task starts a new cycle.
        """
        print("Access granted to", self.task_name, self.activity_name)
        self.granted_mutexes += 1
        if len(self.mutexes) == self.granted_mutexes:
            self._start_cycle()

    def add_mutex(self, mutex):
        """
        Add a mutex to the task.

        Args:
            mutex (Mutex): The mutex to add.
        """
        print("Added mutex " + mutex.name + " to task " + self.task_name + self.activity_name)
        self.mutexes.append(mutex)

    def _end_cycle(self):
        """
        End the current cycle of the task.

        This method is called when the task completes its maximum number of
        cycles. It increments the semaphores of connected tasks, releases
        mutexes, and resets the task's cycle count and visual appearance.
        """
        # If the task is done with the current cycle, increment semaphores of connected tasks
        if self.task_current_cycle == self.task_max_cycles:
            print(
                "ENDING CYCLE " + self.task_name + self.activity_name + " " + str(self.task_current_cycle) + "/" + str(
                    self.task_max_cycles))
            for connection in self.connectors:
                if self.connectors[connection] == "start" or self.connectors[connection] == "or":
                    connection.increment_semaphore(Configuration.step_number)
            self.task_current_cycle = 0
            if len(self.mutexes) > 0:
                for mutex in self.mutexes:
                    mutex.release(self)

            Configuration.canvas.itemconfig(self.oval, outline=Configuration.task_color)

    def on_drag(self, event):
        """
        Handle the drag event when the task is being dragged on the canvas.

        Args:
            event (Event): The drag event.
        """
        if Configuration.edit_mode:
            return

        # Update the position of the task elements based on the drag event
        x = event.x - 50
        y = event.y - 50
        Configuration.canvas.coords(self.oval, x, y, x + 100, y + 100)
        Configuration.canvas.coords(self.name_label, x + 50, y + 50 - 20)
        Configuration.canvas.coords(self.activity_label, x + 50, y + 50)
        Configuration.canvas.coords(self.cycle_label, x + 50, y + 50 + 20)

        Configuration.canvas.coords(self.selection_text, x + 50, y - 20)
        self.update_connections()

        for mutex in self.mutexes:
            mutex.update_visuals()

    def update_status_text(self):
        """Update the status text displaying the current cycle of the task."""
        Configuration.canvas.itemconfig(self.cycle_label,
                                        text="Cycle " + str(self.task_current_cycle) + "/" + str(self.task_max_cycles))

    def update_visuals(self):
        """Update the visual elements of the task with the current task information."""
        Configuration.canvas.itemconfig(self.name_label, text="Task " + self.task_name)
        Configuration.canvas.itemconfig(self.activity_label,
                                        text="Activity " + self.activity_name if self.activity_name != "" else self.task_name)
        self.update_status_text()

    def update_connections(self):
        """Update the positions of the task's connections."""
        for connection in self.connectors:
            Configuration.canvas.tag_raise(self.oval, connection.line)
            Configuration.canvas.tag_raise(self.name_label, self.oval)
            Configuration.canvas.tag_raise(self.activity_label, self.oval)
            Configuration.canvas.tag_raise(self.cycle_label)
            if self.connectors[connection] == "start":
                connection.update_start(self.get_position()[0] + 50, self.get_position()[1] + 50)
                connection.update_end(0, 0, True)

            elif self.connectors[connection] == "end":
                end_x = self.get_position()[0] + 50
                end_y = self.get_position()[1] + 50
                connection.update_end(end_x, end_y)

            elif self.connectors[connection] == "or":
                connection.update_single_or_connection(self)

                for or_con in connection.or_connections:
                    line = connection.or_connections[or_con]
                    Configuration.canvas.tag_raise(self.oval, line)
                    Configuration.canvas.tag_raise(self.name_label, self.oval)
                    Configuration.canvas.tag_raise(self.activity_label, self.oval)
                    Configuration.canvas.tag_raise(self.cycle_label)

    def get_position(self):
        """
        Get the current position of the task on the canvas.

        Returns:
            tuple: The coordinates of the task oval.
        """
        return Configuration.canvas.coords(self.oval)

    def set_connectors(self, connectors):
        """
        Set the connectors of the task.

        Args:
            connectors (dict): A dictionary mapping connectors to their positions.
        """
        self.connectors = connectors

    def add_connector(self, connector, position):
        """
        Add a connector to the task.

        Args:
            connector (Connector): The connector to add.
            position (str): The position of the connector (e.g., "start", "end").
        """
        self.connectors[connector] = position

    def clicked(self, task_name, activity_name):
        """
        Handle the click event when the task is clicked.

        Args:
            task_name (str): The name of the task.
            activity_name (str): The name of the activity.
        """
        if not Configuration.edit_mode:
            return

        print("Clicked on task: " + task_name + activity_name)
        self.selected = not self.selected
        if self.selected:
            selection_number = Configuration.select_new_task(self)
            Configuration.canvas.itemconfig(self.selection_text, text=str(selection_number))
            Configuration.canvas.itemconfig(self.oval, outline=Configuration.task_color_selected)
        else:
            Configuration.canvas.itemconfig(self.selection_text, text="")
            if self.task_current_cycle > 0:
                Configuration.canvas.itemconfig(self.oval, outline=Configuration.task_color_running)
            else:
                Configuration.canvas.itemconfig(self.oval, outline=Configuration.task_color)
            Configuration.remove_selected_task(self)

    @staticmethod
    def switch_selection():
        """Switch the selection mode of the tasks."""
        print("change")
        if Configuration.show_simulation_container:
            return

        Configuration.edit_mode = not Configuration.edit_mode

        for task in Configuration.selected_tasks:
            Configuration.canvas.itemconfig(task.selection_text, text="")
            Configuration.canvas.itemconfig(task.oval, outline=Configuration.task_color)
            task.selected = False

        Configuration.selected_tasks.clear()

        if Configuration.selected_connection is not None:
            Configuration.selected_connection.selected = False
            Configuration.selected_connection.update_visuals()

        Configuration.selected_connection = None

        Configuration.toggle_sidebar(show=False)