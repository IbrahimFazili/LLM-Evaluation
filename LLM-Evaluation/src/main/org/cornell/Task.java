package org.cornell;

import java.time.LocalDate;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Task {

    private int id;
    private String owner;
    private String title;
    private String description;
    private LocalDate startDate;
    private LocalDate endDate;
    private LocalDate completionDate;
    private boolean completed;

    public Task(int id, String owner, String name, String description, LocalDate startDate, LocalDate endDate) {
        this.id = id;
        this.owner = owner;
        this.title = name;
        this.description = description;
        this.startDate = startDate;
        this.endDate = endDate;
        this.completionDate = null;
        this.completed = false;
    }

    public void markAsCompleted() {
        this.completed = true;
    }
}