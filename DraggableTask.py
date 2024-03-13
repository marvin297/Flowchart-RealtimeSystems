from GeneralVariables import GeneralVariables


class DraggableTask:
    allow_selection = False
    selectedTasks = 0
    selectedOrigin = None
    selectedTarget = None

    def __init__(self, task_name, activity_name, x, y, radius, task_max_cycles):
        self.oval = GeneralVariables.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=GeneralVariables.root['bg'],
                                       outline=GeneralVariables.task_color, width=2)

        #self.oval = GeneralVariables.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=GeneralVariables.task_color, outline=GeneralVariables.task_color, width=2)
        self.connectors = {}
        self.task_name = task_name
        self.activity_name = activity_name
        self.selected = False

        self.mutexes = []

        # Task cycle
        self.task_current_cycle = 0
        self.task_max_cycles = task_max_cycles

        # Task elements
        self.name_label = GeneralVariables.canvas.create_text(x, y - 20 if self.activity_name != "" else y - 10, text="Task " + self.task_name, fill="white", font=("Montserrat Black", 12))
        if self.activity_name != "":
            self.activity_label = GeneralVariables.canvas.create_text(x, y, text="Activity " + self.activity_name, fill="white", font=("Montserrat Black", 9))
        self.cycle_label = GeneralVariables.canvas.create_text(x, y + 20 if self.activity_name != "" else y + 10, text="Cycle " + str(self.task_current_cycle) + "/" + str(self.task_max_cycles), fill="white", font=("Montserrat Light", 8))

        self.selection_text = GeneralVariables.canvas.create_text(x, y - radius - 20, text="", fill="#00335c", font=("Arial", 12))

        GeneralVariables.canvas.tag_bind(self.oval, "<Button-1>", lambda event: self.clicked(task_name, activity_name))
        GeneralVariables.canvas.tag_bind(self.name_label, "<Button-1>", lambda event: self.clicked(task_name, activity_name))
        if self.activity_name != "":
            GeneralVariables.canvas.tag_bind(self.activity_label, "<Button-1>", lambda event: self.clicked(task_name, activity_name))
        GeneralVariables.canvas.tag_bind(self.cycle_label, "<Button-1>", lambda event: self.clicked(task_name, activity_name))

        GeneralVariables.canvas.tag_bind(self.oval, "<B1-Motion>", lambda event: self.on_drag(event))
        GeneralVariables.canvas.tag_bind(self.name_label, "<B1-Motion>", lambda event: self.on_drag(event))
        if self.activity_name != "":
            GeneralVariables.canvas.tag_bind(self.activity_label, "<B1-Motion>", lambda event: self.on_drag(event))
        GeneralVariables.canvas.tag_bind(self.cycle_label, "<B1-Motion>", lambda event: self.on_drag(event))
        # self.canvas.tag_bind(self.oval, "<ButtonRelease-1>", self.on_drag_stop)

        GeneralVariables.canvas.pack()

    def try_step(self):
        #  If the task is not in the middle of a cycle, then it can start a new cycle
        if self.task_max_cycles > self.task_current_cycle > 0:
            self.task_current_cycle += 1

        # check if the task can start a new cycle
        amount_of_needed_connections_to_start = 0
        amount_of_ready_connections_to_start = 0
        for connection in self.connectors:
            if self.connectors[connection] == "end":
                amount_of_needed_connections_to_start += 1
                if connection.semaphore_value > 0 and self.task_current_cycle == 0 and connection.last_change != GeneralVariables.step_number: # check time if semaphore was changed this step
                    amount_of_ready_connections_to_start += 1

        self.attend(amount_of_needed_connections_to_start, amount_of_ready_connections_to_start)

        self._end_cycle()

        self.update_status_text()

    def _start_cycle(self):
        for connection in self.connectors:
            if self.connectors[connection] == "end" and connection.semaphore_value > 0:
                self.task_current_cycle = 1
                connection.decrement_semaphore(GeneralVariables.step_number)

        self.update_status_text()

    def attend(self, amount_of_needed_connections_to_start, amount_of_ready_connections_to_start):
        if amount_of_needed_connections_to_start == amount_of_ready_connections_to_start and self.task_current_cycle == 0 and amount_of_needed_connections_to_start > 0:
            if len(self.mutexes) > 0:
                for mutex in self.mutexes:
                    mutex.attend(attendee=self)
            else:
                self._start_cycle()

    def grant_access(self):
        print("Access granted to", self.task_name, self.activity_name)
        self._start_cycle()

    def add_mutex(self, mutex):
        print("Added mutex " + mutex.name + " to task " + self.task_name + self.activity_name)
        self.mutexes.append(mutex)

    def _end_cycle(self):
        # If the task is done with the current cycle, it increments the semaphore of the end connections
        if self.task_current_cycle == self.task_max_cycles:
            print("ENDING CYCLE " + self.task_name + self.activity_name + " " + str(self.task_current_cycle) + "/" + str(self.task_max_cycles))
            for connection in self.connectors:
                if self.connectors[connection] == "start":
                    connection.increment_semaphore(GeneralVariables.step_number)  # TODO: MOVE ALL THESE VARIABLES INSIDE THE SEMAPHORE OBJECT
            self.task_current_cycle = 0
            if len(self.mutexes) > 0:
                for mutex in self.mutexes:
                    mutex.release()

    def on_drag(self, event):
        if DraggableTask.allow_selection:
            return

        x = event.x - 50
        y = event.y - 50
        GeneralVariables.canvas.coords(self.oval, x, y, x + 100, y + 100)  # Adjust 100 according to your oval size
        GeneralVariables.canvas.coords(self.name_label, x + 50, y + 50 - 20 if self.activity_name != "" else y + 50 - 10)
        if self.activity_name != "":
            GeneralVariables.canvas.coords(self.activity_label, x + 50, y + 50)
        GeneralVariables.canvas.coords(self.cycle_label, x + 50, y + 50 + 20 if self.activity_name != "" else y + 50 + 10)

        GeneralVariables.canvas.coords(self.selection_text, x + 50, y - 20)
        self.update_connections()

        for mutex in self.mutexes:
            mutex.update_visuals()

    def update_status_text(self):
        GeneralVariables.canvas.itemconfig(self.cycle_label, text="Cycle " + str(self.task_current_cycle) + "/" + str(self.task_max_cycles))

    def update_connections(self):
        for connection in self.connectors:
            GeneralVariables.canvas.tag_raise(self.oval, connection.line)
            GeneralVariables.canvas.tag_raise(self.name_label, self.oval)
            if self.activity_name != "":
                GeneralVariables.canvas.tag_raise(self.activity_label, self.oval)
            GeneralVariables.canvas.tag_raise(self.cycle_label)
            if self.connectors[connection] == "start":
                connection.update_start(self.get_position()[0] + 50, self.get_position()[1] + 50)
                connection.update_end(0, 0, True)

            elif self.connectors[connection] == "end":
                end_x = self.get_position()[0] + 50
                end_y = self.get_position()[1] + 50
                connection.update_end(end_x, end_y)

    def get_position(self):
        return GeneralVariables.canvas.coords(self.oval)

    def set_connectors(self, connectors):
        self.connectors = connectors

    def add_connector(self, connector, position):
        self.connectors[connector] = position

    def clicked(self, task_name, activity_name):
        if DraggableTask.selectedTasks > 1 and not self.selected or not DraggableTask.allow_selection:
            return

        print("Clicked on task: " + task_name + activity_name)
        self.selected = not self.selected
        if self.selected:
            if DraggableTask.selectedOrigin is None:
                DraggableTask.selectedOrigin = self
                GeneralVariables.canvas.itemconfig(self.selection_text, text="Origin")
            else:
                DraggableTask.selectedTarget = self
                GeneralVariables.canvas.itemconfig(self.selection_text, text="Target")

            GeneralVariables.canvas.itemconfig(self.oval, outline="#00335c")
            DraggableTask.selectedTasks += 1
        else:
            if DraggableTask.selectedOrigin is not None:
                if DraggableTask.selectedOrigin.task_name + DraggableTask.selectedOrigin.activity_name == task_name + activity_name:
                    DraggableTask.selectedOrigin = None
            else:
                DraggableTask.selectedTarget = None

            GeneralVariables.canvas.itemconfig(self.selection_text, text="")
            GeneralVariables.canvas.itemconfig(self.oval, outline=GeneralVariables.task_color)
            DraggableTask.selectedTasks -= 1

        print(DraggableTask.selectedTasks)

    @staticmethod
    def switch_selection():
        DraggableTask.allow_selection = not DraggableTask.allow_selection

        if not DraggableTask.allow_selection:
            if DraggableTask.selectedOrigin is not None:
                GeneralVariables.canvas.itemconfig(DraggableTask.selectedOrigin.selection_text, text="")
                GeneralVariables.canvas.itemconfig(DraggableTask.selectedOrigin.oval, outline=GeneralVariables.task_color)
                DraggableTask.selectedOrigin.selected = False
                DraggableTask.selectedOrigin = None

            if DraggableTask.selectedTarget is not None:
                GeneralVariables.canvas.itemconfig(DraggableTask.selectedTarget.selection_text, text="")
                GeneralVariables.canvas.itemconfig(DraggableTask.selectedTarget.oval, outline=GeneralVariables.task_color)
                DraggableTask.selectedTarget.selected = False
                DraggableTask.selectedTarget = None

            DraggableTask.selectedTasks = 0
