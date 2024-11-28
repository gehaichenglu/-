"""Reminder module."""
from datetime import datetime
import threading

def remind(reminder):
    """Remind the user."""
    while not reminder.stop_flag:
        threading.Event().wait(0.5)
        if reminder.time <= datetime.now():
            reminder.trigger()
            break

class Reminder:
    """Reminder class."""
    def __init__(self, time: datetime, message: str):
        if type(time) is datetime:
            self.time = time
        elif type(time) is str:
            self.time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        else:
            self.time = None
        self.message = message
        if self.time is not None:
            self.schedule()

    @property
    def time(self):
        """Get the time of the reminder."""
        return self._time

    @time.setter
    def time(self, value):
        """Set the time of the reminder."""
        if type(value) is not datetime and value is not None:
            raise ValueError("Time must be a datetime object.")
        else:
            self._time = value

    @property
    def message(self):
        """Get the message of the reminder."""
        return self._message

    @message.setter
    def message(self, value):
        """Set the message of the reminder."""
        if value == "":
            raise ValueError("Message cannot be empty.")
        elif len(value) > 100:
            raise ValueError("Message cannot exceed 100 characters.")
        elif type(value) is not str:
            raise ValueError("Message must be a string.")
        else:
            self._message = value

    def schedule(self):
        """Schedule the reminder."""
        print(f"Set Reminder for {self.time}: {self.message}")
        self.stop_flag = False
        self.thread = threading.Thread(target=remind, args=(self,))
        self.thread.start()

    def trigger(self):
        """Trigger the reminder."""
        print(f"Reminder triggered at {self.time}. Message: {self.message}")
        # TODO: Implement more notification

    def to_dict(self) -> dict:
        """Convert the reminder to a dictionary."""
        if self.time is None:
            return {
                "time": None,
                "message": self.message
            }
        else:
            return {
                "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
                "message": self.message
            }
