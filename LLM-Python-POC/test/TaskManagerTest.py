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

    def testOverlappingTasksWithDifferentOwners(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.", date(2024, 9, 1), date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.", date(2024, 9, 10), date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.", date(2024, 9, 5), date(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        self.assertEqual(len(taskManager.getAllTasks()), 3)
        self.assertTrue(task1.endDate > task2.startDate)
        self.assertTrue(task2.endDate > task1.startDate)

        self.assertEqual(len(taskManager.getTasksOwnedBy("Ibrahim")), 2)
        self.assertEqual(len(taskManager.getTasksOwnedBy("Kevin")), 1)

    def testTaskCompletionUpdates(self):
        taskManager = TaskManager()
        task = Task(1, "Ibrahim",  "Task for Completion", "Task to test completion updates.", date(2024, 9, 1), date(2024, 9, 15))
        taskManager.addTask(task)

        task.markAsCompleted()
        task.completedDate = date.today()

        self.assertTrue(task.completed)
        assert task.completedDate is not None
        self.assertTrue(task.completedDate > task.endDate)

    def testSequentialTaskDependencies(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "First task in a sequence.", date(2024, 9, 1), date(2024, 9, 5))
        task2 = Task(2, "Kevin", "Task 2", "Dependent task.", date(2024, 9, 6), date(2024, 9, 10))

        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.markTaskAsCompleted(task1)

        self.assertEqual(len(taskManager.getCompletedTasks()), 1)
        self.assertTrue(task2.startDate > task1.endDate)

    def testTaskReassignment(self):
        taskManager = TaskManager()
        task = Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.", date(2024, 9, 1), date(2024, 9, 5))
        taskManager.addTask(task)

        taskManager.changeOwner("Kevin", task)

        self.assertEqual(task.owner, "Kevin")

    def testGetTasksOwnedBy(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.", date(2024, 9, 1), date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.", date(2024, 9, 10), date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.", date(2024, 9, 5), date(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        self.assertEqual(len(ibrahimTasks), 2)
        self.assertEqual(len(kevinTasks), 1)
        self.assertTrue(task1 in ibrahimTasks)
        self.assertTrue(task3 in ibrahimTasks)
        self.assertTrue(task2 in kevinTasks)

    def testUpdateOwnerAndGetTasksOwnedBy(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.", date(2024, 9, 1), date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.", date(2024, 9, 10), date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.", date(2024, 9, 5), date(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        self.assertEqual(len(ibrahimTasks), 2)
        self.assertEqual(len(kevinTasks), 1)
        self.assertTrue(task1 in ibrahimTasks)
        self.assertTrue(task3 in ibrahimTasks)
        self.assertTrue(task2 in kevinTasks)

        taskManager.changeOwner("Ibrahim", task2)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        self.assertEqual(3, len(ibrahimTasks))
        self.assertTrue(task1 in ibrahimTasks)
        self.assertTrue(task2 in ibrahimTasks)
        self.assertTrue(task3 in ibrahimTasks)


if __name__ == '__main__':
    unittest.main()
