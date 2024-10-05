import org.cornell.Task;
import org.cornell.TaskManager;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TaskManagerTest {

    // Complex Test 1: Add task with specific start and end dates, verify date manipulation
    @Test
    void testAddTaskWithDateManipulation() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2024, 10, 1); // Set specific start date
        LocalDate endDate = startDate.plus(30, ChronoUnit.DAYS).minusWeeks(1).plusDays(3); // Date manipulation

        Task task = new Task(1, "Ibrahim", "Complex Date Task", "Start-End Date", startDate, endDate);
        taskManager.addTask(task);

        assertTrue(task.getEndDate().isAfter(task.getStartDate())); // End date after start date
        assertEquals(26, ChronoUnit.DAYS.between(task.getStartDate(), task.getEndDate())); // Period check
        assertEquals(1, taskManager.getAllTasks().size());
    }

    // Complex Test 2: Task completion date in the past
    @Test
    void testRemoveTaskAndCompletionDateInPast() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2024, 9, 1);
        LocalDate endDate = startDate.plusWeeks(2); // Ends in mid-September

        Task task = new Task(1, "Ibrahim", "Remove Task", "Completion Test", startDate, endDate);
        taskManager.addTask(task);
        taskManager.markTaskAsCompleted(task);
        taskManager.removeTask(task);

        LocalDate completedDate = LocalDate.of(2024, 9, 18); // Set completion date in the past
        task.setCompletionDate(completedDate);

        assertTrue(task.isCompleted());
        assertTrue(task.getCompletionDate().isBefore(LocalDate.now())); // Ensure it's before "now"
        assertEquals(0, taskManager.getAllTasks().size());
    }

    // Complex Test 3: Overdue task identification using fixed date
    @Test
    void testOverdueTask() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2024, 9, 1); // Start date in the past
        LocalDate dueDate = LocalDate.of(2024, 9, 10); // Overdue by now (October 2024)

        Task task = new Task(1, "Ibrahim", "Overdue Task", "Overdue Test", startDate, dueDate);
        taskManager.addTask(task);

        assertTrue(LocalDate.now().isAfter(task.getEndDate()));
        assertEquals(1, taskManager.getPendingTasks().size());
    }

    // Complex Test 4: Shuffle tasks, check date validity
    @Test
    void testShuffleTaskAndDateValidation() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim", "Task 1", "Start Date Shift", LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 10));
        Task task2 = new Task(2, "Kevin", "Task 2", "Due Date Shift", LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 20));
        taskManager.addTask(task1);
        taskManager.addTask(task2);

        taskManager.shiftTaskAround(task2, 1); // Shift task2 position
        assertTrue(task2.getStartDate().isAfter(task1.getStartDate()));
        assertEquals(2, taskManager.getAllTasks().size());
    }

    @Test
    void testOverlappingTasksWithDifferentOwners() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        Task task2 = new Task(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.",
                LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20));
        Task task3 = new Task(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.",
                LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12));

        taskManager.addTask(task1);
        taskManager.addTask(task2);
        taskManager.addTask(task3);

        assertEquals(3, taskManager.getAllTasks().size());
        assertTrue(task1.getEndDate().isAfter(task2.getStartDate()));
        assertTrue(task2.getEndDate().isAfter(task1.getStartDate()));
    }

    @Test
    void testTaskCompletionUpdates() {
        TaskManager taskManager = new TaskManager();
        Task task = new Task(1, "Ibrahim", "Task for Completion", "Task to test completion updates.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        taskManager.addTask(task);

        task.markAsCompleted();
        task.setCompletionDate(LocalDate.now());

        assertTrue(task.isCompleted());
        assertNotNull(task.getCompletionDate());
        assertTrue(task.getCompletionDate().isAfter(task.getEndDate()));
    }

    @Test
    void testSequentialTaskDependencies() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim", "Task 1", "First task in a sequence.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 5));
        Task task2 = new Task(2, "Kevin", "Task 2", "Dependent task.",
                LocalDate.of(2024, 9, 6), LocalDate.of(2024, 9, 10));

        taskManager.addTask(task1);
        taskManager.addTask(task2);

        taskManager.markTaskAsCompleted(task1);

        assertEquals(1, taskManager.getCompletedTasks().size());
        assertTrue(task2.getStartDate().isAfter(task1.getEndDate()));
    }

    @Test
    void testTaskReassignment() {
        TaskManager taskManager = new TaskManager();
        Task task = new Task(1, "Ibrahim", "Reassign Task", "Task to test reassignment.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        taskManager.addTask(task);

        task.setOwner("Kevin");

        assertEquals("Kevin", task.getOwner());
    }

    @Test
    void testTaskWithHistoricalDatesAndCompletion() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2022, 10, 1);
        LocalDate endDate = LocalDate.of(2023, 4, 1);

        Task task = new Task(1, "Ibrahim", "Historical Completion Task", "Task with historical dates.",
                startDate, endDate);
        taskManager.addTask(task);

        task.markAsCompleted();
        task.setCompletionDate(LocalDate.now());

        assertTrue(task.isCompleted());
        assertTrue(LocalDate.now().isAfter(task.getEndDate()));
    }

    @Test
    void testTaskDurationExtension() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2024, 1, 1);
        LocalDate endDate = startDate.plusMonths(3);

        Task task = new Task(1, "Ibrahim", "Extend Duration Task", "Task to test duration extension.", startDate, endDate);
        taskManager.addTask(task);

        task.setEndDate(endDate.plusMonths(2));

        assertEquals(5, ChronoUnit.MONTHS.between(task.getStartDate(), task.getEndDate()));
    }

    @Test
    void testGetTasksOwnedBy() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        Task task2 = new Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20));
        Task task3 = new Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12));

        taskManager.addTask(task1);
        taskManager.addTask(task2);
        taskManager.addTask(task3);

        List<Task> ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim");
        List<Task> kevinTasks = taskManager.getTasksOwnedBy("Kevin");

        assertEquals(2, ibrahimTasks.size());
        assertEquals(1, kevinTasks.size());
        assertTrue(ibrahimTasks.contains(task1));
        assertTrue(ibrahimTasks.contains(task3));
        assertTrue(kevinTasks.contains(task2));
    }

    @Test
    void testUpdateOwnerAndGetTasksOwnedBy() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        Task task2 = new Task(2, "Kevin", "Task 2", "Task owned by Kevin.",
                LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20));
        Task task3 = new Task(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12));

        taskManager.addTask(task1);
        taskManager.addTask(task2);
        taskManager.addTask(task3);

        List<Task> ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim");
        List<Task> kevinTasks = taskManager.getTasksOwnedBy("Kevin");

        assertEquals(2, ibrahimTasks.size());
        assertEquals(1, kevinTasks.size());
        assertTrue(ibrahimTasks.contains(task1));
        assertTrue(ibrahimTasks.contains(task3));
        assertTrue(kevinTasks.contains(task2));

        // let's update the owners
        task2.setOwner("Ibrahim");

        ibrahimTasks = taskManager.getTasksOwnedBy("Ibrahim");

        assertEquals(3, ibrahimTasks.size());
        assertTrue(ibrahimTasks.contains(task1));
        assertTrue(ibrahimTasks.contains(task2));
        assertTrue(ibrahimTasks.contains(task3));
    }
}
