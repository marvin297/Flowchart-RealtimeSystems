### Flowchart-RealtimeSystems

This project creates a flow chart visualization using Python and the Tkinter GUI toolkit. It allows users to create and manage tasks represented as oval shapes on a canvas. Tasks can be connected to each other, participate in mutexes, and display relevant information such as task name, activity name, and current cycle.

## Features

- Create draggable task ovals on a canvas
- Display task name, activity name, and current cycle
- Connect tasks using connectors
- Manage task dependencies and relationships
- Implement mutex locks for task synchronization
- Customize task and connector appearance
- Support for light and dark themes using CustomTkinter

## Supported mutex types

- Priority Ceiling
- Priority Inversion
- Ticket Lock
- First Come First Serve

## Requirements

- Python 3.x
- Tkinter
- CustomTkinter
- CTkMenuBar

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/draggable-task-visualization.git
   ```

2. Install the required dependencies:

   ```
   pip install customtkinter
   pip install CTkMenuBar
   pip install tkextrafont
   ```

## Usage

1. Run the main script:

   ```
   python main.py
   ```

2. The application window will open, displaying the task visualization canvas.

3. Use the GUI controls to create tasks, establish connections, and manage mutexes.

4. Drag tasks around the canvas to rearrange their positions.

5. Customize task and connector appearance using the provided options.

## Getting Started

### Creating a template
To create a template for creating your own diagram, you need to execute the following steps:
1. Run the software
2. In the menu-bar click on `file`
3. Click on `Save as xslx`
4. Save the template at your desired path and give it a name
5. Click on the `Save` button to store the template

### Loading an example file
We have provided some demo files for exploring our Flowchart editor and visualizer.
To load a file from disk, you need to:
1. Run the software
2. In the menu-bar locate and click on `file`
3. Click on `Load from xslx`
4. A system prompt will open and you can locate a file you want to open. _To open the examples, you need to locate this project's root (or download the *above* provided xslx-files seperately). All example files are located there:_
   * ring.xslx
   * ring2.xslx
   * test.xslx
   * data2.xslx
   * data3.xslx
   * ... (see repository root)
6. Click on `Load`

### Starting a simulation
To start the simulation it is *REQUIRED* to load a file beforehand. (see section above)
Also ensure that you are not in EDIT mode (disabled by default after each restart of the software).
On the menu-bar locate and click on `Run`. You can now either choose manual mode by clicking `Next step`, which simulates a single clock input and thus advances the system by one cycle *OR* you can use the "Simulation Feature":
1. Click on `Hide/Show Simulation Sidebar`.
2. Now the simulation menu should show up at the right side of the window.
3. Drag the slider with your mouse cursor to a desired delay value between cycles (left click).
4. Press the `Start` button to begin the simulation
5. To Halt the simulation press the `Stop` button
6. To resume the simulation, just press `Start` again

You can reload the file at any time by locating `File` in the menu bar and clicking on `Reload file`.

### Edit a file
To edit a file, be sure to hide the simulation bar from the left side of the window. If it is still present, locate `Run` in the menu bar and click on `Hide/Show Simulation Sidebar`. Otherwise the edit mode is not available.

1. Locate `Edit` on the menu-bar and click on it.
2. Click on ONE task, it is now highlighted in dark blue. You can now adjust the following parameters:
   * Task Name
   * Activity Name
   * Amount of cycles the task needs for completion
3. If you click on MORE THAN ONE task, you can either set a connection (including semaphore) or a mutex. YOu can select multiple tasks by clicking on them. To reverse the direction of aconnection you need to select the sourcefirst and then the destination task.

To add a new task, you need to click on `Edit` > `Add new task`. By dragging the task with your mouse, you can move the task to a preferred place. If this doesn't work and the task just gets highlighted dark-blue, be sure to deselect `Edit` > `Edit mode` in the menu-bar.

**!Caution!**: Remember to save your new flowchart that you just created/edited:
1. In the menu-bar click on `File`
2. Click on `Save as xslx`
3. Save the file at your desired path and give it a meaningful name <sub>:)</sub>
4. Click on the `Save` button to store the file


## Configuration

The `Configuration` class in `Configuration.py` contains various settings and references used throughout the project. You can modify these settings to customize the behavior and appearance of the application.

## Q&A
### I cannot get the project to start
Try installing all required libraries if any are missing.
If none of this helps, ensure that your OS is supported. Currently only Windows 10/11 is supported.

### I want to modify the source code
We used PyCharm by Jetbrains for developing this software. Also Visual Studio Code with the required plugins will work certainly.


## License

This project is licensed under the [MIT License](LICENSE).
