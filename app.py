import json
from category import Category
from reminder import Reminder
from tag import Tag
from datetime import datetime
from task import Task
from user import User
from timeline import Timeline

class App:
    #TODO: implement the GUI for the app

    def run(self):
        print("Welcome!")
        print("Please login or register to continue.")
        print("1 for login. 2 for register.")
        i = input()
        while i not in ["1", "2"]:
            print("Invalid input. Please enter 1 or 2.")
            i = input()
        self.users = self.load()
        if i == "1":
            self.user = self.login()
        else:
            self.user = self.register()
        self.loop()


    def login(self):
        """Login to the app."""
        users = self.users
        username = input("Enter username: ")
        while username not in users:
            print("Username not found.")
            username = input("Enter username or [Enter] for register: ")
            if username == "":
                return self.register()
        password = input("Enter password: ")
        while password != users[username]["password"]:
            print("Password incorrect.")
            password = input("Enter password or [Enter] for re-input username: ")
            if password == "":
                return self.login()
        print(f"User {username} logins successfully.")
        return self.convert_to_users(self.users[username])
    
    def register(self):
        """Register a new user."""
        print("Register")
        users = self.users
        
        username = input("Enter username or [Enter] for login: ")
        while username in users:
            print("Username already exists.")
            username = input("Enter username or [Enter] for login: ")
            if username == "":
                return self.login()
        if username == "":
            return self.login()
        password = input("Enter password: ")
        #users[username] = {"password": password, "id": len(users)}
        users[username] = User(username=username, password=password, id=len(users))
        self.save()
        print(f"User {username} registers successfully.")
        return self.convert_to_users(self.users[username])
    
    def loop(self):
        """Main loop for the app."""
        user = self.user
        while True:
            print("1 for add timeline. 2 for remove timeline. ")
            print("3 for display timelines. 4 for add category.")
            print("5 for remove category. 6 for display categories.")
            print("7 for select a timeline. 8 for save.")
            print("9 for exit.")
            i = input()
            while i not in [str(x) for x in range(1, 10)]:
                print(f"Invalid input. Please enter [1,...,9].")
                i = input()
            if i == "1":
                user.add_timeline()
            elif i == "2":
                user.rm_timeline()
            elif i == "3":
                user.display_timelines()
            elif i == "4":
                user.add_category()
            elif i == "5":
                user.rm_category()
            elif i == "6":
                user.display_categories()
            elif i == "7":
                print("Select a timeline.")
                user.display_timelines()
                id = -1
                while id not in range(len(user.timelines)):
                    print(f"id must be in range of [0,{len(user.timelines)-1}]")
                    try:
                        id = input("Enter timeline id or [Enter] for back: ")
                        if id == "":
                            break
                        id = int(id)
                    except ValueError:
                        print("id must be an integer.")
                        id = -1
                if id != -1 and id != "":
                    self.timeline_loop(user, id)
            elif i == "8":
                self.save()
            else:
                break
            
    
    def timeline_loop(self, user, id):
        t = user.timelines[id]
        print("Selected timeline:", t.name)
        t.display()
        while True:
            print("1 for add task. 2 for remove task. ")
            print("3 for display tasks. 4 for back.")
            print("5 for select a task.")
            i = input()
            while i not in [str(x) for x in range(1, 6)]:
                print(f"Invalid input. Please enter [1,...,5].")
                i = input()
            if i == "1":
                t.add_task()
            elif i == "2":
                t.rm_task(user.categories)
            elif i == "3":
                t.display()
            elif i == "4":
                break
            else:
                print("Select a task.")
                t.display()
                id = -1
                while id not in range(len(t.tasks)):
                    print(f"id must be in range of [0,{len(t.tasks)-1}]")
                    try:
                        id = input("Enter task id or [Enter] for back: ")
                        if id == "":
                            break
                        id = int(id)
                    except ValueError:
                        print("id must be an integer.")
                        id = -1
                if id != -1 and id != "":
                    self.task_loop(t, id, user)
    
    def task_loop(self, timeline, id, user):
        t = timeline.tasks[id]
        print(t)
        while True:
            print("1 for edit task. 2 for add tag.")
            print("3 for delete tag. 4 for back.")
            print("5 for cancel reminder. 6 for add to category.")
            
            i = input()
            while i not in [str(x) for x in range(1, 7)]:
                print(f"Invalid input. Please enter [1,7].")
                i = input()
            if i == "1":
                t.edit()
            elif i == "2":
                t.add_tag()
            elif i == "3":
                t.rm_tag()
            elif i == "4":
                break
            elif i == "5":
                t.cancel_reminder()
            else:
                t.add_to_category(user.categories)

    def set_reminder(self):
        """Set reminder for tasks."""
        for timeline in self.user.timelines:
            for task in timeline.tasks:
                if task.reminder:
                    task.reminder.schedule()
            
    def load(self):
        """Load users from file."""
        try:
            with open('data/users.json', "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        except json.decoder.JSONDecodeError:
            users = {}
        
        return users

    def save(self):
        """Save users to file."""
        self.users[self.user.username] = self.user.to_dict()
        with open('data/users.json', 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def convert_to_users(self, user):
        """Convert dict to User objects."""
        return User(id=user["id"], username=user["username"], password=user["password"],
                          timelines=user["timelines"], categories=user["categories"]) 
                
if __name__ == "__main__":
    app = App()
    app.run()