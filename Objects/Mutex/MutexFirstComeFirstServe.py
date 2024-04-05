from Objects.Mutex.MutexBase import MutexBase


class MutexFirstComeFirstServe(MutexBase):
    def __init__(self):
        super().__init__()
        self.algorithm_type = "First Come First Serve"

    def attend(self, task):
        self.attendees.append(task)

    def evaluate(self):
        if self.lock or not self.attendees:
            return

        first_priority_task = self.attendees.pop(0)
        self.lock = True
        self.holder = first_priority_task
        print(f"Mutex locked by {first_priority_task.task_name}")

        first_priority_task.grant_access()

    def release(self, task):
        if task != self.holder:
            return

        print(f"Mutex released by {task.task_name}")
        self.lock = False
        self.holder = None
