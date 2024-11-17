package cornell;

import java.util.ArrayList;
import java.util.List;

public class TaskManager {
    private final List<Task> tasks = new ArrayList<>();

    public void addTask(Task task) {
        tasks.add(task);
    }

    public void removeTask(Task task) {
        tasks.remove(task);
    }

    public void markTaskAsCompleted(Task task) {
        if (tasks.contains(task)) {
            task.markAsCompleted();
        }
    }

    public List<Task> getAllTasks() {
        return new ArrayList<>(tasks);
    }

    public List<Task> getPendingTasks() {
        List<Task> pendingTasks = new ArrayList<>();
        for (Task task : tasks) {
            if (!task.isCompleted()) {
                pendingTasks.add(task);
            }
        }
        return pendingTasks;
    }

    public List<Task> getCompletedTasks() {
        List<Task> completedTasks = new ArrayList<>();
        for (Task task : tasks) {
            if (task.isCompleted()) {
                completedTasks.add(task);
            }
        }
        return completedTasks;
    }

    public void shiftTaskAround(Task task, int position) {
        if (position >= tasks.size() || !tasks.contains(task)){
            return;
        }
        tasks.remove(task);
        tasks.add(position, task);
    }

    public List<Task> getTasksOwnedBy(String owner) {
        List<Task> rlTask = new ArrayList<>();
        for (Task t: tasks) {
            if (t.getOwner().equals(owner)) {
                rlTask.add(t);
            }
        }
        return rlTask;
    }

    public void changeOwner(String owner, Task task) {
        if (tasks.contains(task)) {
            int i = tasks.indexOf(task);
            tasks.get(i).setOwner(owner);
        }
    }
}
