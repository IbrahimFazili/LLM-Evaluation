class Task:

    def __init__(self, id, owner, name, description, start_date, end_date):
        self.id = id
        self.owner = owner
        self.title = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.completion_date = None
        self.completed = False

    def mark_as_completed(self):
        self.completed = True
