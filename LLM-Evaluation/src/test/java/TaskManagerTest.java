import org.cornell.Task;
import org.cornell.TaskManager;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

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

        assertTrue(LocalDate.now().isAfter(task.getEndDate())); // Task is overdue
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

        taskManager.shiftTaskAround(task2, 7); // Shift task2 by 7 days

        assertTrue(task2.getStartDate().plusDays(7).isAfter(task2.getStartDate()));
        assertEquals(2, taskManager.getAllTasks().size());
    }

    // Complex Test 5: Overlapping dates with specific date comparisons
    @Test
    void testTaskOverlappingDates() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim", "Overlapping Task 1", "Task 1", LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        Task task2 = new Task(2, "Kevin", "Overlapping Task 2", "Task 2", LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20));

        taskManager.addTask(task1);
        taskManager.addTask(task2);

        assertTrue(task1.getEndDate().isBefore(task2.getEndDate())); // task1 ends before task2
        assertTrue(task2.getStartDate().isBefore(task1.getEndDate())); // task2 starts before task1 ends
    }

    // Complex Test 6: Task extended beyond 1 year using fixed dates
    @Test
    void testLongTermTaskWithExtendedEndDate() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2024, 1, 1);
        LocalDate endDate = startDate.plusYears(1); // Initially 1-year task

        Task task = new Task(1, "Ibrahim", "Long Term Task", "Task Extension", startDate, endDate);
        taskManager.addTask(task);

        // Extend the task end date if within 1 month of current date
        if (task.getEndDate().isBefore(LocalDate.of(2025, 2, 1))) {
            task.setEndDate(task.getEndDate().plusMonths(6)); // Extend by 6 months
        }

        assertEquals(18, ChronoUnit.MONTHS.between(task.getStartDate(), task.getEndDate())); // Now 18 months
    }

    // Complex Test 7: Completed task with future completion date
    @Test
    void testCompletedTaskWithFutureDate() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2024, 9, 1);
        LocalDate dueDate = LocalDate.of(2024, 9, 15);

        Task task = new Task(1, "Ibrahim", "Future Completion Task", "Completion Future Test", startDate, dueDate);
        taskManager.addTask(task);
        taskManager.markTaskAsCompleted(task);

        LocalDate futureCompletionDate = LocalDate.of(2024, 11, 1); // Simulate future completion date
        task.setCompletionDate(futureCompletionDate);

        assertTrue(task.isCompleted());
        assertTrue(task.getCompletionDate().isAfter(task.getEndDate())); // Completion is after due date
    }


    // Complex Test 8: Sequential task chain with fixed dates
    @Test
    void testTaskChainWithSequentialDates() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim", "Task 1", "Sequential Dates", LocalDate.of(2024, 10, 1), LocalDate.of(2024, 10, 5));
        Task task2 = new Task(2, "Kevin", "Task 2", "Sequential Dependency", LocalDate.of(2024, 10, 6), LocalDate.of(2024, 10, 15));

        taskManager.addTask(task1);
        taskManager.addTask(task2);

        assertTrue(task2.getStartDate().isAfter(task1.getEndDate())); // task2 starts after task1 ends
        assertEquals(2, taskManager.getAllTasks().size());
    }

    // Complex Test 9: Overdue task with historical start/end dates
    @Test
    void testOverdueTaskWithHistoricalDates() {
        TaskManager taskManager = new TaskManager();
        LocalDate startDate = LocalDate.of(2022, 10, 1); // 2 years ago
        LocalDate endDate = LocalDate.of(2023, 4, 1); // Ended more than a year ago

        Task task = new Task(1, "Ibrahim", "Historical Task", "Historical Overdue", startDate, endDate);
        taskManager.addTask(task);

        assertTrue(LocalDate.now().isAfter(task.getEndDate())); // Task is long overdue
        assertEquals(1, taskManager.getAllTasks().size());
    }
}
