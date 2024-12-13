import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def mark_task_as_completed(self, task):
        if task in self.tasks:
            task.mark_as_completed()

    def get_all_tasks(self):
        return list(self.tasks)

    def get_pending_tasks(self):
        pending_tasks = []
        for task in self.tasks:
            if not task.completed:
                pending_tasks.append(task)
        return pending_tasks

    def get_completed_tasks(self):
        completed_tasks = []
        for task in self.tasks:
            if task.completed:
                completed_tasks.append(task)
        return completed_tasks

    def shift_task_around(self, task, position):
        if position >= len(self.tasks) or task not in self.tasks:
            return
        self.tasks.remove(task)
        self.tasks.insert(position, task)

    def get_tasks_owned_by(self, owner):
        rl_task = []
        for t in self.tasks:
            if t.owner == owner:
                rl_task.append(t)
        return rl_task

    def change_owner(self, owner, task):
        if task in self.tasks:
            i = self.tasks.index(task)
            self.tasks[i].owner = owner
