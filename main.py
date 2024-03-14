from tkinter import *
import customtkinter
from FileOperations import browse_files, save_file
from DraggableTask import DraggableTask
from CTkMenuBar import *
from GeneralVariables import GeneralVariables
from TaskConnector import TaskConnector


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        GeneralVariables.root = self

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")
        self.geometry("800x800")

        # configure window
        self.title("Flowchart Editor")

        # fonts
        from tkextrafont import Font
        GeneralVariables.font_black = Font(file="fonts/Montserrat-Black.ttf", family="Montserrat")
        GeneralVariables.font_light_normal = Font(file="fonts/Montserrat-Light.ttf", family="Montserrat")

        # Create a canvas object
        canvas = Canvas(self, bd=0, highlightthickness=0, background=self['bg'])
        canvas.pack(fill=BOTH, expand=True)
        GeneralVariables.canvas = canvas

        menubar = CTkTitleMenu(master=self)
        button_file_menu = menubar.add_cascade("File")
        button_edit_menu = menubar.add_cascade("Edit")
        button_run_menu = menubar.add_cascade("Run")

        filemenu = CustomDropdownMenu(widget=button_file_menu, border_color="")
        filemenu.add_option(option="Save as xslx", command=lambda: save_file())
        filemenu.add_option(option="Load from xslx", command=lambda: browse_files())
        filemenu.add_separator()
        filemenu.add_option(option="Clear chart", command=lambda: App.clear_canvas())
        filemenu.add_option(option="Exit to desktop", command=self.quit)

        editmenu = CustomDropdownMenu(widget=button_edit_menu, border_color="")
        editmenu.add_option(option="Edit tasks", command=lambda: print("NOT IMPLEMENTED YET"))
        editmenu.add_option(option="Add new task", command=lambda: App.add_task("?"))
        editmenu.add_option(option="Add new task 2", command=lambda: App.add_task("??"))
        editmenu.add_separator()
        editmenu.add_option(option="Connection mode", command=lambda: DraggableTask.switch_selection())
        editmenu.add_option(option="Add new connection (Requires connection mode)", command=lambda: App.add_connection())
        editmenu.add_separator()
        editmenu.add_option(option="Mutex mode", command=lambda: print("NOT IMPLEMENTED YET"))
        editmenu.add_option(option="Add new mutex (Requires mutex mode)", command=lambda: print("NOT IMPLEMENTED YET"))

        runmenu = CustomDropdownMenu(widget=button_run_menu, border_color="")
        runmenu.add_option(option="Next step", command=App.step)

    @staticmethod
    def clear_canvas():
        GeneralVariables.clear_general_variables()
        GeneralVariables.canvas.delete("all")

    @staticmethod
    def step():
        print("Step")
        GeneralVariables.step_number += 1
        for task in GeneralVariables.task_objects:
            task.try_step()

        for mutex in GeneralVariables.mutex_objects:
            GeneralVariables.mutex_objects[mutex].evaluate()
            GeneralVariables.mutex_objects[mutex].update_visuals()

    @staticmethod
    def add_task(name):
        print("Add task")
        new_task = DraggableTask(name, "", 50, 50, 50, 1)
        GeneralVariables.task_objects.append(new_task)

    @staticmethod
    def add_connection():
        print("Add connection")
        if not DraggableTask.allow_selection or DraggableTask.selectedOrigin is None or DraggableTask.selectedTarget is None:
            return

        activity_connection = False
        if DraggableTask.selectedOrigin.task_name == DraggableTask.selectedTarget.task_name:
            activity_connection = True

        new_offset = 0
        for connection in DraggableTask.selectedOrigin.connectors:
            if connection in DraggableTask.selectedTarget.connectors:
                connection.offset = 50
                new_offset = -50

        new_connection = TaskConnector("?", 0, activity_connection, new_offset)
        DraggableTask.selectedOrigin.add_connector(new_connection, "start")
        DraggableTask.selectedTarget.add_connector(new_connection, "end")

        DraggableTask.selectedOrigin.update_connections()
        DraggableTask.selectedTarget.update_connections()

        start_task_name = DraggableTask.selectedOrigin.task_name + DraggableTask.selectedOrigin.activity_name
        connector_name = new_connection.name
        end_task_name = DraggableTask.selectedTarget.task_name + DraggableTask.selectedTarget.activity_name
        initial_value = 0

        GeneralVariables.connector_objects.append([start_task_name, connector_name, end_task_name, initial_value])


if __name__ == "__main__":
    app = App()
    app.mainloop()
