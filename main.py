from tkinter import *
import customtkinter
from FileOperations import browseFiles, saveFile
from DraggableTask import DraggableTask

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")
        self.geometry("800x800")

        # configure window
        self.title("Flowchart Editor")

        # Create a canvas object
        c = Canvas(self, bd=0, highlightthickness=0, background=self['bg'])
        c.pack(fill=BOTH, expand=True)

        # creates menubar
        menubar = Menu(self, relief=FLAT, bd=0, background='green')
        # Sets menubar background color and active select but does not remove 3d  effect/padding
        menubar.config(bg="BLACK", fg='white', activeborderwidth=0, relief=FLAT)

        filemenu = Menu(menubar, tearoff=0, relief=FLAT)

        filemenu.config(bg="WHITE")
        filemenu.add_command(label="Save as xlsx", command=saveFile)
        filemenu.add_command(label="Load from xlsx", command=lambda: browseFiles(c, self))
        filemenu.add_separator()
        filemenu.add_command(label="Exit to desktop", command=self.quit)

        # Attach filemenu to menubar
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0, relief=FLAT)
        editmenu.add_command(label="Edit Tasks", command=lambda: DraggableTask.switch_selection(c))

        menubar.add_cascade(label="Edit", menu=editmenu)

        self.config(menu=menubar)



        # load_file_btn = customtkinter.CTkButton(c, text="Load file", command=lambda: browseFiles(c, self)).pack()
        # store_file_btn = customtkinter.CTkButton(c, text="Store file", command=saveFile).pack()
        next_step_btn = customtkinter.CTkButton(c, text="Next step", command=lambda: print("Stepping...")).pack()
        # edit_btn = customtkinter.CTkButton(c, text="Edit", command=lambda: DraggableTask.switch_selection(c)).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
