import org.cornell.Task
import org.cornell.TaskManager
import org.junit.jupiter.api.Test

import java.time.LocalDate
import java.time.temporal.ChronoUnit
import java.util.List

import static org.junit.jupiter.api.Assertions.*

class TaskManagerTest:

    # Complex Test 1: Add task with specific start and end dates, verify date manipulation
    @Test
    def testAddTaskWithDateManipulation():
        taskManager = TaskManager()
        startDate = LocalDate.of(2024, 10, 1)  # Set specific start date
        endDate = startDate.plus(30, ChronoUnit.DAYS).minusWeeks(1).plusDays(3)  # Date manipulation

        task = Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", startDate, endDate)
        taskManager.addTask(task)

        assert task.getEndDate().isAfter(task.getStartDate())  # End date after start date
        assertEquals(26, ChronoUnit.DAYS.between(task.getStartDate(), task.getEndDate()))  # Period check
        assertEquals(1, taskManager.getAllTasks().size())

    # Complex Test 2: Task completion date in the past
    @Test
    def testRemoveTaskAndCompletionDateInPast():
        taskManager = TaskManager()
        startDate = LocalDate.of(2024, 9, 1)
        endDate = startDate.plusWeeks(2)  # Ends in mid-September

        task = Task(1, "Ibrahim", "Remove Task", "Completion Test", startDate, endDate)
        taskManager.addTask(task)
        taskManager.markTaskAsCompleted(task)
        taskManager.removeTask(task)

        completedDate = LocalDate.of(2024, 9, 18)  # Set completion date in the past
        task.setCompletionDate(completedDate)

        assert task.isCompleted()
        assert task.getCompletionDate().isBefore(LocalDate.now())  # Ensure it's before "now"
        assertEquals(0, taskManager.getAllTasks().size())

    # Complex Test 3: Overdue task identification using fixed date
    @Test
    def testOverdueTask():
        taskManager = TaskManager()
        startDate = LocalDate.of(2024, 9, 1)  # Start date in the past
        dueDate = LocalDate.of(2024, 9, 10)  # Overdue by now (October 2024)

        task = Task(1, "Ibrahim", "Overdue Task", "Overdue Test", startDate, dueDate)
        taskManager.addTask(task)

        assert LocalDate.now().isAfter(task.getEndDate())
        assertEquals(1, taskManager.getPendingTasks().size())

    # Complex Test 4: Shuffle tasks, check date validity
    @Test
    def testShuffleTaskAndDateValidation():
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Start Date Shift", LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 10))
        task2 = Task(2, "Kevin", "Task 2", "Due Date Shift", LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 20))
        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.shiftTaskAround(task1, 1)  # Shift task2 position
        assert taskManager.getAllTasks().get(0).getStartDate().isAfter(taskManager.getAllTasks().get(1).getStartDate())
        assertEquals(2, taskManager.getAllTasks().size())

    @Test
    def testOverlappingTasksWithDifferentOwners():
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.",
                     LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15))
        task2 = Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.",
                     LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.",
                     LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        assertEquals(3, taskManager.getAllTasks().size())
        assert task1.getEndDate().isAfter(task2.getStartDate())
        assert task2.getEndDate().isAfter(task1.getStartDate())

    @Test
    def testTaskCompletionUpdates():
        taskManager = TaskManager()
        task = Task(1, "Ibrahim", "Task for Completion", "Task to test completion updates.",
                     LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15))
        taskManager.addTask(task)

        task.markAsCompleted()
        task.setCompletionDate(LocalDate.now())

        assert task.isCompleted()
        assert task.getCompletionDate() is not None
        assert task.getCompletionDate().isAfter(task.getEndDate())

    @Test
    def testSequentialTaskDependencies():
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "First task in a sequence.",
                     LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 5))
        task2 = Task(2, "Kevin", "Task 2", "Dependent task.",
                     LocalDate.of(2024, 9, 6), LocalDate.of(2024, 9, 10))

        taskManager.addTask(task1)
        taskManager.addTask(task2)

        taskManager.markTaskAsCompleted(task1)

        assertEquals(1, taskManager.getCompletedTasks().size())
        assert task2.getStartDate().isAfter(task1.getEndDate())

    @Test
    def testTaskReassignment():
        taskManager = TaskManager()
        task = Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.",
                     LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15))
        taskManager.addTask(task)

        taskManager.changeOwner("Kevin", task)

        assertEquals("Kevin", task.getOwner())

    @Test
    def testGetTasksOwnedBy():
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                     LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                     LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                     LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        assertEquals(2, ibrahimTasks.size())
        assertEquals(1, kevinTasks.size())
        assert ibrahimTasks.contains(task1)
        assert ibrahimTasks.contains(task3)
        assert kevinTasks.contains(task2)

    @Test
    def testUpdateOwnerAndGetTasksOwnedBy():
        taskManager = TaskManager()
        task1 = Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                     LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15))
        task2 = Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                     LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20))
        task3 = Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                     LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12))

        taskManager.addTask(task1)
        taskManager.addTask(task2)
        taskManager.addTask(task3)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")
        kevinTasks = taskManager.getTasksOwnedBy("Kevin")

        assertEquals(2, ibrahimTasks.size())
        assertEquals(1, kevinTasks.size())
        assert ibrahimTasks.contains(task1)
        assert ibrahimTasks.contains(task3)
        assert kevinTasks.contains(task2)

        # let's update the owners
        taskManager.changeOwner("Ibrahim", task2)

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim")

        assertEquals(3, ibrahimTasks.size())
        assert ibrahimTasks.contains(task1)
        assert ibrahimTasks.contains(task2)
        assert ibrahimTasks.contains(task3)
