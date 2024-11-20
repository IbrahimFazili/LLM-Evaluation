import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.graalvm.polyglot.Context;
import org.graalvm.polyglot.Engine;
import org.graalvm.polyglot.Source;
import org.graalvm.polyglot.Value;

import java.io.File;
import java.io.IOException;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class TaskManagerTestPythonFeedback {

    // tried to use relative path, doesn't work. should probably try to find a way to do that
//    private static final String CODE_DIRECTORY = "/Users/ibrahimfazili/OneDrive - " +
//            "Cornell University/CS6158 Software Engineering in Machine Learning/LLM-Evaluation/ConvertedCode";

    //Local path for kevin
    private static final String CODE_DIRECTORY = "/Users/kevincui/Desktop/LLM-Evaluation/ConvertedCode";

    private static final String[] PYTHON_SCRIPTS = {
            "Task.py",
            "TaskManager.py"
    };

    private static Engine sharedEngine = Engine.create();
    private Context context;
    private Value taskClass;
    private Value taskManagerClass;

    @BeforeEach
    void setUp() throws IOException {
        // Initialize the Python context before each test
        context = Context.newBuilder("python")
                .allowAllAccess(true)
                .engine(sharedEngine)
                .build();

        // the only this works for some reason
        context.eval("python", "import sys; sys.path.append('" + CODE_DIRECTORY + "')");

        // Load Python files
        loadPythonFile(context, PYTHON_SCRIPTS[0]);
        loadPythonFile(context, PYTHON_SCRIPTS[1]);

        // Access Task and TaskManager classes
        taskClass = context.getBindings("python").getMember("Task").getMember("Task");
        taskManagerClass = context.getBindings("python").getMember("TaskManager");
    }
    @Test
    void testAddTaskWithDateManipulation() {
        try {

            LocalDate startDate = LocalDate.of(2024, 10, 1);
            LocalDate endDate = startDate.plus(30, ChronoUnit.DAYS).minusWeeks(1).plusDays(3);

            Value taskInstance = taskClass.newInstance(1, "Ibrahim", "Complex Date Task", "Start-End Date",
                    startDate, endDate);
            Value taskManagerInstance = taskManagerClass.newInstance();
            taskManagerInstance.invokeMember("addTask", taskInstance);

            LocalDate taskStartDate = taskInstance.getMember("startDate").as(LocalDate.class);
            LocalDate taskEndDate = taskInstance.getMember("endDate").as(LocalDate.class);

            assertTrue(taskEndDate.isAfter(taskStartDate));

            long daysBetween = ChronoUnit.DAYS.between(taskStartDate, taskEndDate);
            assertEquals(26, daysBetween);

            Value allTasks = taskManagerInstance.invokeMember("getAllTasks");
            assertEquals(1, allTasks.getArraySize());


        } catch (Exception e) {
            System.out.println("[-] Error: " + e);
        }
    }
    @Test
    void testRemoveTaskAndCompletionDateInPast() {
        try {
            Value taskManagerInstance = taskManagerClass.newInstance();
            LocalDate startDate = LocalDate.of(2024, 9, 1);
            LocalDate endDate = startDate.plusWeeks(2);

            Value task = taskClass.newInstance(1, "Ibrahim", "Remove Task", "Completion Test", startDate, endDate);
            taskManagerInstance.invokeMember("addTask", task);
            taskManagerInstance.invokeMember("markTaskAsCompleted", task);
            taskManagerInstance.invokeMember("removeTask", task);

            LocalDate completedDate = LocalDate.of(2024, 9, 18); // Set completion date in the past
            task.putMember("completedDate", completedDate);

            assertTrue(task.getMember("completed").asBoolean());
            assertTrue(task.getMember("completedDate").asDate().isBefore(LocalDate.now()));
            assertEquals(taskManagerInstance.invokeMember("getAllTasks").getArraySize(), 0);

        } catch (Exception e) {
            System.out.println("[-] Error: " + e);
        }
    }

    @Test
    void testOverdueTask() {
        try {
            Value taskManagerInstance = taskManagerClass.newInstance();
            LocalDate startDate = LocalDate.of(2024, 9, 1);
            LocalDate endDate = LocalDate.of(2024, 9, 10);

            Value task = taskClass.newInstance(1, "Ibrahim", "Overdue Task", "Overdue Test", startDate, endDate);
            taskManagerInstance.invokeMember("addTask", task);
            assertTrue(LocalDate.now().isAfter(task.getMember("endDate").asDate()));
            assertEquals(1, taskManagerInstance.invokeMember("getPendingTasks").getArraySize());

        } catch (Exception e) {
            System.out.println("[-] Error: " + e);
        }
    }

    @Test
    void testShuffleTaskAndDateValidation() {
        try {
            Value taskManagerInstance = taskManagerClass.newInstance();
            Value task1 = taskClass.newInstance(1, "Ibrahim", "Task 1", "Start Date Shift",
                    LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 10));
            Value task2 = taskClass.newInstance(2, "Kevin", "Task 2", "Due Date Shift",
                    LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 20));
            taskManagerInstance.invokeMember("addTask", task1);
            taskManagerInstance.invokeMember("addTask", task2);
            taskManagerInstance.invokeMember("shiftTaskAround", task1, 1);

            assertEquals(2, taskManagerInstance.invokeMember("getAllTasks").getArraySize());
            assertTrue(
                    taskManagerInstance
                            .invokeMember("getAllTasks")
                            .getArrayElement(0)
                            .getMember("startDate").asDate()
                            .isAfter(taskManagerInstance.invokeMember("getAllTasks").getArrayElement(1).getMember("startDate").asDate())
            );

        } catch (Exception e) {
            System.out.println("[-] Error: " + e);
        }
    }

    @Test
    void testOverlappingTasksWithDifferentOwners(){

        Value taskManagerInstance = taskManagerClass.newInstance();
        Value task1 = taskClass.newInstance(1, "Ibrahim", "Overlapping Task 1", "This task overlaps with another task.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        Value task2 = taskClass.newInstance(2, "Kevin", "Overlapping Task 2", "This task overlaps with task 1.",
                LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20));
        Value task3 = taskClass.newInstance(3, "Ibrahim", "Overlapping Task 3", "Another overlapping task for Ibrahim.",
                LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12));

        taskManagerInstance.invokeMember("addTask", task1);
        taskManagerInstance.invokeMember("addTask", task2);
        taskManagerInstance.invokeMember("addTask", task3);

        assertEquals(3, taskManagerInstance.invokeMember("getAllTasks").getArraySize());
        assertTrue(
                task1.getMember("endDate").asDate().isAfter(task2.getMember("startDate").asDate())
        );
        assertTrue(
                task2.getMember("endDate").asDate().isAfter(task2.getMember("startDate").asDate())
        );
    }

    @Test
    void testTaskCompletionUpdates() {
        Value taskManagerInstance = taskManagerClass.newInstance();

        Value task = taskClass.newInstance(1, "Ibrahim", "Task for Completion", "Task to test completion updates.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        taskManagerInstance.invokeMember("addTask", task);

        task.invokeMember("markAsCompleted");
        task.putMember("completedDate", LocalDate.now());

        assertTrue(task.getMember("completed").asBoolean());
        assertNotNull(task.getMember("completedDate"));
        assertTrue(task.getMember("completedDate").asDate().isAfter(task.getMember("endDate").asDate()));
    }

    @Test
    void testSequentialTaskDependencies() {
        Value taskManagerInstance = taskManagerClass.newInstance();

        Value task1 = taskClass.newInstance(1, "Ibrahim", "Task 1", "First task in a sequence.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 5));
        Value task2 = taskClass.newInstance(2, "Kevin", "Task 2", "Dependent task.",
                LocalDate.of(2024, 9, 6), LocalDate.of(2024, 9, 10));

        taskManagerInstance.invokeMember("addTask", task1);
        taskManagerInstance.invokeMember("addTask", task2);

        taskManagerInstance.invokeMember("markTaskAsCompleted", task1);

        assertEquals(1, taskManagerInstance.invokeMember("getCompletedTasks").getArraySize());
        assertTrue(task2.getMember("startDate").asDate().isAfter(task1.getMember("endDate").asDate()));
    }

    @Test
    void testTaskReassignment(){
        Value taskManagerInstance = taskManagerClass.newInstance();

        Value task = taskClass.newInstance(1, "Ibrahim", "Reassign Task", "Task to test reassignment.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        taskManagerInstance.invokeMember("addTask", task);
        taskManagerInstance.invokeMember("changeOwner", "Kevin", task);

        assertEquals("Kevin", task.getMember("owner").asString());
    }

    @Test
    void testGetTasksOwnedBy(){
        Value taskManagerInstance = taskManagerClass.newInstance();

        Value task1 = taskClass.newInstance(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        Value task2 = taskClass.newInstance(2, "Kevin", "Task 2", "Task owned by Kevin.",
                LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20));
        Value task3 = taskClass.newInstance(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12));

        taskManagerInstance.invokeMember("addTask", task1);
        taskManagerInstance.invokeMember("addTask", task2);
        taskManagerInstance.invokeMember("addTask", task3);

        Value ibrahimTasksValue = taskManagerInstance.invokeMember("getTasksOwnedBy", "Ibrahim");
        Value kevinTasksValue = taskManagerInstance.invokeMember("getTasksOwnedBy", "Kevin");

        List<Value> ibrahimTasks = new ArrayList<>();
        for (int i = 0; i < ibrahimTasksValue.getArraySize(); i++) {
            ibrahimTasks.add(ibrahimTasksValue.getArrayElement(i));
        }

        List<Value> kevinTasks = new ArrayList<>();
        for (int i = 0; i < kevinTasksValue.getArraySize(); i++) {
            kevinTasks.add(kevinTasksValue.getArrayElement(i));
        }

        assertEquals(2, ibrahimTasksValue.getArraySize());
        assertEquals(1, kevinTasksValue.getArraySize());
        assertTrue(ibrahimTasks.contains(task1));
        assertTrue(ibrahimTasks.contains(task3));
        assertTrue(kevinTasks.contains(task2));
    }

    @Test
    void testUpdateOwnerAndGetTasksOwnedBy() {
        Value taskManagerInstance = taskManagerClass.newInstance();

        Value task1 = taskClass.newInstance(1, "Ibrahim", "Task 1", "Task owned by Ibrahim.",
                LocalDate.of(2024, 9, 1), LocalDate.of(2024, 9, 15));
        Value task2 = taskClass.newInstance(2, "Kevin", "Task 2", "Task owned by Kevin.",
                LocalDate.of(2024, 9, 10), LocalDate.of(2024, 9, 20));
        Value task3 = taskClass.newInstance(3, "Ibrahim", "Task 3", "Another task owned by Ibrahim.",
                LocalDate.of(2024, 9, 5), LocalDate.of(2024, 9, 12));

        taskManagerInstance.invokeMember("addTask", task1);
        taskManagerInstance.invokeMember("addTask", task2);
        taskManagerInstance.invokeMember("addTask", task3);

        Value ibrahimTasksValue = taskManagerInstance.invokeMember("getTasksOwnedBy", "Ibrahim");
        Value kevinTasksValue = taskManagerInstance.invokeMember("getTasksOwnedBy", "Kevin");

        List<Value> ibrahimTasks = new ArrayList<>();
        for (int i = 0; i < ibrahimTasksValue.getArraySize(); i++) {
            ibrahimTasks.add(ibrahimTasksValue.getArrayElement(i));
        }

        List<Value> kevinTasks = new ArrayList<>();
        for (int i = 0; i < kevinTasksValue.getArraySize(); i++) {
            kevinTasks.add(kevinTasksValue.getArrayElement(i));
        }

        assertEquals(2, ibrahimTasksValue.getArraySize());
        assertEquals(1, kevinTasksValue.getArraySize());
        assertTrue(ibrahimTasks.contains(task1));
        assertTrue(ibrahimTasks.contains(task3));
        assertTrue(kevinTasks.contains(task2));

        taskManagerInstance.invokeMember("changeOwner", "Ibrahim", task2);
        ibrahimTasksValue = taskManagerInstance.invokeMember("getTasksOwnedBy", "Ibrahim");

        ibrahimTasks = new ArrayList<>();
        for (int i = 0; i < ibrahimTasksValue.getArraySize(); i++) {
            ibrahimTasks.add(ibrahimTasksValue.getArrayElement(i));
        }

        assertEquals(3, ibrahimTasksValue.getArraySize());
        assertTrue(ibrahimTasks.contains(task1));
        assertTrue(ibrahimTasks.contains(task3));
        assertTrue(ibrahimTasks.contains(task2));
    }

    private void loadPythonFile(Context context, String fileName) throws IOException {
        File file = new File(CODE_DIRECTORY, fileName);
        Source source = Source.newBuilder("python", file).build();
        context.eval(source);
    }

}
