

class GeneralVariables:
    task_objects = []
    connector_objects = []
    mutex_objects = {}
    step_number = 0
    canvas = None
    root = None

    font_black = None
    font_light = None

    arrow_color = "#767676"
    activity_arrow_color = "#029cff"
    mutex_color = "#464646"

    task_color = "#029cff"

    @staticmethod
    def clear_general_variables():
        GeneralVariables.task_objects.clear()
        GeneralVariables.connector_objects.clear()
        GeneralVariables.mutex_objects = {}
        GeneralVariables.step_number = 0
