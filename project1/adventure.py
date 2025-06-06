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

from game_entities import Location, Item, Puzzle
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: integer value of the current location id
        - ongoing: boolean value to check if the game is still going
        - data: a list of inventory, score and time values

    Representation Invariants:
        - self.data[1] >= 0
        - self.data[2] >= 0
        - self.data[3] >= 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    data: list[list[Item] | int]
    required_items: set[str]
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

        self.required_items = {"USB Drive", "Laptop Charger", "Lucky Mug"}
        self.data = [[], 0, 150, 25, []]  # inventory, score, time, number of moves and dropped items

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'], loc_data['available_commands'],
                                    loc_data['items'], loc_data['Puzzle'])
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

            # If no Location object has the provided location ID, return the current location id
            return self._locations[self.current_location_id]

    def display_inventory(self) -> None:
        """Displays each item the user currently has"""
        if not self.data[0]:
            print("Your inventory is empty.")
        else:
            items = ""
            for item_obj in self.data[0]:
                items += ", " + item_obj.name

            print("Inventory:" + items[1:])

    def pickup_items(self, curr_location: Location) -> None:
        """Displays each item the player picked up and updates inventory"""
        if not curr_location.items:
            print("There are no items at this location currently.")
            return

        for item_obj in self._items:
            # This is to account for the fact that the items are listed as
            # strings in the location data instead of item objects
            if item_obj.name in curr_location.items:
                print("You picked up a: " + item_obj.name)
                curr_location.items.remove(item_obj.name)  # Updates the current locations items
                if item_obj.name in self.required_items:
                    print("You need this item to submit your project! Bring this back with you to your dorm room.")
                else:
                    print("You should drop this " + item_obj.name + " "
                          "at: " + self._locations[item_obj.target_position].name)
                self.data[0].append(item_obj)

    def display_items(self, curr_location: Location) -> None:
        """Displays each item at the players current location"""

        for item_obj in self._items:
            # This is to account for the fact that the items are listed as
            # strings in the location data instead of item objects
            if item_obj.name in curr_location.items:
                print("There is a " + item_obj.name + " at this location")

    def drop_item(self, curr_location: Location) -> None:
        """Handles drop item case"""
        if not self.data[0]:  # No items in inventory
            print("There are no items to drop.")
        else:  # There are items
            possible_items = ['quit']
            print("Available items to drop: (Keep in mind you cannot get this item back. "
                  "If you change your mind, enter quit) ")
            for item_obj in self.data[0]:
                print("-" + item_obj.name)
                possible_items.append(item_obj.name.lower())
            drop_choice = input("\nEnter item or quit: ").lower().strip()
            while drop_choice not in possible_items:
                print("You do not have that item; try again or quit.")
                drop_choice = input("\nEnter item: ").lower().strip()

            if drop_choice == "quit":
                print("You dropped nothing.")
                return

            game.remove_item(drop_choice, curr_location)

    def remove_item(self, drop_choice: str, curr_location: Location) -> None:
        """Removes item from inventory after dropping it"""
        print("You decided to drop: " + drop_choice)
        for item_obj in self.data[0]:
            if item_obj.name.lower() == drop_choice:
                if item_obj.target_position == curr_location.id_num:
                    print("You gained " + str(item_obj.target_points) + " points!")
                    self.data[1] += item_obj.target_points
                self.data[4].append(item_obj)
                self.data[0].remove(item_obj)
                return

    def display_score(self) -> None:
        """Displays the current score"""
        print("Your score is: " + str(self.data[1]))

    def update_time(self, command: str, curr_location: Location) -> None:
        """Updates the time based on the choice of the user"""
        if command in menu:
            self.data[2] -= menu[command]
        if command in curr_location.available_commands:
            self.data[2] -= 10  # A command for specific locations account for more time compared to menu options

    def submit(self) -> None:
        """Win condition of the game, submits the assignment"""
        inventory_names = {item.name for item in self.data[0]}
        if self.required_items.issubset(inventory_names):  # Player has all the required items
            if self.data[2] > 0:  # Player returned all the items on time
                print("Congratulations! You made it back to your dorm room in "
                      "time with all your items and you submitted your assignment on time.")
                game.quit()
            else:  # Player has all items but did not make it in time
                if (self.data[2] + self.data[1]) > 0:  # Player accumulated enough points so they still win
                    print("You made it back with all your items, but the deadline has already passed. "
                          "However, the instructor decided to give you an extension due to your extra points. "
                          "Congratulations!")
                    game.quit()
                else:  # Player just loses
                    print("You made it back with all your items, but the deadline has already passed. You failed.")
                    game.quit()
        else:  # Player does not have all the required items
            missing_items = list(self.required_items - inventory_names)
            print("The items you are missing are:")
            for missing in missing_items:
                print("- " + missing)

            print("Please come back with the required items.")

    def quit(self) -> None:
        """Quit function, ends the game"""
        self.ongoing = False

    def undo(self) -> None:
        """Undo the player's most recent action."""

        if game_log.is_empty():
            print("There aren't any actions to undo!")
            return

        last_event = game_log.last
        # Gives the user back the time that they lost from the command they chose
        if last_event.prev.next_command in menu:  # next_command is a menu command
            self.data[2] += menu[last_event.prev.next_command]
        else:  # next_command is a location specific command
            self.data[2] += 10
            if last_event.prev.next_command == "drop":  # If player drops an item and does undo, they get it back
                self.data[0].append(self.data[4].pop())
        self.current_location_id = last_event.prev.id_num
        game_log.remove_last_event()

    def display_time(self) -> None:
        """Displays the amount of time before deadline"""

        print("You have " + str(self.data[2]) + " minutes left before the deadline.")

    def encountered_puzzle(self) -> None:
        """Handles puzzle case"""
        possible_choices = ['yes', 'no']
        print("You have encountered a puzzle! Would you like to do it? You will not get this option again.")
        puzzle_choice = input("\nEnter Yes/No: ").lower().strip()
        while puzzle_choice not in possible_choices:
            print("That was an invalid input; try again.")
            puzzle_choice = input("\nEnter Yes/No: ").lower().strip()

        if puzzle_choice == "yes":
            location.has_puzzle = False
            current_puzzle = Puzzle()
            print("Here is a scrambled word: " + current_puzzle.scrambled)
            print("You have " + str(current_puzzle.tries) + " tries to unscramble this word.")
            while current_puzzle.tries > 0:
                guess = input("\nEnter guess: ").lower().strip()
                if guess == current_puzzle.random_word:
                    print("Congratulations! You unscrambled the word " + current_puzzle.random_word + ".")
                    print("You gained " + str(current_puzzle.points) + " points.")
                    self.data[1] += current_puzzle.points
                    return
                else:
                    print("Wrong answer! Try again.")
                current_puzzle.tries -= 1
        else:
            location.has_puzzle = False
            return

        print("You failed the puzzle. The word was: " + current_puzzle.random_word + ". Better luck next time!")


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = {
        "look": 5,
        "inventory": 5,
        "score": 0,
        "undo": 0,
        "log": 0,
        "quit": 0,
        "time": 0
    }  # A mapping of menu options to the time (in minutes) it takes for each option
    choice = None

    # Objective: get back to dorm before deadline with required items, return extra items for more points

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        # Total number of moves is 25, if they exceed it, they fail.
        if game.data[3] == 0:
            print("The deadline has passed. You failed.")
            game.quit()

        location = game.get_location()

        curr_event = Event(location.id_num, location.long_description, None, None, None)
        # Everything that is None gets handled by add_event()
        game_log.add_event(curr_event, choice)

        if location.visited:
            print("LOCATION: " + location.name)
            print(location.brief_description)
        else:
            print("LOCATION: " + location.name)
            print(location.long_description)
            location.visited = True

        # If there is a puzzle at the location they are at, ask if they want to do it.
        if location.has_puzzle:
            game.encountered_puzzle()

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit, time")
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
            if choice == "score":
                game.display_score()
            if choice == "undo":
                game.undo()
            if choice == "log":
                game_log.display_events()
            if choice == "quit":
                game.quit()
            if choice == "time":
                game.display_time()

        else:
            # Handle non-menu actions
            if choice == "drop":
                game.drop_item(location)
            elif choice == "pick up":
                game.pickup_items(location)  # only locations with items have the available command "pick up"
            elif choice == "submit":
                game.submit()
            else:
                result = location.available_commands[choice]
                game.current_location_id = result  # Updates location

        game.update_time(choice, location)
        game.data[3] -= 1
