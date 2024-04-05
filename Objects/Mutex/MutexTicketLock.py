from Objects.Mutex.MutexBase import MutexBase

class MutexTicketLock(MutexBase):
    def __init__(self):
        super().__init__()
        self.algorithm_type = "Ticket Lock"
        self.ticket_counter = 0  # Initialize the ticket counter
        self.current_ticket = 0  # The ticket currently being served

    def attend(self, task):
        task.ticket = self.ticket_counter
        self.ticket_counter += 1
        self.attendees.append(task)

        print(f"Task {task.task_name} received ticket {task.ticket}")

    def evaluate(self):
        if self.lock or not self.attendees:
            return

        # Find the task with the current ticket
        for task in self.attendees:
            if task.ticket == self.current_ticket:
                self.attendees.remove(task)
                self.lock = True
                self.holder = task
                print(f"Mutex locked by {task.task_name} with ticket {task.ticket}")
                self.current_ticket += 1
                task.grant_access()
                break

    def release(self, task):
        if task != self.holder:
            return

        print(f"Mutex released by {task.task_name} with ticket {task.ticket}")
        self.lock = False
        self.holder = None

        # Continue with the next ticket
        self.evaluate()