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
