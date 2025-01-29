"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: integer value of the current location id
        - ongoing: boolean value to check if the game is still going
        - score: the players score, which can determine if they win or not
        - inventory: inventory of all the items the player currently has
        - time: the amount time the player has before the deadline

    Representation Invariants:
        -
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    inventory: list[Item]
    score: int
    time: int
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

        self.inventory = []
        self.score = 0
        self.time = 15

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            for location_id in self._locations:
                if location_id == loc_id:
                    return self._locations[location_id]

    def display_inventory(self) -> None:
        """Displays each item the user currently has"""
        items = ""
        for item_obj in self.inventory:
            items += " " + item_obj.name

        print("Inventory:" + items)

    def display_items(self, curr_location: Location) -> None:
        """Displays each item the player picked up and updates inventory"""

        for item_obj in self._items:
            if item_obj.name in curr_location.items:
                print("You picked up a: " + item_obj.name)
                print("You need to drop " + item_obj.name + " at: " + self._locations[item_obj.target_position].name)
                self.inventory.append(item_obj)

    def drop_item(self) -> None:
        """Handles drop item case"""
        if not self.inventory:  # No items in inventory
            print("There are no items to drop.")
        else:  # There are items
            ...

    def display_score(self) -> None:
        """Displays the current score"""
        print("Your score is: " + str(self.score))

    def update_time(self, command: str, curr_location: Location) -> None:
        """Updates the time based on the choice of the user"""
        if command in menu:
            self.time -= menu[command]
        if command in curr_location.available_commands:
            self.time -= 15

    def quit(self) -> None:
        """Quit function, ends the game"""
        self.ongoing = False


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = {
        "look": 5,
        "inventory": 5,
        "drop": 5,
        "score": 5,
        "undo": 0,
        "log": 5,
        "quit": 0
    }  # A mapping of menu options to the time (in minutes) it takes for each option
    choice = None

    # Objective, get back to dorm before deadline with required items, return extra items for more points
    # 1 2 3
    # 4 -1 -1
    # 5 6 7

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing and game.time > 0:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        # Note: Print starting messages

        location = game.get_location()

        curr_event = Event(location.id_num, location.long_description, choice, None, None)
        game_log.add_event(curr_event, choice)

        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)

        # If there is an item at the location they are at, they automatically pick it up.
        # If they pick up an item, it tells them what they picked up and where they need to drop it.
        if location.items:
            game.display_items(location)
        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            if choice == "look":
                print(location.long_description)
            if choice == "inventory":
                game.display_inventory()
            if choice == "drop":
                game.drop_item()
            if choice == "score":
                game.display_score()
            if choice == "undo":
                # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
                ...
            if choice == "log":
                game_log.display_events()
            if choice == "quit":
                game.quit()

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result  # Updates location

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
