import java
import unittest
import sys
import os
import datetime
from datetime import date, timedelta

Task = java.type('org.cornell.Task')
TaskManager = java.type('org.cornell.TaskManager')

class TaskManagerTest(unittest.TestCase):

    def javaLocalDateToPythonDate(self, javaLocalDate):
        """Helper function to convert Java LocalDate to Python date."""
        return date(javaLocalDate.getYear(), javaLocalDate.getMonthValue(), javaLocalDate.getDayOfMonth())

    def testAddTaskWithDateManipulation(self):
        taskManager = TaskManager()
        startDate = date(2024, 10, 1)
        endDate = startDate + timedelta(days=30) + timedelta(weeks=-1) + timedelta(days=3)

        task = Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", startDate, endDate)
        taskManager.addTask(task)
        
        pythonStartDate = self.javaLocalDateToPythonDate(task.getStartDate())
        pythonEndDate = self.javaLocalDateToPythonDate(task.getEndDate())

        self.assertTrue(pythonStartDate < pythonEndDate)
        self.assertEqual(pythonEndDate - pythonStartDate, timedelta(days=26))
        self.assertEqual(len(taskManager.getAllTasks()), 1)

    def testRemoveTaskAndCompletionDateInPast(self):
        taskManager = TaskManager()
        startDate = date(2024, 9, 1)
        endDate = startDate + timedelta(weeks=2)

        task = Task(1, "Ibrahim", "Remove Task", "Completion Test", startDate, endDate)
        taskManager.addTask(task)

        taskManager.markTaskAsCompleted(task)

        completedDate = date(2024, 9, 18)
        task.setCompletionDate(completedDate)

        taskManager.removeTask(task)

        self.assertTrue(task.isCompleted()) 
        self.assertTrue(self.javaLocalDateToPythonDate(task.getCompletionDate()) < date.today())
        self.assertEqual(len(taskManager.getAllTasks()), 0)

    
    def testOverdueTask(self):
        taskManager = TaskManager()
        startDate = date(2024, 9, 1)
        dueDate = date(2024, 9, 10)

        task = Task(1, "Ibrahim", "Overdue Task", "Overdue Test", startDate, dueDate)
        taskManager.addTask(task)

        pythonDueDate = self.javaLocalDateToPythonDate(task.getEndDate())

        self.assertTrue(pythonDueDate < date.today())

        self.assertEqual(len(taskManager.getPendingTasks()), 1)

    def testShuffleTaskAndDateValidation(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Start Date Test", date(2024, 9, 1), date(2024, 9, 10))
        task2 = Task(2, "Kevin", "Task 2", "Due Date Test", date(2024, 9, 5), date(2024, 9, 20))

        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.shiftTaskAround(task1, 1)

        self.assertEqual(len(taskManager.getAllTasks()), 2)

        task1StartDate = self.javaLocalDateToPythonDate(taskManager.getAllTasks()[0].getStartDate())
        task2StartDate = self.javaLocalDateToPythonDate(taskManager.getAllTasks()[1].getStartDate())

        self.assertTrue(task1StartDate > task2StartDate)


    def testOverlappingTasksWithDifferentOwners(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.", date(2024, 9, 1), date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.", date(2024, 9, 10), date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.", date(2024, 9, 5), date(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        self.assertEqual(len(taskManager.getAllTasks()), 3)

        task1EndDate = self.javaLocalDateToPythonDate(task1.getEndDate())
        task2StartDate = self.javaLocalDateToPythonDate(task2.getStartDate())
        task2EndDate = self.javaLocalDateToPythonDate(task2.getEndDate())
        task1StartDate = self.javaLocalDateToPythonDate(task1.getStartDate())

        self.assertTrue(task1EndDate > task2StartDate)
        self.assertTrue(task2EndDate > task1StartDate)

        self.assertEqual(len(taskManager.getTasksOwnedBy("Ibrahim")), 2)
        self.assertEqual(len(taskManager.getTasksOwnedBy("Kevin")), 1)

    def testTaskCompletionUpdates(self):
        taskManager = TaskManager()
        task = Task(1, "Ibrahim", "Task for Completion", "Task to test completion updates.", date(2024, 9, 1), date(2024, 9, 15))
        taskManager.addTask(task)

        task.markAsCompleted()
        task.setCompletionDate(date.today())

        self.assertTrue(task.isCompleted())

        taskEndDate = self.javaLocalDateToPythonDate(task.getEndDate())
        taskCompletionDate = self.javaLocalDateToPythonDate(task.getCompletionDate())

        self.assertIsNotNone(taskCompletionDate)
        self.assertTrue(taskCompletionDate > taskEndDate)

    def testSequentialTaskDependencies(self):
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "First task in a sequence.", date(2024, 9, 1), date(2024, 9, 5))
        task2 = Task(2, "Kevin", "Task 2", "Dependent task.", date(2024, 9, 6), date(2024, 9, 10))

        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.markTaskAsCompleted(task1)

        self.assertEqual(len(taskManager.getCompletedTasks()), 1)  # Check if task1 is marked as completed

        task1EndDate = self.javaLocalDateToPythonDate(task1.getEndDate())
        task2StartDate = self.javaLocalDateToPythonDate(task2.getStartDate())

        self.assertTrue(task2StartDate > task1EndDate)

    def testTaskReassignment(self):
        taskManager = TaskManager()
        task = Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.", date(2024, 9, 1), date(2024, 9, 5))
        taskManager.addTask(task)

        taskManager.changeOwner("Kevin", task)

        self.assertEqual(task.getOwner(), "Kevin")  # Use the getter method to get the owner's name

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
        self.assertIn(task1, ibrahimTasks)
        self.assertIn(task3, ibrahimTasks)
        self.assertIn(task2, kevinTasks)

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