import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def addTask(self, task):
        self.tasks.append(task)

    def removeTask(self, task):
        self.tasks.remove(task)

    def markTaskAsCompleted(self, task):
        if task in self.tasks:
            task.markAsCompleted()

    def getAllTasks(self):
        return list(self.tasks)

    def getPendingTasks(self):
        pending_tasks = []
        for task in self.tasks:
            if not task.isCompleted():
                pending_tasks.append(task)
        return pending_tasks

    def getCompletedTasks(self):
        completed_tasks = []
        for task in self.tasks:
            if task.isCompleted():
                completed_tasks.append(task)
        return completed_tasks

    def shiftTaskAround(self, task, position):
        if position >= len(self.tasks) or task not in self.tasks:
            return
        self.tasks.remove(task)
        self.tasks.insert(position, task)

    def getTasksOwnedBy(self, owner):
        rl_task = []
        for t in self.tasks:
            if t.getOwner() == owner:
                rl_task.append(t)
        return rl_task

    def changeOwner(self, owner, task):
        if task in self.tasks:
            i = self.tasks.index(task)
            task.setOwner(owner)
