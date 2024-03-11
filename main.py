from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.geometry("300x400")

class CustomButton(customtkinter.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def on_release(self, event):
        pass
        #self.configure(fg_color="blue", text="Released")

    def on_drag(self, event):
        self.place(x=root.winfo_pointerx() - root.winfo_rootx() - self.winfo_width() / 2, y=root.winfo_pointery() - root.winfo_rooty() - self.winfo_height() / 2)
        #self.configure(fg_color="red", text="Dragging")

class CustomCanvas(Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def on_release(self, event):
        pass
        #self.configure(fg_color="blue", text="Released")

    def on_drag(self, event):
        self.place(x=root.winfo_pointerx() - root.winfo_rootx() - self.winfo_width() / 2, y=root.winfo_pointery() - root.winfo_rooty() - self.winfo_height() / 2)
        #self.configure(fg_color="red", text="Dragging")


button = CustomButton(master=root, text="Click me!")

button.place(relx=0.5, rely=0.5, anchor=CENTER)


# bind button
# button.bind("<Button-1>", button_event)
button.bind("<B1-Motion>", button.on_drag)
button.bind("<ButtonRelease-1>", button.on_release)
button.pack()

#Create a canvas object
c = Canvas(root, bd=0, highlightthickness=0, background=root['bg'])
c.pack(fill=BOTH, expand=True)

#Draw an Oval in the canvas
outer_circle = c.create_oval(0,0,100,100, fill="red")
inner_circle = c.create_oval(5,5,95,95, fill="blue")

line = c.create_line(0, 0, 50, 50, width=5, fill="white")

#c.bind("<B1-Motion>", c.on_drag)
#c.bind("<ButtonRelease-1>", c.on_release)
c.pack()

def on_drag(event, inner_circle, outer_circle, line):
    print('You clicked on the oval')
    print(event.x, event.y)
    x = event.x - 50
    y = event.y - 50
    c.coords(inner_circle, x + 5, y + 5, x + 95, y + 95)  # Adjust 100 according to your oval size
    c.tag_raise(inner_circle, outer_circle)
    c.tag_raise(outer_circle, line)
    c.coords(outer_circle, x, y, x + 100, y + 100)  # Adjust 100 according to your oval size

    c.coords(line, 0, 0, event.x, event.y)


c.tag_bind(inner_circle, '<B1-Motion>', lambda event: on_drag(event, inner_circle, outer_circle, line))

root.mainloop()