class DraggableTask:
    def __init__(self, canvas, task_name, activity_name, x, y, radius, root):
        self.canvas = canvas
        self.oval = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=root['bg'],
                                       outline="#ff335c", width=5)
        self.connectors = {}
        self.task_name = task_name
        self.activity_name = activity_name

        self.name = canvas.create_text(x, y, text=task_name + activity_name, fill="#ff335c", font=("Arial", 12))

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