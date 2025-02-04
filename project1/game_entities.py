"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
import requests
import random


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: id of this location
        - name: name of this location
        - brief_description: brief description of this location
        - long_description: long description of this location
        - available_commands: a mapping of available commands at this location to
                                the location executing that command would lead to
        - items: a list of all the items at this location
        - visited: a boolean value to check if this location has been visited

    Representation Invariants:
        - self.name != ''
        - self.brief_description != ''
        - self.long_description != ''
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool
    has_puzzle: bool

    def __init__(self, location_id, name, brief_description, long_description, available_commands, items,
                 has_puzzle, visited=False) -> None:
        """Initialize a new location.

        """

        self.id_num = location_id
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited
        self.has_puzzle = has_puzzle


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of this item
        - start_position: starting position of this item
        - target_position: the location ID of where the item is to be deposited for credit
        - target_points: points rewarded for depositing the item in target_position

    Representation Invariants:
        - self.name != ''
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    start_position: int
    target_position: int
    target_points: int


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.
class Puzzle:
    """A word puzzle in our text adventure game

    Instance Attributes:
        - random_word: A random word
        - scrambled: random_word but scrambled
        - tries: The amount of tries the player gets to unscramble the word
        - points: The amount of points for unscrambling the word

    Representation Invarients:
        - self.random_word != ""
        - self.scrambled != ""
        - self.points >= 0
    """

    random_word: str
    scrambled: str
    tries: int
    points: int

    def __init__(self) -> None:
        """Initializes a new Puzzle"""

        self.random_word = self.get_random_word()
        self.scrambled = self.scramble_word(self.random_word)
        self.tries = 3
        self.points = 5

    def get_random_word(self) -> str:
        """Generates a new random word"""
        response = requests.get("https://random-word-api.herokuapp.com/word")
        return response.json()[0] if response.status_code == 200 else "error"

    def scramble_word(self, word: str) -> str:
        """Scrambles word"""
        if len(word) <= 1:
            return word  # No need to scramble single-letter words

        word_list = list(word)
        random.shuffle(word_list)  # Shuffle the letters
        return ''.join(word_list)


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
