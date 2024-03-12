from tkinter import *
import customtkinter
from FileOperations import browseFiles, saveFile
from DraggableTask import DraggableTask
from CTkMenuBar import *

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

        menubar = CTkTitleMenu(master=self)
        buttonFileMenu = menubar.add_cascade("File")
        buttonEditMenu = menubar.add_cascade("Edit")
        buttonRunMenu = menubar.add_cascade("Run")

        filemenu = CustomDropdownMenu(widget=buttonFileMenu)
        filemenu.add_option(option="Save as xslx", command=lambda: saveFile())
        filemenu.add_option(option="Load from xslx", command=lambda: browseFiles(c, self))
        filemenu.add_separator()
        filemenu.add_option(option="Exit to Desktop", command=self.quit)

        editmenu = CustomDropdownMenu(widget=buttonEditMenu)
        editmenu.add_option(option="Edit Tasks", command=lambda: DraggableTask.switch_selection(c))

        runmenu = CustomDropdownMenu(widget=buttonRunMenu)
        runmenu.add_option(option="Next Step", command=lambda: print("Stepping..."))


if __name__ == "__main__":
    app = App()
    app.mainloop()
