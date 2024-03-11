from typing import List


class Task:
    def __init__(self, name: str, activity: str, inputs: List[str], outputs: List[str], cycles: int = 1, priority: int = 0):
        self.name = name
        self.activity = activity
        self.cycles = cycles
        self.priority = priority
        self.inputs = inputs
        self.outputs = outputs

    def __str__(self):
        return f"{self.name} {self.cycles} {self.priority} {self.inputs} {self.outputs}"
