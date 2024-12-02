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

    def setOwner(self, owner):
        self.owner = owner

    def getOwner(self):
        return self.owner

    def isCompleted(self):
        return self.completed

    def setCompleted(self, completed):
        self.completed = completed


class TaskManager:

    def __init__(self):
        self.tasks = []

    def addTask(self, task):
        self.tasks.append(task)

    def getTasks(self):
        return self.tasks

    def markTaskAsCompleted(self, taskId):
        for task in self.tasks:
            if task.id == taskId:
                task.markAsCompleted()
                break
