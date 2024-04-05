from Objects.Mutex.MutexBase import MutexBase


class MutexPriorityInversion(MutexBase):
    def __init__(self):
        super().__init__()
        self.algorithm_type = "Priority Inversion"

    def attend(self, task):
        # Add a task to the attendees list and sort descending by priority
        self.attendees.append(task)
        self.attendees.sort(key=lambda x: x.priority, reverse=True)

        # Check for the priority inversion
        if self.lock and self.holder.priority < self.attendees[0].priority:
            self.holder.elevated_priority = self.attendees[0].priority
            print(
                f"Priority inheritance: {self.holder.task_name}'s priority elevated to {self.holder.elevated_priority}")

    def evaluate(self):
        if self.lock or not self.attendees:
            return
        highest_priority_task = self.attendees.pop(0)
        self.lock = True
        self.holder = highest_priority_task
        print("Mutex locked by " + highest_priority_task.task_name + highest_priority_task.activity_name)
        highest_priority_task.grant_access()

    def release(self, task):
        print("Mutex released")
        if task != self.holder:
            return

        print("Mutex released by " + task.task_name + task.activity_name)
        self.lock = False
        self.holder = None

        # Restore original priority back if elevated
        if hasattr(task, 'elevated_priority'):
            task.priority = task.original_priority
            del task.elevated_priority
