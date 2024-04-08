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

## Configuration

The `Configuration` class in `Configuration.py` contains various settings and references used throughout the project. You can modify these settings to customize the behavior and appearance of the application.

## License

This project is licensed under the [MIT License](LICENSE).
