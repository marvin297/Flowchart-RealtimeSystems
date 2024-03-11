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

def on_drag(event, canvas, inner_circle, outer_circle, line):
    print('You clicked on the oval')
    print(event.x, event.y)
    x = event.x - 50
    y = event.y - 50
    canvas.coords(inner_circle, x + 5, y + 5, x + 95, y + 95)  # Adjust 100 according to your oval size
    canvas.tag_raise(inner_circle, outer_circle)
    canvas.tag_raise(outer_circle, line)
    canvas.coords(outer_circle, x, y, x + 100, y + 100)  # Adjust 100 according to your oval size

    canvas.coords(line, 0, 0, event.x, event.y)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")
        self.geometry("300x400")

        # configure window
        self.title("CustomTkinter complex_example.py")

        button = CustomButton(master=self, text="Click me!")

        button.place(relx=0.5, rely=0.5, anchor=CENTER)

        # bind button
        # button.bind("<Button-1>", button_event)
        button.bind("<B1-Motion>", button.on_drag)
        button.bind("<ButtonRelease-1>", button.on_release)
        button.pack()

        # Create a canvas object
        c = Canvas(self, bd=0, highlightthickness=0, background=self['bg'])
        c.pack(fill=BOTH, expand=True)

        line = c.create_line(0, 0, 50, 50, width=5, fill="#ff335c")
        # Draw an Oval in the canvas
        outer_circle = c.create_oval(0, 0, 100, 100, fill="#ff335c")
        inner_circle = c.create_oval(5, 5, 95, 95, fill=self['bg'])

        # c.bind("<B1-Motion>", c.on_drag)
        # c.bind("<ButtonRelease-1>", c.on_release)
        c.pack()

        c.tag_bind(inner_circle, '<B1-Motion>', lambda event: on_drag(event, c, inner_circle, outer_circle, line))

if __name__ == "__main__":
    app = App()
    app.mainloop()
