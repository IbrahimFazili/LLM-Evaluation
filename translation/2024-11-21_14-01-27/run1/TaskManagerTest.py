import unittest
import Task
import TaskManager
from datetime import timedelta, date

class TaskManagerTest(unittest.TestCase):

    # Complex Test 1: Add task with specific start and end dates, verify date manipulation
    def test_add_task_with_date_manipulation(self):
        task_manager = TaskManager()
        start_date = date(2024, 10, 1)  # Set specific start date
        end_date = start_date + timedelta(days=30) - timedelta(weeks=1) + timedelta(days=3)  # Date manipulation

        task = Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", start_date, end_date)
        task_manager.add_task(task)

        self.assertTrue(task.end_date > task.start_date)  # End date after start date
        self.assertEqual((task.end_date - task.start_date).days, 26)  # Period check
        self.assertEqual(len(task_manager.get_all_tasks()), 1)

    # Complex Test 2: Task completion date in the past
    def test_remove_task_and_completion_date_in_past(self):
        task_manager = TaskManager()
        start_date = date(2024, 9, 1)
        end_date = start_date + timedelta(weeks=2)  # Ends in mid-September

        task = Task(1, "Ibrahim", "Remove Task", "Completion Test", start_date, end_date)
        task_manager.add_task(task)
        task_manager.mark_task_as_completed(task)
        task_manager.remove_task(task)

        completed_date = date(2024, 9, 18)  # Set completion date in the past
        task.set_completion_date(completed_date)

        self.assertTrue(task.is_completed())
        self.assertTrue(task.get_completion_date() < date.today())  # Ensure it's before "now"
        self.assertEqual(len(task_manager.get_all_tasks()), 0)

    # Complex Test 3: Overdue task identification using fixed date
    def test_overdue_task(self):
        task_manager = TaskManager()
        start_date = date(2024, 9, 1)  # Start date in the past
        due_date = date(2024, 9, 10)  # Overdue by now (October 2024)

        task = Task(1, "Ibrahim", "Overdue Task", "Overdue Test", start_date, due_date)
        task_manager.add_task(task)

        self.assertTrue(date.today() > task.end_date)
        self.assertEqual(len(task_manager.get_pending_tasks()), 1)

    # Complex Test 4: Shuffle tasks, check date validity
    def test_shuffle_task_and_date_validation(self):
        task_manager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Start Date Shift", date(2024, 9, 1), date(2024, 9, 10))
        task2 = Task(2, "Kevin", "Task 2", "Due Date Shift", date(2024, 9, 5), date(2024, 9, 20))
        task_manager.add_task(task1)
        task_manager.add_task(task2)

        task_manager.shift_task_around(task1, 1)  # Shift task2 position
        self.assertTrue(task_manager.get_all_tasks()[0].start_date > task_manager.get_all_tasks()[1].start_date)
        self.assertEqual(len(task_manager.get_all_tasks()), 2)

    def test_overlapping_tasks_with_different_owners(self):
        task_manager = TaskManager()
        task1 = Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.",
                     date(2024, 9, 1), date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.",
                     date(2024, 9, 10), date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.",
                     date(2024, 9, 5), date(2024, 9, 12))

        task_manager.add_task(task1)
        task_manager.add_task(task2)
        task_manager.add_task(task3)

        self.assertEqual(len(task_manager.get_all_tasks()), 3)
        self.assertTrue(task1.end_date > task2.start_date)
        self.assertTrue(task2.end_date > task1.start_date)

    def test_task_completion_updates(self):
        task_manager = TaskManager()
        task = Task(1, "Ibrahim", "Task for Completion", "Task to test completion updates.",
                    date(2024, 9, 1), date(2024, 9, 15))
        task_manager.add_task(task)

        task.mark_as_completed()
        task.set_completion_date(date.today())

        self.assertTrue(task.is_completed())
        self.assertIsNotNone(task.get_completion_date())
        self.assertTrue(task.get_completion_date() > task.end_date)

    def test_sequential_task_dependencies(self):
        task_manager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "First task in a sequence.",
                     date(2024, 9, 1), date(2024, 9, 5))
        task2 = Task(2, "Kevin", "Task 2", "Dependent task.",
                     date(2024, 9, 6), date(2024, 9, 10))

        task_manager.add_task(task1)
        task_manager.add_task(task2)

        task_manager.mark_task_as_completed(task1)

        self.assertEqual(len(task_manager.get_completed_tasks()), 1)
        self.assertTrue(task2.start_date > task1.end_date)

    def test_task_reassignment(self):
        task_manager = TaskManager()
        task = Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.",
                    date(2024, 9, 1), date(2024, 9, 15))
        task_manager.add_task(task)

        task_manager.change_owner("Kevin", task)

        self.assertEqual(task.owner, "Kevin")

    def test_get_tasks_owned_by(self):
        task_manager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                     date(2024, 9, 1), date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                     date(2024, 9, 10), date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                     date(2024, 9, 5), date(2024, 9, 12))

        task_manager.add_task(task1)
        task_manager.add_task(task2)
        task_manager.add_task(task3)

        ibrahim_tasks = task_manager.get_tasks_owned_by("Ibrahim")
        kevin_tasks = task_manager.get_tasks_owned_by("Kevin")

        self.assertEqual(len(ibrahim_tasks), 2)
        self.assertEqual(len(kevin_tasks), 1)
        self.assertIn(task1, ibrahim_tasks)
        self.assertIn(task3, ibrahim_tasks)
        self.assertIn(task2, kevin_tasks)

    def test_update_owner_and_get_tasks_owned_by(self):
        task_manager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                     date(2024, 9, 1), date(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                     date(2024, 9, 10), date(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                     date(2024, 9, 5), date(2024, 9, 12))

        task_manager.add_task(task1)
        task_manager.add_task(task2)
        task_manager.add_task(task3)

        ibrahim_tasks = task_manager.get_tasks_owned_by("Ibrahim")
        kevin_tasks = task_manager.get_tasks_owned_by("Kevin")

        self.assertEqual(len(ibrahim_tasks), 2)
        self.assertEqual(len(kevin_tasks), 1)
        self.assertIn(task1, ibrahim_tasks)
        self.assertIn(task3, ibrahim_tasks)
        self.assertIn(task2, kevin_tasks)

        # let's update the owners
        task_manager.change_owner("Ibrahim", task2)

        ibrahim_tasks = task_manager.get_tasks_owned_by("Ibrahim")

        self.assertEqual(len(ibrahim_tasks), 3)
        self.assertIn(task1, ibrahim_tasks)
        self.assertIn(task2, ibrahim_tasks)
        self.assertIn(task3, ibrahim_tasks)

if __name__ == '__main__':
    unittest.main()
