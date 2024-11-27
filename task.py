from datetime import datetime
from reminder import Reminder
from tag import Tag

import re
from tag import Color
def extract_rgb_values(rgb_str):
    if rgb_str == "red":
        return 255, 0, 0
    elif rgb_str == "green":
        return 0, 255, 0
    elif rgb_str == "blue":
        return 0, 0, 255
    elif rgb_str == "yellow":
        return 255, 255, 0
    elif rgb_str == "black":
        return 0, 0, 0
    elif rgb_str == "white":
        return 255, 255, 255
    """Extract and return the integer values of r, g, b from an RGB string."""
    # 使用正则表达式提取数值部分
    pattern = r'rgb\((\s*\d{1,3}\s*,\s*){2}\s*\d{1,3}\s*\)'
    match = re.match(pattern, rgb_str)
    
    if not match:
        raise ValueError("Invalid RGB string format")
    
    # 提取数值
    rgb_values = re.findall(r'\d{1,3}', rgb_str)
    
    # 转换为整数
    r = int(rgb_values[0])
    g = int(rgb_values[1])
    b = int(rgb_values[2])
    
    # 检查数值范围
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("RGB values must be between 0 and 255")
    
    return r, g, b

class Task:
    def __init__(
            self,
            id: int, 
            category, 
            title: str, 
            description: str, 
            due_date, 
            reminder: Reminder,
            tag = [],
            timeline_name = None
            ):
        self.id = id
        from category import Category
        if category is not None:
            self.category = Category(id=category["id"], name=category["name"])
        else:
            self.category = Category(id=None, name="default")
        self.title = title
        self.description = description
        if type(due_date) is datetime:
            self.due_date = due_date
        elif type(due_date) is str:
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError("Due date must be a datetime object or a string in %Y-%m-%d %H:%M:%S format.")
        self.tags = [Tag(id=i, name=tag[i]["name"], color=tag[i]["color"]) for i in range(len(tag))]
        if type(reminder) is Reminder:
            self.reminder = reminder
        elif type(reminder) is dict:
            self.reminder = Reminder(time=reminder["time"], message=reminder["message"])
        else:
            self.reminder = Reminder(time=None, message="No reminder set.")
        assert timeline_name is not None, "Timeline must be provided."
        self.timeline_name = timeline_name
    
    def __str__(self):
        ret = f"""Task: {self.title}\n""" + \
                    f"""due_time:({self.due_date})\n""" + \
                    f"""category: {self.category.name}\n""" + \
                    f"""description: {self.description}\n"""
        for tag in self.tags:
            r, g, b = extract_rgb_values(tag.color)
            ret += f"""tag: \033[38;2;{r};{g};{b}m{tag.name}\033[0m\n"""
        ret += f"""reminder time: {self.reminder.to_dict()["time"]}\n""" + \
                    f"""reminder message: {self.reminder.to_dict()["message"]}"""
        return ret

    @property
    def title(self):
        """Get the title of the task."""
        return self._title
    
    @title.setter
    def title(self, value):
        """Set the title of the task."""
        if value == "":
            raise ValueError("Title cannot be empty.")
        elif len(value) > 50:
            raise ValueError("Title cannot exceed 50 characters.")
        elif type(value) is not str:
            raise ValueError("Title must be a string.")
        else:
            self._title = value

    @property
    def description(self):
        """Get the description of the task."""
        return self._description
    
    @description.setter
    def description(self, value):
        """Set the description of the task."""
        if len(value) > 500:
            raise ValueError("Description cannot exceed 500 characters.")
        elif type(value) is not str:
            raise ValueError("Description must be a string.")
        else:
            self._description = value

    @property
    def due_date(self):
        """Get the due date of the task."""
        return self._due_date
    
    @due_date.setter
    def due_date(self, value):
        """Set the due date of the task."""
        if type(value) is not datetime:
            raise ValueError("Due date must be a datetime object.")
        else:
            self._due_date = value

    @property
    def reminder(self):
        """Get the reminder of the task."""
        return self._reminder

    @reminder.setter
    def reminder(self, value):
        """Set the reminder of the task."""
        if type(value) is not Reminder:
            raise ValueError("Reminder must be a Reminder object.")
        else:
            self._reminder = value

    def set_due_date(self, date: datetime):
        self.due_date = date
        print(f"Due date updated to: {self.due_date}")

    def set_reminder(self, reminder: Reminder):
        self.reminder = reminder
        print(f"Reminder set for task: {self.title}")

    def add_tag(self):
        """Add a tag to the task."""
        name = input("Enter tag name: ")
        print("Tag color options: red, green, blue, yellow, black, white or rgb(r, g, b)")
        color = input("Enter tag color: ")
        tag = Tag(name=name, color=color)
        self.tags.append(tag)
        print(f"Tag '{tag.name}' added to task: {self.title}")

    def rm_tag(self):
        """Remove a tag from the task."""
        for i in range(len(self.tags)):
            print(f"Tag id: {i}, name: {self.tags[i].name}")
        print("Select tag id to remove tag.")
        while True:
            try:
                tag_id = int(input())
                if tag_id in range(len(self.tags)):
                    self.tags.pop(tag_id)
                    print(f"Tag removed from task: {self.title}")
                    break
                else:
                    print("Invalid tag id.")
            except ValueError:
                print("Invalid input.")

    def edit(self):
        try:
            title = input("Enter task title or [Enter] for continue: ")
            if title != "":
                self.title = title
            description = input("Enter task description or [Enter] for continue: ")
            if description != "":
                self.description = description
            due_date = input("Enter task due date (YYYY-MM-DD HH:MM:SS) or [Enter] for continue: ")
            if due_date != "":
                self.due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
            reminder_time = input("Enter reminder time (YYYY-MM-DD HH:MM:SS) or [Enter] for continue: ")
            reminder = None
            if reminder_time != "":
                reminder_message = input("Enter reminder message: ")
                reminder = Reminder(time=reminder_time, message=reminder_message)
                self.cancel_reminder()
                self.reminder = reminder
            print(f"Finish modifying task: {self.title}")
        except ValueError as e:
            print(e)

    def cancel_reminder(self):
        if self.reminder.time is not None:
            self.reminder.stop_flag = True
            self.reminder = Reminder(time=None, message="No reminder set.")
        
    def add_to_category(self, category):
        l = len(category)
        for i in range(l):
            print(f"Category id: {i}, name: {category[i].name}")
        print("Select category id to add task.")
        while True:
            try:
                category_id = int(input())
                if category_id in range(l):
                    from category import Category
                    if self.category.id is not None:
                        for i in range(l):
                            if category[i].name == self.category.name:
                                category[i].tasks.remove(self)
                                break
                    self.category = Category(id=category[category_id].id, name=category[category_id].name)
                    if self not in category[category_id].tasks:
                        category[category_id].tasks.append(self)
                    
                    break
                else:
                    print("Invalid category id.")
            except ValueError:
                print("Invalid input.")

    def get_tags(self):
        return self.tags
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category.to_dict(),
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d %H:%M:%S"),
            "tags": [tag.to_dict() for tag in self.tags],
            "reminder": self.reminder.to_dict(),
            "timeline": self.timeline_name
        }