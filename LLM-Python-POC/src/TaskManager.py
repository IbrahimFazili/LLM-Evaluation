import Task

class TaskManager:
    tasks: list

    def __init__(self) -> None:
        self.tasks = []

    def addTask(self, task: Task) -> None:
        self.tasks.append(task)

    def removeTask(self, task: Task) -> None:
        self.tasks.remove(task)

    def markTaskAsCompleted(self, task: Task) -> None:
        if task in self.tasks:
            i = self.tasks.index(task)
            self.tasks[i].markAsCompleted()

    def getAllTasks(self) -> list:
        return self.tasks
    
    def getCompletedTasks(self) -> list:
        return [task for task in self.tasks if task.completed]
    
    def getPendingTasks(self) -> list:
        return [task for task in self.tasks if not task.completed]
    
    def shiftTaskAround(self, task: Task, position: int) -> None:
        if position < 0 or position >= len(self.tasks) or task not in self.tasks:
            return
        self.tasks.remove(task)
        self.tasks.insert(position, task)

    def getTasksOwnedBy(self, owner: str) -> list:
        return [task for task in self.tasks if task.owner == owner]
    
    def changeOwner(self, owner: str, task: Task) -> None:
        if task in self.tasks:
            i = self.tasks.index(task)
            self.tasks[i].owner = owner