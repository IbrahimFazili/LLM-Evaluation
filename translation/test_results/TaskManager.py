import java.time.LocalDate
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
        pendingTasks = []
        for task in self.tasks:
            if not task.completed:
                pendingTasks.append(task)
        return pendingTasks

    def getCompletedTasks(self):
        completedTasks = []
        for task in self.tasks:
            if task.completed:
                completedTasks.append(task)
        return completedTasks

    def shiftTaskAround(self, task, position):
        if position >= len(self.tasks) or task not in self.tasks:
            return
        self.tasks.remove(task)
        self.tasks.insert(position, task)

    def getTasksOwnedBy(self, owner):
        rlTask = []
        for t in self.tasks:
            if t.owner == owner:
                rlTask.append(t)
        return rlTask

    def changeOwner(self, owner, task):
        if task in self.tasks:
            i = self.tasks.index(task)
            self.tasks[i].owner = owner
