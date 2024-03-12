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