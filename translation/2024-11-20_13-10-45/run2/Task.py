import datetime

class Task:

    def __init__(self, id, owner, name, description, startDate, endDate):
        self.id = id
        self.owner = owner
        self.title = name
        self.description = description
        self.startDate = startDate
        self.endDate = endDate
        self.completionDate = None
        self.completed = False

    def markAsCompleted(self):
        self.completed = True


class TaskManager:

    def __init__(self):
        self.tasks = []

    def addTask(self, task):
        self.tasks.append(task)

    def removeTask(self, taskId):
        self.tasks = [task for task in self.tasks if task.id != taskId]

    def getTask(self, taskId):
        for task in self.tasks:
            if task.id == taskId:
                return task
        return None

    def getAllTasks(self):
        return self.tasks

    def completeTask(self, taskId):
        task = self.getTask(taskId)
        if task:
            task.markAsCompleted()
