from tkinter import *
import customtkinter


class CustomButton(customtkinter.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = self

    def on_release(self, event):
        pass
        #self.configure(fg_color="blue", text="Released")

    def on_drag(self, event):
        self.place(x=self.root.winfo_pointerx() - self.root.winfo_rootx() - self.winfo_width() / 2, y=self.root.winfo_pointery() - self.root.winfo_rooty() - self.winfo_height() / 2)
        #self.configure(fg_color="red", text="Dragging")


class CustomCanvas(Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = self

    def on_release(self, event):
        pass
        #self.configure(fg_color="blue", text="Released")

    def on_drag(self, event):
        self.place(x=self.root.winfo_pointerx() - self.root.winfo_rootx() - self.winfo_width() / 2, y=self.root.winfo_pointery() - self.root.winfo_rooty() - self.winfo_height() / 2)
        #self.configure(fg_color="red", text="Dragging")


class TaskConnector:
    def __init__(self, canvas, x, y, x2, y2):
        self.canvas = canvas
        self.line = canvas.create_line(x, y, x2, y2, width=5, fill="#ff335c")
        self.canvas.pack()

    def update_start(self, new_x, new_y):
        x1, y1, x2, y2 = self.canvas.coords(self.line)
        self.canvas.coords(self.line, new_x, new_y, x2, y2)

    def update_end(self, new_x, new_y):
        x1, y1, x2, y2 = self.canvas.coords(self.line)
        self.canvas.coords(self.line, x1, y1, new_x, new_y)


class DraggableTask:
    def __init__(self, canvas, x, y, radius, root, connectors=None):
        self.canvas = canvas
        self.oval = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=root['bg'], outline="#ff335c", width=5)

        self.connections = {
            TaskConnector(self.canvas, 0, 0, 50, 50): "start",
            TaskConnector(self.canvas, 100, 0, 50, 50): "end"
        }

        #self.canvas.tag_bind(self.oval, "<Button-1>", self.on_drag_start)
        self.canvas.tag_bind(self.oval, "<B1-Motion>", lambda event: self.on_drag(event))
        #self.canvas.tag_bind(self.oval, "<ButtonRelease-1>", self.on_drag_stop)

        self.canvas.pack()

    def on_drag(self, event):
        print(event.x, event.y)
        x = event.x - 50
        y = event.y - 50
        self.canvas.coords(self.oval, x + 5, y + 5, x + 95, y + 95)  # Adjust 100 according to your oval size
        self.update_connections()

    def update_connections(self):
        for connection in self.connections:
            self.canvas.tag_raise(self.oval, connection.line)
            if self.connections[connection] == "start":
                connection.update_start(self.get_position()[0] + 50, self.get_position()[1] + 50)
            elif self.connections[connection] == "end":
                connection.update_end(self.get_position()[0] + 50, self.get_position()[1] + 50)

    def get_position(self):
        return self.canvas.coords(self.oval)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")
        self.geometry("300x400")

        # configure window
        self.title("CustomTkinter complex_example.py")

        # Create a canvas object
        c = Canvas(self, bd=0, highlightthickness=0, background=self['bg'])
        c.pack(fill=BOTH, expand=True)

        DraggableTask(c, 50, 50, 50, self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
