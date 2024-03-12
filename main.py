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

        load_file_btn = customtkinter.CTkButton(c, text="Load file", command=lambda: browseFiles(c, self)).pack()
        store_file_btn = customtkinter.CTkButton(c, text="Store file", command=saveFile).pack()
        next_step_btn = customtkinter.CTkButton(c, text="Next step", command=lambda: print("Stepping...")).pack()
        edit_btn = customtkinter.CTkButton(c, text="Edit", command=lambda: DraggableTask.switch_selection(c)).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
