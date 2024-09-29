package org.cornell;

import java.util.ArrayList;
import java.util.List;

public class TaskManager {
    private final List<Task> tasks = new ArrayList<>();

    public void addTask(Task task) {
        tasks.add(task);
        notifyObservers("Task added: " + task.getTitle());
    }

    public void removeTask(Task task) {
        tasks.remove(task);
        notifyObservers("Task removed: " + task.getTitle());
    }

    public void markTaskAsCompleted(Task task) {
        if (tasks.contains(task)) {
            task.markAsCompleted();
            notifyObservers("Task completed: " + task.getTitle());
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

    // Notify observers (for event handling)
    private void notifyObservers(String message) {
        // Implementation for notifying observers can go here
        System.out.println(message);
    }
}
