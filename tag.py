"""Tag module."""
from enum import Enum
import re


class Color(Enum):
    """Color enum."""
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    WHITE = "white"

class Tag:
    """Tag class."""
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    @property
    def name(self):
        """Get the name of the tag."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name of the tag."""
        if value == "":
            raise ValueError("Tag name cannot be empty.")
        elif len(value) > 50:
            raise ValueError("Tag name cannot exceed 50 characters.")
        elif isinstance(value, str) is False:
            raise ValueError("Tag name must be a string.")
        else:
            self._name = value

    @property
    def color(self):
        """Get the color of the tag."""
        return self._color

    @color.setter
    def color(self, value):
        """Set the color of the tag."""

        def is_valid_rgb(rgb_str):
            """Check if the RGB string is valid."""
            pattern = r'^rgb\((\s*\d{1,3}\s*,\s*){2}\s*\d{1,3}\s*\)$'
            match = re.match(pattern, rgb_str)

            if not match:
                return False
            rgb_values = re.findall(r'\d{1,3}', rgb_str)
            for value in rgb_values:
                if not 0 <= int(value) <= 255:
                    return False
            return True
        if value not in [color.value for color in Color] and not is_valid_rgb(value):
            raise ValueError("Invalid color.")
        else:
            self._color = value

    def to_dict(self) -> dict:
        """Convert the tag to a dictionary."""
        return {
            "name": self.name,
            "color": self.color
        }
