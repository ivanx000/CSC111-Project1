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
            new_location_id = current_location.available_commands[command]
            new_location = self._game.get_location(new_location_id)
            new_event = Event(new_location_id, new_location.long_description, command)

            self._events.add_event(new_event, command)
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

    win_walkthrough = ["no", "go east", "pick up", "go west", "go south",
                       "no", "pick up", "go south", "no", "go east", "go east", "submit"]
    # "no" does not get added to the event log
    expected_log = [1, 2, 2, 1, 4, 4, 5, 6, 6, 7]
    sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    assert expected_log == sim.get_id_log()

    lose_demo = ["no", "pick up", "go east", "pick up", "go east", "no", "drop", "quit"]
    # "no" does not get added to the event log
    # "quit" does not quit the game, in this case, it is to cancel the drop. It also doesn't get added to the event log
    expected_log = [1, 1, 2, 2, 3, 3]
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    assert expected_log == sim.get_id_log()

    inventory_demo = [..., "inventory", ...]
    expected_log = []
    sim = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    assert expected_log == sim.get_id_log()

    scores_demo = ["no", "score", "pick up", "go east", "go east", "no", "drop", "phone", "score", "quit"]
    # checks score, should be 0 at first. After you drop an item, you get points and the score should update.
    expected_log = [1, 1, 1, 2, 3, 3, 3]
    sim = AdventureGameSimulation('game_data.json', 1, scores_demo)
    assert expected_log == sim.get_id_log()

    puzzle_demo = ["yes", "quit"]
    # "yes" means you accept the puzzle
    expected_log = [1]
    sim = AdventureGameSimulation('game_data.json', 1, puzzle_demo)
    assert expected_log == sim.get_id_log()

    # Note: You can add more code below for your own testing purposes
