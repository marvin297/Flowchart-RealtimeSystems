# -*- coding: utf-8 -*-
# Import necessary modules
from Objects.Connection.ConnectionBase import ConnectionBase
from General.Configuration import Configuration


class ConnectionTask(ConnectionBase):
    """
    A class representing a connector between tasks in a workflow.

    This class creates a line on a canvas that connects two tasks and represents
    a dependency or relationship between them. It displays a semaphore value and
    allows for visual customization based on the type of connection (regular or
    activity). The connector can be selected and updated dynamically as the tasks
    are moved or modified.
    """

    def __init__(self, name, semaphore_value=0, offset=0):
        """
        Initialize a new instance of the TaskConnector class.

        Args:
            name (str): The name of the connector.
            semaphore_value (int, optional): The initial semaphore value. Defaults to 0.
            offset (int, optional): The offset value for positioning the connector. Defaults to 0.
        """
        arrow_color = Configuration.arrow_color
        arrow_color_selected = Configuration.arrow_color_selected
        arrow_style = (25, 25, 10)
        line_width = 5

        super().__init__(name, arrow_color, arrow_color_selected, arrow_style, line_width, semaphore_value, offset)
