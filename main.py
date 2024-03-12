from tkinter import *
import customtkinter
from FileOperations import browseFiles, saveFile
from DraggableTask import DraggableTask
from CTkMenuBar import *
from GeneralVariables import GeneralVariables


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")
        self.geometry("800x800")

        # configure window
        self.title("Flowchart Editor")

        # Create a canvas object
        canvas = Canvas(self, bd=0, highlightthickness=0, background=self['bg'])
        canvas.pack(fill=BOTH, expand=True)

        menubar = CTkTitleMenu(master=self)
        button_file_menu = menubar.add_cascade("File")
        button_edit_menu = menubar.add_cascade("Edit")
        button_run_menu = menubar.add_cascade("Run")

        filemenu = CustomDropdownMenu(widget=button_file_menu, border_color="")
        filemenu.add_option(option="Save as xslx", command=lambda: saveFile())
        filemenu.add_option(option="Load from xslx", command=lambda: browseFiles(canvas, self))
        filemenu.add_separator()
        filemenu.add_option(option="Clear chart", command=lambda: App.clear_canvas(canvas))
        filemenu.add_option(option="Exit to desktop", command=self.quit)

        editmenu = CustomDropdownMenu(widget=button_edit_menu, border_color="")
        editmenu.add_option(option="Edit tasks", command=lambda: DraggableTask.switch_selection(canvas))
        editmenu.add_option(option="Add task", command=lambda: print("NOT IMPLEMENTED YET"))
        editmenu.add_option(option="Add connection", command=lambda: print("NOT IMPLEMENTED YET"))

        runmenu = CustomDropdownMenu(widget=button_run_menu, border_color="")
        runmenu.add_option(option="Next step", command=App.step)

    @staticmethod
    def clear_canvas(canvas):
        GeneralVariables.task_objects.clear()
        GeneralVariables.connector_objects.clear()
        canvas.delete("all")

    @staticmethod
    def step():
        from time import time
        start = time()
        for task in GeneralVariables.task_objects:
            task.try_step(start)


if __name__ == "__main__":
    app = App()
    app.mainloop()
