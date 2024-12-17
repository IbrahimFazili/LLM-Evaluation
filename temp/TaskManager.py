import Task
from typing import List

class TaskManager:
    def __init__(self):
        self.tasks = []

    def addTask(self, task: Task):
        self.tasks.append(task)

    def removeTask(self, task: Task):
        self.tasks.remove(task)

    def markTaskAsCompleted(self, task: Task):
        if task in self.tasks:
            task.markAsCompleted()

    def getAllTasks(self) -> List[Task]:
        return list(self.tasks)

    def getPendingTasks(self) -> List[Task]:
        pending_tasks = []
        for task in self.tasks:
            if not task.isCompleted():
                pending_tasks.append(task)
        return pending_tasks

    def getCompletedTasks(self) -> List[Task]:
        completed_tasks = []
        for task in self.tasks:
            if task.isCompleted():
                completed_tasks.append(task)
        return completed_tasks

    def shiftTaskAround(self, task: Task, position: int):
        if position >= len(self.tasks) or task not in self.tasks:
            return
        self.tasks.remove(task)
        self.tasks.insert(position, task)

    def getTasksOwnedBy(self, owner: str) -> List[Task]:
        rl_task = []
        for t in self.tasks:
            if t.getOwner() == owner:
                rl_task.append(t)
        return rl_task

    def changeOwner(self, owner: str, task: Task):
        if task in self.tasks:
            i = self.tasks.index(task)
            task.setOwner(owner)
