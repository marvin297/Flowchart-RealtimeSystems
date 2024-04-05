from Objects.Mutex.MutexBase import MutexBase


class MutexPriorityCeiling(MutexBase):
    def __init__(self):
        super().__init__()
        self.algorithm_type = "Priority Ceiling"
        self.ceiling_priority = None  # Initialize ceiling priority

    def update_ceiling_priority(self):
        if self.connected_tasks:
            self.ceiling_priority = max(task.priority for task in self.connected_tasks)
        else:
            self.ceiling_priority = None

    def attend(self, task):
        # Update ceiling priority when a new task attends
        self.update_ceiling_priority()

        self.attendees.append(task)
        self.attendees.sort(key=lambda x: x.priority, reverse=True)

        if self.lock and self.holder.priority < task.priority and self.ceiling_priority < task.priority:
            print(f"Task {task.task_name} blocked due to priority ceiling protocol")

    def evaluate(self):
        if self.lock or not self.attendees or (self.ceiling_priority is not None and self.attendees[0].priority > self.ceiling_priority):
            return

        highest_priority_task = self.attendees.pop(0)
        self.lock = True
        self.holder = highest_priority_task
        print(f"Mutex locked by {highest_priority_task.task_name}")

        highest_priority_task.grant_access()

    def release(self, task):
        if task != self.holder:
            return

        print(f"Mutex released by {task.task_name}")
        self.lock = False
        self.holder = None

        # Restore original priority back if elevated
        if hasattr(task, 'elevated_priority'):
            task.priority = task.original_priority
            del task.elevated_priority

        # Update ceiling priority after a task is released
        self.update_ceiling_priority()

