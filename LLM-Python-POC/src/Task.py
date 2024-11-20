import datetime

class Task:
    id: int
    owner: str
    name: str
    description: str
    startDate: datetime.date
    endDate: datetime.date
    completed: bool
    completedDate: datetime.date

    def __init__(self, id,  owner,  name,  description,  startDate,  endDate):
        self.id = id
        self.owner = owner
        self.name = name
        self.description = description
        self.startDate = startDate
        self.endDate = endDate
        self.completed = False
        self.completedDate = None


    def markAsCompleted(self):
        self.completed = True
