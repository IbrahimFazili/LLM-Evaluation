import unittest
import Task
import TaskManager
from datetime import datetime, timedelta

class TaskManagerTest(unittest.TestCase):

    def testAddTaskWithDateManipulation(self):
        taskManager = TaskManager.TaskManager()
        startDate = datetime(2024, 10, 1)  # Set specific start date
        endDate = startDate + timedelta(days=30) - timedelta(weeks=1) + timedelta(days=3)  # Date manipulation

        task = Task.Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", startDate, endDate)
        taskManager.addTask(task)

        self.assertTrue(task.endDate > task.startDate)  # End date after start date
        self.assertEqual(26, (task.endDate - task.startDate).days)  # Period check
        self.assertEqual(1, len(taskManager.getAllTasks()))

    def testRemoveTaskAndCompletionDateInPast(self):
        taskManager = TaskManager.TaskManager()
        startDate = datetime(2024, 9, 1)
        endDate = startDate + timedelta(weeks=2)  # Ends in mid-September

        task = Task.Task(1, "Ibrahim", "Remove Task", "Completion Test", startDate, endDate)
        taskManager.addTask(task)
        taskManager.markTaskAsCompleted(task)
        taskManager.removeTask(task)

        completedDate = datetime(2024, 9, 18)  # Set completion date in the past
        task.completionDate = completedDate  # Correctly setting the completion date

        self.assertTrue(task.isCompleted())
        self.assertTrue(task.completionDate < datetime.now())  # Ensure it's before "now"
        self.assertEqual(0, len(taskManager.getAllTasks()))

    def testOverdueTask(self):
        taskManager = TaskManager.TaskManager()
        startDate = datetime(2024, 9, 1)  # Start date in the past
        dueDate = datetime(2024, 9, 10)  # Overdue by now (October 2024)

        task = Task.Task(1, "Ibrahim", "Overdue Task", "Overdue Test", startDate, dueDate)
        taskManager.addTask(task)

        self.assertTrue(datetime.now() > task.endDate)
        self.assertEqual(1, len(taskManager.getPendingTasks()))

    def testShuffleTaskAndDateValidation(self):
        taskManager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "Start Date Shift", datetime(2024, 9, 1), datetime(2024, 9, 10))
        task2 = Task.Task(2, "Kevin", "Task 2", "Due Date Shift", datetime(2024, 9, 5), datetime(2024, 9, 20))
        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.shiftTaskAround(task1, 1)  # Shift task2 position
        self.assertTrue(taskManager.getAllTasks()[0].startDate > taskManager.getAllTasks()[1].startDate)
        self.assertEqual(2, len(taskManager.getAllTasks()))

    def testOverlappingTasksWithDifferentOwners(self):
        taskManager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.",
                          datetime(2024, 9, 1), datetime(2024, 9, 15))
        task2 = Task.Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.",
                          datetime(2024, 9, 10), datetime(2024, 9, 20))
        task3 = Task.Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.",
                          datetime(2024, 9, 5), datetime(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        self.assertEqual(3, len(taskManager.getAllTasks()))
        self.assertTrue(task1.endDate > task2.startDate)
        self.assertTrue(task2.endDate > task1.startDate)

    def testTaskCompletionUpdates(self):
        taskManager = TaskManager.TaskManager()
        task = Task.Task(1, "Ibrahim", "Task for Completion", "Task to test completion updates.",
                         datetime(2024, 9, 1), datetime(2024, 9, 15))
        taskManager.addTask(task)

        task.markAsCompleted()
        task.completionDate = datetime.now()  # Correctly setting the completion date

        self.assertTrue(task.isCompleted())
        self.assertIsNotNone(task.completionDate)
        self.assertTrue(task.completionDate > task.endDate)

    def testSequentialTaskDependencies(self):
        taskManager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "First task in a sequence.",
                          datetime(2024, 9, 1), datetime(2024, 9, 5))
        task2 = Task.Task(2, "Kevin", "Task 2", "Dependent task.",
                          datetime(2024, 9, 6), datetime(2024, 9, 10))

        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.markTaskAsCompleted(task1)

        self.assertEqual(1, len(taskManager.getCompletedTasks()))
        self.assertTrue(task2.startDate > task1.endDate)

    def testTaskReassignment(self):
        taskManager = TaskManager.TaskManager()
        task = Task.Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.",
                         datetime(2024, 9, 1), datetime(2024, 9, 15))
        taskManager.addTask(task)

        taskManager.changeOwner("Kevin", task)

        self.assertEqual("Kevin", task.owner)

    def testGetTasksOwnedBy(self):
        taskManager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                          datetime(2024, 9, 1), datetime(2024, 9, 15))
        task2 = Task.Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                          datetime(2024, 9, 10), datetime(2024, 9, 20))
        task3 = Task.Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                          datetime(2024, 9, 5), datetime(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        self.assertEqual(2, len(ibrahimTasks))
        self.assertEqual(1, len(kevinTasks))
        self.assertIn(task1, ibrahimTasks)
        self.assertIn(task3, ibrahimTasks)
        self.assertIn(task2, kevinTasks)

    def testUpdateOwnerAndGetTasksOwnedBy(self):
        taskManager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                          datetime(2024, 9, 1), datetime(2024, 9, 15))
        task2 = Task.Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                          datetime(2024, 9, 10), datetime(2024, 9, 20))
        task3 = Task.Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                          datetime(2024, 9, 5), datetime(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        self.assertEqual(2, len(ibrahimTasks))
        self.assertEqual(1, len(kevinTasks))
        self.assertIn(task1, ibrahimTasks)
        self.assertIn(task3, ibrahimTasks)
        self.assertIn(task2, kevinTasks)

        # let's update the owners
        taskManager.changeOwner("Ibrahim", task2)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")

        self.assertEqual(3, len(ibrahimTasks))
        self.assertIn(task1, ibrahimTasks)
        self.assertIn(task2, ibrahimTasks)
        self.assertIn(task3, ibrahimTasks)

if __name__ == '__main__':
    unittest.main()
