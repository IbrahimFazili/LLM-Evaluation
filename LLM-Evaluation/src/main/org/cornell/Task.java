package org.cornell;

import java.time.LocalDate;

public class Task {

    private int id;
    private String owner;
    private String title;
    private String description;
    private LocalDate creationDate;
    private LocalDate dueDate;
    private boolean completed;

    public Task(int id, String owner, String name, String description, LocalDate creationDate, LocalDate dueDate) {
        this.id = id;
        this.owner = owner;
        this.title = name;
        this.description = description;
        this.creationDate = creationDate;
        this.dueDate = dueDate;
        this.completed = false;
    }

    public int getId() {
        return id;
    }

    public String getOwner() {
        return owner;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public LocalDate getCreationDate() {
        return creationDate;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void markAsCompleted() {
        this.completed = true;
    }

}