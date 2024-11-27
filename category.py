from task import Task

class Category:
    def __init__(self, id: int, name: str, tasks = [], timelines = []):
        self.id = id
        self.name = name
        # self.tasks = [
        #     Task(
        #         tasks[i]["id"], 
        #         {"id": id, "name": name}, 
        #         tasks[i]["title"], 
        #         tasks[i]["description"], 
        #         tasks[i]["due_date"], 
        #         tasks[i]["reminder"],
        #         tasks[i]["tag"],
        #         tasks[i]["timeline_id"]
        #         )
        #     for i in range(len(tasks))
        # ]
        self.tasks = []
        for task in tasks:
            t = task["timeline"]
            for i in timelines:
                if i.name == t:
                    t = i
                    break
            for i in t.tasks:
                if i.id == task["id"]:
                    self.tasks.append(i)
                    break

    def __str__(self):
        return f"Category: {self.name}"

    @property
    def name(self):
        """Get the name of the category."""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set the name of the category."""
        if value == "":
            raise ValueError("Category name cannot be empty.")
        elif len(value) > 50:
            raise ValueError("Category name cannot exceed 50 characters.")
        elif type(value) is not str:
            raise ValueError("Category name must be a string.")
        else:
            self._name = value

    def display(self):
        """Display the category."""
        print(f"Category name: {self.name}")
        for task in self.tasks:
            print(f"{str(task)}")

    def add_task(self, task: Task):
        """Add a task to the category."""
        self.tasks.append(task)
        print(f"Task '{task.title}' added to category: {self.name}")

    def rm_task(self, task_id: int):
        """Remove a task from the category."""
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                print(f"Task with ID {task_id} removed from category: {self.name}")
                return
        print(f"Task with ID {task_id} not found in category: {self.name}")

    def get_tasks(self):
        """Get all tasks in the category."""
        return self.tasks
    
    def to_dict(self) -> dict:
        """Convert the category to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "tasks": [task.to_dict() for task in self.tasks]
        }