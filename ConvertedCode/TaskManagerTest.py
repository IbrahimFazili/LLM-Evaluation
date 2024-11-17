import unittest
import datetime
from TaskManager import TaskManager
from Task import Task

class TaskManagerTest(unittest.TestCase):

    def testAddTaskWithDateManipulation(self):
        taskManager = TaskManager()
        startDate = datetime.date(2024, 10, 1)
        endDate = startDate + datetime.timedelta(days=30) - datetime.timedelta(weeks=1) + datetime.timedelta(days=3)

        task = Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", startDate, endDate)
        taskManager.addTask(task)

        self.assertTrue(task.endDate > task.startDate)
        self.assertEqual((task.endDate - task.startDate).days, 26)
        self.assertEqual(len(taskManager.getAllTasks()), 1)

    def testRemoveTaskAndCompletionDateInPast(self):
        taskManager = TaskManager()
        startDate = datetime.date(2024, 9, 1)
        endDate = startDate + datetime.timedelta(weeks=2)

        task = Task(1, "Ibrahim", "Remove Task", "Completion Test", startDate, endDate)
        taskManager.addTask(task)
        taskManager.markTaskAsCompleted(task)
        taskManager.removeTask(task)

        completedDate = datetime.date(2024, 9, 18)
        task.completionDate = completedDate

        self.assertTrue(task.completed)
        self.assertTrue(task.completionDate < datetime.date.today())
        self.assertEqual(len(taskManager.getAllTasks()), 0)

    def testOverdueTask(self):
        taskManager = TaskManager()
        startDate = datetime.date(2024, 9, 1)
        dueDate = datetime.date(2024, 9, 10)

        task = Task(1, "Ibrahim", "Overdue Task", "Overdue Test", startDate, dueDate)
        taskManager.addTask(task)

        self.assertTrue(datetime.date.today() > task.endDate)
        self.assertEqual(len(taskManager.getPendingTasks()), 1)

    def testShuffleTaskAndDateValidation(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Start Date Shift", datetime.date(2024, 9, 1), datetime.date(2024, 9, 10))
        task2 = Task(2, "Kevin", "Task 2", "Due Date Shift", datetime.date(2024, 9, 5), datetime.date(2024, 9, 20))
        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.shiftTaskAround(task1, 1)
        self.assertTrue(taskManager.getAllTasks()[0].startDate > taskManager.getAllTasks()[1].startDate)
        self.assertEqual(len(taskManager.getAllTasks()), 2)

    def testOverlappingTasksWithDifferentOwners(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.",
                      datetime.date(2024, 9, 1), datetime.date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.",
                      datetime.date(2024, 9, 10), datetime.date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.",
                      datetime.date(2024, 9, 5), datetime.date(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        self.assertEqual(len(taskManager.getAllTasks()), 3)
        self.assertTrue(task1.endDate > task2.startDate)
        self.assertTrue(task2.endDate > task1.startDate)

    def testTaskCompletionUpdates(self):
        taskManager = TaskManager()
        task = Task(1, "Ibrahim", "Task for Completion", "Task to test completion updates.",
                    datetime.date(2024, 9, 1), datetime.date(2024, 9, 15))
        taskManager.addTask(task)

        task.markAsCompleted()
        task.completionDate = datetime.date.today()

        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completionDate)
        self.assertTrue(task.completionDate > task.endDate)

    def testSequentialTaskDependencies(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "First task in a sequence.",
                      datetime.date(2024, 9, 1), datetime.date(2024, 9, 5))
        task2 = Task(2, "Kevin", "Task 2", "Dependent task.",
                      datetime.date(2024, 9, 6), datetime.date(2024, 9, 10))

        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.markTaskAsCompleted(task1)

        self.assertEqual(len(taskManager.getCompletedTasks()), 1)
        self.assertTrue(task2.startDate > task1.endDate)

    def testTaskReassignment(self):
        taskManager = TaskManager()
        task = Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.",
                    datetime.date(2024, 9, 1), datetime.date(2024, 9, 15))
        taskManager.addTask(task)

        taskManager.changeOwner("Kevin", task)

        self.assertEqual(task.owner, "Kevin")

    def testGetTasksOwnedBy(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                      datetime.date(2024, 9, 1), datetime.date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                      datetime.date(2024, 9, 10), datetime.date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                      datetime.date(2024, 9, 5), datetime.date(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        self.assertEqual(len(ibrahimTasks), 2)
        self.assertEqual(len(kevinTasks), 1)
        self.assertIn(task1, ibrahimTasks)
        self.assertIn(task3, ibrahimTasks)
        self.assertIn(task2, kevinTasks)

    def testUpdateOwnerAndGetTasksOwnedBy(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                      datetime.date(2024, 9, 1), datetime.date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                      datetime.date(2024, 9, 10), datetime.date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                      datetime.date(2024, 9, 5), datetime.date(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        self.assertEqual(len(ibrahimTasks), 2)
        self.assertEqual(len(kevinTasks), 1)
        self.assertIn(task1, ibrahimTasks)
        self.assertIn(task3, ibrahimTasks)
        self.assertIn(task2, kevinTasks)

        taskManager.changeOwner("Ibrahim", task2)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")

        self.assertEqual(len(ibrahimTasks), 3)
        self.assertIn(task1, ibrahimTasks)
        self.assertIn(task2, ibrahimTasks)
        self.assertIn(task3, ibrahimTasks)

if __name__ == '__main__':
    unittest.main()
