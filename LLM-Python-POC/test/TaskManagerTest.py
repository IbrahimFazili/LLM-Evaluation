import unittest
import sys
import os
import datetime
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from TaskManager import TaskManager
from Task import Task

class TaskManagerTest(unittest.TestCase):

    # Complex Test 1: Add task with specific start and end dates, verify date manipulation
    def testAddTaskWithDateManipulation(self):
        taskManager = TaskManager()
        startDate = date(2024, 10, 1)
        endDate = startDate + timedelta(days=30) + timedelta(weeks=-1) + timedelta(days=3)

        task = Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", startDate, endDate)
        taskManager.addTask(task)
        
        self.assertTrue(task.startDate < task.endDate)
        self.assertEqual(task.endDate - task.startDate, timedelta(days=26))
        self.assertEqual(len(taskManager.getAllTasks()), 1)

    # Complex Test 2: Task completion date in the past
    def testRemoveTaskAndCompletionDateInPast(self):
        taskManager = TaskManager()
        startDate = date(2024, 9, 1)
        endDate = startDate + timedelta(weeks=2)
        
        task = Task(1, "Ibrahim", "Remove Task", "Completion Test", startDate, endDate)
        taskManager.addTask(task)
        taskManager.markTaskAsCompleted(task)
        taskManager.removeTask(task)

        completedDate = date(2024, 9, 18)
        task.completedDate = completedDate

        self.assertEqual(task.completed, True)
        self.assertTrue(task.completedDate < date.today())
        self.assertEqual(len(taskManager.getAllTasks()), 0)

    # Complex Test 3: Overdue task identification using fixed date
    def testOverdueTask(self):
        taskManager = TaskManager()
        startDate = date(2024, 9, 1)
        dueDate = date(2024, 9, 10)

        task = Task(1, "Ibrahim", "Overdue Task", "Overdue Test", startDate, dueDate)
        taskManager.addTask(task)

        self.assertTrue(task.endDate < date.today())
        self.assertEqual(len(taskManager.getPendingTasks()), 1)

    # Complex Test 4: Shuffle tasks, check date validity
    def testShuffleTaskAndDateValidation(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Start Date Test", date(2024, 9, 1), date(2024, 9, 10))
        task2 = Task(2, "Kevin", "Task 2", "Due Date Test", date(2024, 9, 5), date(2024, 9, 20))
        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.shiftTaskAround(task1, 1)

        self.assertEqual(len(taskManager.getAllTasks()), 2)
        self.assertTrue(taskManager.tasks[0].startDate > taskManager.tasks[1].startDate)

if __name__ == '__main__':
    unittest.main()
