from datetime import datetime
from reminder import Reminder
from category import Category
from tag import Tag
from task import Task
from user import User

class Timeline:
  
    def __init__(self, id, user: User, name: str, tasks = []):
        self.id = id
        self.user = user
        self.name = name
        self.tasks = [
            Task(
                i, 
                tasks[i]["category"], 
                tasks[i]["title"], 
                tasks[i]["description"], 
                tasks[i]["due_date"], 
                tasks[i]["reminder"], 
                tasks[i]["tags"],
                self.name
                )
            for i in range(len(tasks))
        ]

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if value == "":
            raise ValueError("Timeline name cannot be empty.")
        elif len(value) > 25:
            raise ValueError("Timeline name cannot exceed 25 characters.")
        elif type(value) is not str:
            raise ValueError("Timeline name must be a string.")
        else:
            self._name = value
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        if type(value) is not User:
            raise ValueError("User must be a User object.")
        else:
            self._user = value

    def display(self):
        print(f"Timeline for user: {self.user.username}")
        for i in range(len(self.tasks)):
            print(f"Task id: {i}")
            print(self.tasks[i])
        
    def add_task(self):
        """Add a task to the timeline."""
        while True:
            try:
                title = input("Enter task title or [Enter] for back: ")
                if title == "":
                    return
                description = input("Enter task description or [Enter] for back: ")
                if description == "":
                    return
                due_date = input("Enter task due date (YYYY-MM-DD HH:MM:SS) or [Enter] for back: ")
                if due_date == "":
                    return
                reminder_time = input("Enter reminder time (YYYY-MM-DD HH:MM:SS) or [Enter] for no reminder: ")
                reminder = None
                if reminder_time != "":
                    reminder_message = input("Enter reminder message: ")
                    reminder = Reminder(time=reminder_time, message=reminder_message)
                self.tasks.append(Task(
                    len(self.tasks), 
                    None, 
                    title, 
                    description, 
                    due_date, 
                    reminder, 
                    [],
                    self.name
                    ))
                print(f"Task '{title}' added to timeline: {self.name}")
                break
            except ValueError as e:
                print(e)
    
    def rm_task(self, category):
        """Remove a task from the timeline."""
        print("Remove a task from the timeline.")
        for i in range(len(self.tasks)):
            print(f"Task id {i}: {self.tasks[i]}")
        id = -1
        while id not in range(len(self.tasks)):
            print(f"id must be in range of [0,{len(self.tasks)-1}]")
            try:
                id = input("Enter task id or [Enter] for back: ")
                if id == "":
                    return
                id = int(id)
            except ValueError:
                print("id must be an integer.")
                id = -1
        t = self.tasks[int(id)]
        self.tasks.remove(t)
        print(f"Task removed for timeline: {self.name}")
        t.cancel_reminder()
        if t.category.id is not None:
            for c in category:
                if c.name == t.category.name:
                    for task in c.tasks:
                        if t.title == task.title and t.timeline_name == task.timeline_name:
                            c.tasks.remove(task)
                            return
                    break


    def to_dict(self) -> dict:
        #TODO: user
        return {
            "id": self.id,
            "name": self.name,
            "tasks": [task.to_dict() for task in self.tasks]
        }