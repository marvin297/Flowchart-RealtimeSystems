from tkinter import *
import customtkinter
from FileOperations import browse_files, save_file
from DraggableTask import DraggableTask
from CTkMenuBar import *
from GeneralVariables import GeneralVariables
from TaskConnector import TaskConnector


class App(customtkinter.CTk):
    sidebar = None

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
        editmenu.add_option(option="Edit mode", command=lambda: DraggableTask.switch_selection())
        editmenu.add_option(option="Add new task", command=lambda: App.add_task())

        runmenu = CustomDropdownMenu(widget=button_run_menu, border_color="")
        runmenu.add_option(option="Next step", command=App.step)

        self.create_sidebar()

    def create_sidebar(self):
        GeneralVariables.sidebar = Frame(self, width=300, bd=0, bg="#303030")
        GeneralVariables.sidebar.place(relx=0, rely=0, relheight=1, x=-300)

        GeneralVariables.sidebar_task_input = StringVar()
        GeneralVariables.sidebar_activity_input = StringVar()
        GeneralVariables.sidebar_cycles_input = IntVar()

        sidebar_title = Label(GeneralVariables.sidebar, text="Editor", font=("Montserrat Light", 20), bg="#2A2A2A", fg="white",
                              width=15)
        sidebar_title.pack(side=TOP, anchor=N, padx=0, pady=10)
        App.create_edit_task_container()
        App.create_connection_container()
        App.create_mutex_container()

    @staticmethod
    def create_edit_task_container():
        GeneralVariables.sidebar_edit_task_container = Frame(GeneralVariables.sidebar, bd=0, bg="#303030")

        task_name_frame = Frame(GeneralVariables.sidebar_edit_task_container, bd=0, bg="#2A2A2A", height=30)
        task_name_frame.place(relx=0, rely=0, x=15, y=100)
        task_name_title = Label(task_name_frame, text="Task name", font=("Montserrat Light", 10), bg="#2A2A2A",
                                fg="white", width=15)
        task_name_title.pack(side=TOP, anchor=N, padx=0, pady=5)
        task_name_input = Entry(task_name_frame, font=("Montserrat Light", 10), bd=0, bg="#303030", fg="white",
                                insertbackground="white", width=20, textvariable=GeneralVariables.sidebar_task_input,
                                borderwidth=10, relief="flat")
        task_name_input.pack(side=TOP, anchor=N, padx=15, pady=15)

        activity_name_frame = Frame(GeneralVariables.sidebar_edit_task_container, bd=0, bg="#2A2A2A", height=30)
        activity_name_frame.place(relx=0, rely=0, x=15, y=210)
        activity_name_title = Label(activity_name_frame, text="Activity name", font=("Montserrat Light", 10),
                                    bg="#2A2A2A",
                                    fg="white", width=15)
        activity_name_title.pack(side=TOP, anchor=N, padx=0, pady=5)
        activity_name_input = Entry(activity_name_frame, font=("Montserrat Light", 10), bd=0, bg="#303030", fg="white",
                                    insertbackground="white", width=20,
                                    textvariable=GeneralVariables.sidebar_activity_input, borderwidth=10, relief="flat")
        activity_name_input.pack(side=TOP, anchor=N, padx=15, pady=15)

        cycles_frame = Frame(GeneralVariables.sidebar_edit_task_container, bd=0, bg="#2A2A2A", height=30)
        cycles_frame.place(relx=0, rely=0, x=15, y=320)
        cycles_title = Label(cycles_frame, text="Amount of cycles", font=("Montserrat Light", 10),
                             bg="#2A2A2A",
                             fg="white", width=15)
        cycles_title.pack(side=TOP, anchor=N, padx=0, pady=5)
        cycles_input = Entry(cycles_frame, font=("Montserrat Light", 10), bd=0, bg="#303030", fg="white",
                             insertbackground="white", width=20, textvariable=GeneralVariables.sidebar_cycles_input,
                             borderwidth=10,
                             relief="flat")
        cycles_input.pack(side=TOP, anchor=N, padx=15, pady=15)

        # Create a frame to simulate the button appearance
        button_confirm_task_frame = Frame(GeneralVariables.sidebar_edit_task_container, bg="#303030", bd=1, relief="solid",
                             highlightbackground=GeneralVariables.task_color,
                             highlightthickness=1)
        button_confirm_task_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_confirm_task_frame, text="CONFIRM SETTINGS", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: GeneralVariables.confirm_task_change(),
                              width=20)
        button_label.pack()

    @staticmethod
    def create_connection_container():
        GeneralVariables.sidebar_add_connection_container = Frame(GeneralVariables.sidebar, bd=0, bg="#303030")

        # Create a frame to simulate the button appearance
        button_add_connection_frame = Frame(GeneralVariables.sidebar_add_connection_container, bg="#303030", bd=1, relief="solid",
                             highlightbackground=GeneralVariables.task_color,
                             highlightthickness=1)
        button_add_connection_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_add_connection_frame, text="ADD CONNECTION", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: App.add_connection(),
                              width=20)
        button_label.pack()

    @staticmethod
    def create_mutex_container():
        GeneralVariables.sidebar_add_mutex_container = Frame(GeneralVariables.sidebar, bd=0, bg="#303030")

        # Create a frame to simulate the button appearance
        button_add_connection_frame = Frame(GeneralVariables.sidebar_add_mutex_container, bg="#303030", bd=1,
                                            relief="solid",
                                            highlightbackground=GeneralVariables.task_color,
                                            highlightthickness=1)
        button_add_connection_frame.pack(side=BOTTOM, anchor=N, padx=10, pady=10)

        # Create a label inside the frame to display button text
        button_label = Button(button_add_connection_frame, text="ADD MUTEX", fg="white", bg="#303030", bd=0,
                              font=("Montserrat Light", 12), command=lambda: print("NOT YET IMPLEMENTED"),
                              width=20)
        button_label.pack()

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
    def add_task():
        print("Add task")
        new_task = DraggableTask("?", "?", GeneralVariables.root.winfo_width() / 2, GeneralVariables.root.winfo_height() / 2, 50, 1)
        GeneralVariables.task_objects.append(new_task)

    @staticmethod
    def add_connection():  # TODO: UPDATE TO NEW EDIT SYSTEM
        print("Add connection")
        origin_task = [task_object for task_object, position in GeneralVariables.selected_tasks.items() if str(position) == str(1)][0]
        target_task = [task_object for task_object, position in GeneralVariables.selected_tasks.items() if str(position) == str(2)][0]

        activity_connection = False
        if origin_task.task_name == target_task.task_name:
            activity_connection = True

        new_offset = 0
        for connection in origin_task.connectors:
            if connection in target_task.connectors:
                connection.offset = 50
                new_offset = -50

        new_connection = TaskConnector("?", 0, activity_connection, new_offset)
        origin_task.add_connector(new_connection, "start")
        target_task.add_connector(new_connection, "end")

        origin_task.update_connections()
        target_task.update_connections()

        start_task_name = origin_task.task_name + origin_task.activity_name
        connector_name = new_connection.name
        end_task_name = target_task.task_name + target_task.activity_name
        initial_value = 0

        GeneralVariables.connector_objects.append([start_task_name, connector_name, end_task_name, initial_value])


if __name__ == "__main__":
    app = App()
    app.mainloop()
