import unittest
import Task
import TaskManager
from datetime import datetime, timedelta

class TaskManagerTest(unittest.TestCase):

    # Complex Test 1: Add task with specific start and end dates, verify date manipulation
    def test_add_task_with_date_manipulation(self):
        task_manager = TaskManager.TaskManager()
        start_date = datetime(2024, 10, 1)  # Set specific start date
        end_date = start_date + timedelta(days=30) - timedelta(weeks=1) + timedelta(days=3)  # Date manipulation

        task = Task.Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", start_date, end_date)
        task_manager.addTask(task)

        self.assertTrue(task.endDate > task.startDate)  # End date after start date
        self.assertEqual(26, (task.endDate - task.startDate).days)  # Period check
        self.assertEqual(1, len(task_manager.getAllTasks()))

    # Complex Test 2: Task completion date in the past
    def test_remove_task_and_completion_date_in_past(self):
        task_manager = TaskManager.TaskManager()
        start_date = datetime(2024, 9, 1)
        end_date = start_date + timedelta(weeks=2)  # Ends in mid-September

        task = Task.Task(1, "Ibrahim", "Remove Task", "Completion Test", start_date, end_date)
        task_manager.addTask(task)
        task_manager.markTaskAsCompleted(task)
        task_manager.removeTask(task)

        completed_date = datetime(2024, 9, 18)  # Set completion date in the past
        task.completionDate = completed_date

        self.assertTrue(task.isCompleted())
        self.assertTrue(task.completionDate < datetime.now())  # Ensure it's before "now"
        self.assertEqual(0, len(task_manager.getAllTasks()))

    # Complex Test 3: Overdue task identification using fixed date
    def test_overdue_task(self):
        task_manager = TaskManager.TaskManager()
        start_date = datetime(2024, 9, 1)  # Start date in the past
        due_date = datetime(2024, 9, 10)  # Overdue by now (October 2024)

        task = Task.Task(1, "Ibrahim", "Overdue Task", "Overdue Test", start_date, due_date)
        task_manager.addTask(task)

        self.assertTrue(datetime.now() > task.endDate)
        self.assertEqual(1, len(task_manager.getPendingTasks()))

    # Complex Test 4: Shuffle tasks, check date validity
    def test_shuffle_task_and_date_validation(self):
        task_manager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "Start Date Shift", datetime(2024, 9, 1), datetime(2024, 9, 10))
        task2 = Task.Task(2, "Kevin", "Task 2", "Due Date Shift", datetime(2024, 9, 5), datetime(2024, 9, 20))
        task_manager.addTask(task1)
        task_manager.addTask(task2)

        task_manager.shiftTaskAround(task1, 1)  # Shift task2 position
        self.assertTrue(task_manager.getAllTasks()[0].startDate > task_manager.getAllTasks()[1].startDate)
        self.assertEqual(2, len(task_manager.getAllTasks()))

    def test_overlapping_tasks_with_different_owners(self):
        task_manager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.",
                          datetime(2024, 9, 1), datetime(2024, 9, 15))
        task2 = Task.Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.",
                          datetime(2024, 9, 10), datetime(2024, 9, 20))
        task3 = Task.Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.",
                          datetime(2024, 9, 5), datetime(2024, 9, 12))

        task_manager.addTask(task1)
        task_manager.addTask(task2)
        task_manager.addTask(task3)

        self.assertEqual(3, len(task_manager.getAllTasks()))
        self.assertTrue(task1.endDate > task2.startDate)
        self.assertTrue(task2.endDate > task1.startDate)

    def test_task_completion_updates(self):
        task_manager = TaskManager.TaskManager()
        task = Task.Task(1, "Ibrahim", "Task for Completion", "Task to test completion updates.",
                         datetime(2024, 9, 1), datetime(2024, 9, 15))
        task_manager.addTask(task)

        task.markAsCompleted()
        task.completionDate = datetime.now()

        self.assertTrue(task.isCompleted())
        self.assertIsNotNone(task.completionDate)
        self.assertTrue(task.completionDate > task.endDate)

    def test_sequential_task_dependencies(self):
        task_manager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "First task in a sequence.",
                          datetime(2024, 9, 1), datetime(2024, 9, 5))
        task2 = Task.Task(2, "Kevin", "Task 2", "Dependent task.",
                          datetime(2024, 9, 6), datetime(2024, 9, 10))

        task_manager.addTask(task1)
        task_manager.addTask(task2)

        task_manager.markTaskAsCompleted(task1)

        self.assertEqual(1, len(task_manager.getCompletedTasks()))
        self.assertTrue(task2.startDate > task1.endDate)

    def test_task_reassignment(self):
        task_manager = TaskManager.TaskManager()
        task = Task.Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.",
                         datetime(2024, 9, 1), datetime(2024, 9, 15))
        task_manager.addTask(task)

        task_manager.changeOwner("Kevin", task)

        self.assertEqual("Kevin", task.owner)

    def test_get_tasks_owned_by(self):
        task_manager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                          datetime(2024, 9, 1), datetime(2024, 9, 15))
        task2 = Task.Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                          datetime(2024, 9, 10), datetime(2024, 9, 20))
        task3 = Task.Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                          datetime(2024, 9, 5), datetime(2024, 9, 12))

        task_manager.addTask(task1)
        task_manager.addTask(task2)
        task_manager.addTask(task3)

        ibrahim_tasks = task_manager.getTasksOwnedBy("Ibrahim")
        kevin_tasks = task_manager.getTasksOwnedBy("Kevin")

        self.assertEqual(2, len(ibrahim_tasks))
        self.assertEqual(1, len(kevin_tasks))
        self.assertIn(task1, ibrahim_tasks)
        self.assertIn(task3, ibrahim_tasks)
        self.assertIn(task2, kevin_tasks)

    def test_update_owner_and_get_tasks_owned_by(self):
        task_manager = TaskManager.TaskManager()
        task1 = Task.Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                          datetime(2024, 9, 1), datetime(2024, 9, 15))
        task2 = Task.Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                          datetime(2024, 9, 10), datetime(2024, 9, 20))
        task3 = Task.Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                          datetime(2024, 9, 5), datetime(2024, 9, 12))

        task_manager.addTask(task1)
        task_manager.addTask(task2)
        task_manager.addTask(task3)

        ibrahim_tasks = task_manager.getTasksOwnedBy("Ibrahim")
        kevin_tasks = task_manager.getTasksOwnedBy("Kevin")

        self.assertEqual(2, len(ibrahim_tasks))
        self.assertEqual(1, len(kevin_tasks))
        self.assertIn(task1, ibrahim_tasks)
        self.assertIn(task3, ibrahim_tasks)
        self.assertIn(task2, kevin_tasks)

        # let's update the owners
        task_manager.changeOwner("Ibrahim", task2)

        ibrahim_tasks = task_manager.getTasksOwnedBy("Ibrahim")

        self.assertEqual(3, len(ibrahim_tasks))
        self.assertIn(task1, ibrahim_tasks)
        self.assertIn(task2, ibrahim_tasks)
        self.assertIn(task3, ibrahim_tasks)

if __name__ == '__main__':
    unittest.main()
