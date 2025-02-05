"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        initial_location = self._game.get_location()
        first_event = Event(initial_location_id, initial_location.long_description, None, None, None)
        self._events.add_event(first_event)

        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            curr_event = Event(current_location.id_num, current_location.long_description, None, None, None)
            self._events.add_event(curr_event, command)
            if command in current_location.available_commands:
                # If it is not an available command, it is a menu command which does not change location.
                location_id = current_location.available_commands[command]
                if location_id > 0:
                    # Some available commands do not change location. This handles the case where the location changes
                    new_location = self._game.get_location(location_id)
                    current_location = new_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    win_walkthrough = ["go east", "pick up", "go west", "go south",
                       "pick up", "go south", "go east", "go east", "submit"]
    expected_log = [1, 1, 2, 2, 1, 4, 4, 5, 6, 7]
    win_sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    assert expected_log == win_sim.get_id_log()

    lose_demo = ["pick up", "go east", "pick up", "go east",
                 "drop", "go west", "go west", "go south",
                 "pick up", "go south", "go east", "pick up",
                 "go west", "drop", "go east", "go east", "submit"]
    # For drop commands, this is assuming they don't drop anything and waste the command
    expected_log = [1, 1, 1, 2, 2, 3, 3, 2, 1, 4, 4, 5, 6, 6, 5, 5, 6, 7]
    lose_sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    assert expected_log == lose_sim.get_id_log()

    inventory_demo = ["inventory", "pick up", "inventory", "quit"]
    expected_log = [1, 1, 1, 1, 1]
    inventory_sim = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    assert expected_log == inventory_sim.get_id_log()

    scores_demo = ["score", "pick up", "go east", "go east", "drop", "phone", "score", "quit"]
    # checks score, should be 0 at first. After you drop an item, you get points and the score should update.
    expected_log = [1, 1, 1, 1, 2, 3, 3, 3, 3]
    scores_sim = AdventureGameSimulation('game_data.json', 1, scores_demo)
    assert expected_log == scores_sim.get_id_log()

    time_demo = ["time", "pick up", "time", "go east", "time", "quit"]
    # checks time, should be 150 at first. After you do an action, the time should update accordingly.
    expected_log = [1, 1, 1, 1, 1, 2, 2]
    time_sim = AdventureGameSimulation('game_data.json', 1, time_demo)
    assert expected_log == time_sim.get_id_log()

    puzzle_demo = ["yes", "quit"]
    # "yes" means you accept the puzzle
    # Because of how puzzles are made, to test it, you must run the adventure.py file and play the game.

    # Note: You can add more code below for your own testing purposes
