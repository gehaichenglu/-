"""User moduler"""
from datetime import datetime
from reminder import Reminder
from category import Category
from tag import Tag
from task import Task


class User:
    """User class."""
    def __init__(self, id: int, username: str, password: str, timelines = [], categories = []):
        self.id = id
        self.username = username
        self.password = password
        from timeline import Timeline
        self.timelines = [Timeline(i, self, timelines[i]["name"], timelines[i]["tasks"])
                        for i in range(len(timelines))]
        self.categories = [Category(i, categories[i]["name"], categories[i]["tasks"],
                                    self.timelines)
                        for i in range(len(categories))]

    @property
    def username(self):
        """Get the username of the user."""
        return self._username

    @username.setter
    def username(self, value):
        if value == "":
            raise ValueError("Username cannot be empty.")
        elif len(value) > 16:
            raise ValueError("Username cannot exceed 16 characters.")
        elif isinstance(value, str) is False:
            raise ValueError("Username must be a string.")
        else:
            self._username = value

    @property
    def password(self):
        """Get the password of the user."""
        return self._password

    @password.setter
    def password(self, value):
        if value == "":
            raise ValueError("Password cannot be empty.")
        elif len(value) > 16:
            raise ValueError("Password cannot exceed 16 characters.")
        elif isinstance(value, str) is False:
            raise ValueError("Password must be a string.")
        else:
            self._password = value

    def add_timeline(self):
        """Add a timeline for the user."""
        from timeline import Timeline
        while True:
            try:
                name = input("Enter timeline name or [Enter] for back: ")
                if name == "":
                    return
                for timeline in self.timelines:
                    if timeline.name == name:
                        raise ValueError("Timeline name already exists.")
                self.timelines.append(Timeline(len(self.timelines), self, name))
                print(f"Timeline {name} added for user: {self.username}")
                break
            except ValueError as e:
                print(e)

    def rm_timeline(self):
        """Remove a timeline for the user."""
        from timeline import Timeline
        print("Remove timeline")
        for i in range(len(self.timelines)):
            print(f"Timeline id {i}: {self.timelines[i].name}")
        id = -1
        while id not in range(len(self.timelines)):
            print(f"id must be in range of [0,{len(self.timelines)-1}]")
            try:
                id = input("Enter timeline id or [Enter] for back: ")
                if id == "":
                    return
                id = int(id)
            except ValueError:
                print("id must be an integer.")
                id = -1
        t = self.timelines[int(id)]
        self.timelines.remove(t)
        for c in self.categories:
            for task in c.tasks:
                if task.timeline_name == t.name:
                    c.tasks.remove(task)
        print(f"Timeline {t.name} removed for user: {self.username}")

    def display_timelines(self):
        """Display all timelines for the user."""
        for i in range(len(self.timelines)):
            print(f"Timeline {i}: {self.timelines[i].name}")
            self.timelines[i].display()

    def get_timelines(self):
        """Get all timelines for the user."""
        return self.timelines

    def add_category(self):
        """Add a category for the user."""
        while True:
            try:
                name = input("Enter category name or [Enter] for back: ")
                if name == "":
                    return
                for c in self.categories:
                    if c.name == name:
                        raise ValueError("Category name already exists.")
                self.categories.append(Category(len(self.categories), name))
                print(f"Category {name} added for user: {self.username}")
                break
            except ValueError as e:
                print(e)

    def rm_category(self):
        """Remove a category for the user."""
        for i in range(len(self.categories)):
            print(f"Category id {i}: {self.categories[i].name}")
        id = -1
        while id not in range(len(self.categories)):
            print(f"id must be in range of [0,{len(self.categories)-1}]")
            try:
                id = input("Enter category id or [Enter] for back: ")
                if id == "":
                    return
                id = int(id)
            except ValueError:
                print("id must be an integer.")
                id = -1
        c = self.categories[int(id)]
        self.categories.remove(c)
        for timeline in self.timelines:
            for task in timeline.tasks:
                if task.category.name == c.name :
                    task.category = Category(None, "Default")
        print(f"Category {c.name} removed for user: {self.username}")

    def display_categories(self):
        """Display all categories for the user."""
        for i in range(len(self.categories)):
            print(f"Category {i}: {self.categories[i].name}")
            self.categories[i].display()

    def to_dict(self):
        """Convert the user to a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "timelines": [t.to_dict() for t in self.timelines],
            "categories": [c.to_dict() for c in self.categories]
        }
