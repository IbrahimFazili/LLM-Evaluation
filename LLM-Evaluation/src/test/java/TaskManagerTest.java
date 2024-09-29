import org.cornell.Task;
import org.cornell.TaskManager;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

class TaskManagerTest {

    @Test
    void testAddTask() {
        TaskManager taskManager = new TaskManager();
        Task task = new Task(1, "Ibrahim","Create Project", "Creating Time", LocalDate.now(), LocalDate.now().plusWeeks(3L));
        taskManager.addTask(task);
        assertEquals(1, taskManager.getAllTasks().size());
    }

    @Test
    void testRemoveTask() {
        TaskManager taskManager = new TaskManager();
        Task task = new Task(1, "Ibrahim","Create Project", "Creating Time", LocalDate.now(), LocalDate.now().plusWeeks(3L));
        taskManager.addTask(task);
        taskManager.removeTask(task);
        assertEquals(0, taskManager.getAllTasks().size());
    }

    @Test
    void testMarkTaskAsCompleted() {
        TaskManager taskManager = new TaskManager();
        Task task = new Task(1, "Ibrahim","Create Project", "Creating Time", LocalDate.now(), LocalDate.now().plusWeeks(3L));
        taskManager.addTask(task);
        taskManager.markTaskAsCompleted(task);
        assertTrue(task.isCompleted());
    }

    @Test
    void testGetPendingTasks() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim","Create Project", "Creating Time", LocalDate.now(), LocalDate.now().plusWeeks(3L));
        Task task2 = new Task(2, "Kevin","Deleting Project", "Deleting Time", LocalDate.now(), LocalDate.now().plusWeeks(1L));
        taskManager.addTask(task1);
        taskManager.addTask(task2);
        taskManager.markTaskAsCompleted(task1);

        assertEquals(1, taskManager.getPendingTasks().size());
    }

    @Test
    void testGetCompletedTasks() {
        TaskManager taskManager = new TaskManager();
        Task task1 = new Task(1, "Ibrahim","Create Project", "Creating Time", LocalDate.now(), LocalDate.now().plusWeeks(3L));
        Task task2 = new Task(2, "Kevin","Deleting Project", "Deleting Time", LocalDate.now(), LocalDate.now().plusWeeks(1L));
        taskManager.addTask(task1);
        taskManager.addTask(task2);
        taskManager.markTaskAsCompleted(task1);

        assertEquals(1, taskManager.getCompletedTasks().size());
    }
}
