class GeneralVariables:
    task_objects = []
    connector_objects = []
    mutex_objects = {}
    step_number = 0
    canvas = None
    root = None

    @staticmethod
    def clear_general_variables():
        GeneralVariables.task_objects.clear()
        GeneralVariables.connector_objects.clear()
        GeneralVariables.mutex_objects = {}
        GeneralVariables.step_number = 0