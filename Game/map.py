""" This module contains the classes for the map and the zones.
This is designed to be used as the mapping system for the Text-RPG game in the main_file.py file.
The map is gnereated using the networkx library, and the displayed using matplotlib.

zone_names:
    list : Contains the names of the zones that's used in the zone class.

Map:
    class : Creates the map of the game, and the methods to generate and display it.

Zone:
    class : Creates the zones of the game, and all the information about them.
    
zone_data:
    dict : Contains the data for each zone in the game.
"""

# ! Major overhaul underway.

# ------------------ Importing Modules ------------------ #

# import generator type hint

from typing import Generator
import random
from time import sleep
import matplotlib.pyplot as plt
import networkx as nx

# ------------------ Map Class ------------------ #

zone_names: list[str] = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "D1",
    "D2",
    "D3",
    "D4",
    "D5",
    "E1",
    "E2",
    "E3",
    "E4",
    "E5",
]


class Map:
    """Creates the map of the game as a networkx graph which can be displayed to the player."""

    def __init__(
        self, width: int = 5, height: int = 5, zone_names: list[str] = zone_names
    ):
        """Initialises the map class.

        Args:
            width (int, optional): Width of map. Defaults to 5.
            height (int, optional): Height of map. Defaults to 5.
            zone_names (list[str], optional): Names of zones used to create map. Defaults to zone_names.
        """

        self.width = width
        self.height = height
        self.zone_map: nx.Graph = self.create_map(zone_names)
        # I only have the widh and height to be referenced in __str__, no other use for them.

    def create_map(self, zone_names: list) -> nx.Graph:
        """Creates a map as a networkx graph using the names pf the zones.

        Args:
            zone_names (list): The names of the zones that will be used to create the map.

        Returns:
            nx.Graph: The map of the game, as a networkx graph.
        """

        zone_map = nx.Graph()
        zone_map.add_nodes_from(zone_names)  # Adds all values in iterable to the graph.

        def create_edges() -> Generator[tuple[str, str], None, None]:
            """Creates the edges for the map, connecting the nodes (zones) together.

            Yields:
                Generator[tuple[str, str], None, None]: Generator that yields a tuple containing the nodes to be connected.
            """

            for node in zone_map.nodes:
                split_name: list[str] = [x for x in node]
                # e.g. split_name = ["A", "1"], split_name[0] = "A", split_name[1] = "1"

                if split_name[0] != "A":  # checks bottom side
                    yield (node, chr(ord(split_name[0]) - 1) + split_name[1])
                # e.g. if node = "C3", then yield ("C3", "B3")
                if split_name[0] != "E":  # checks top side
                    yield (node, chr(ord(split_name[0]) + 1) + split_name[1])
                # e.g. if node = "C3", then yield ("C3", "D3")
                if split_name[1] != "1":  # checks left side
                    yield (node, split_name[0] + str(int(split_name[1]) - 1))
                # e.g. if node = "C3", then yield ("C3", "C2")
                if split_name[1] != "5":  # checks right side
                    yield (node, split_name[0] + str(int(split_name[1]) + 1))
                # e.g. if node = "C3", then yield ("C3", "C4")

                # The above if statements check if the nodes are at the side of the map,
                # and if they are, they won't yield an edge tuple.
                # e.g. if node = "A1", then it won't yield ("A1", "A0") or ("A1", "@1")

        zone_map.add_edges_from(
            create_edges()
        )  # Adds all values from generator as edges to the graph.

        return zone_map

    def print_map(self) -> None:
        """Displays the map using matplotlib and the neworkx draw function."""

        pos = {}
        for node in self.zone_map.nodes:  # Gives each node a position on the graph.
            split_name = [x for x in node]
            pos[node] = (int(split_name[1]), ord(split_name[0]) - 64)

        _, ax = plt.subplots(figsize=(5, 10))
        nx.draw(  # Draws the graph.
            self.zone_map,
            pos=pos,
            with_labels=True,
            ax=ax,
            node_size=1000,
            node_color="purple",
            font_size=15,
            font_color="white",
        )

        plt.title("Game Map")
        ax.set_axis_on()  # Axis is off by default, so this turns it on.
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

        plt.show()  # Displays the graph.

    def __str__(self) -> str:
        return f"Width: {self.width}, Height: {self.height}"


# ------------------ Zone Class ------------------ #


def sprint(text: str, delay: float = 0.05, sep: str = "", end: str = "\n") -> None:
    """Prints text with a delay between each character.

    Args:
        text (str): The text to be printed.
        delay (float, optional): The delay between each character. Defaults to 0.05.
        sep (str, optional): The separator between each character. Defaults to "".
        end (str, optional): The end of the print. Defaults to "

    """
    for char in text:
        print(char, end=sep, flush=True)
        sleep(delay)
    print(end=end, flush=True)


class Zone:
    """Creates a zone object, which is a location on the map."""

    def __init__(
        self,
        name: str,
        description: str,
        is_player_here: bool = False,
        map: Map = Map(5, 5, zone_names),
    ):
        """Initialises the zone class.

        Args:
            name (str): The name of the zone.
            description (str): A description of the zone.
            is_player_here (bool, optional): Represents if the player is in the zone. Defaults to False.
            map (Map, optional): Creates map of the game, only used here for zone_map attribute. Defaults to Map(5, 5, zone_names).
        """
        self.name = name
        self.description = description
        self.is_player_here = is_player_here
        self.zone_map: nx.Graph = map.zone_map
        self.moveable_zones: list[str] = self.get_moveable_zones()

    def get_moveable_zones(self) -> list[str]:
        """Gets a list of zones that the player can move to.

        Returns:
            list[str]: A list of zones adjacent to the current zone, that the player can move to.
        """

        moveable_zones = []

        for zone in self.zone_map.neighbors(self.name):
            moveable_zones.append(zone)

        return moveable_zones  # Returns a list of zones that the player can move to.

    def place_player(self) -> None:
        self.is_player_here = True

    def remove_player(self) -> None:
        self.is_player_here = False

    def move(self) -> None:
        """Moves the player to a new zone."""

        sprint("Where would you like to move?")
        sprint("You can move to the following zones:")
        for i, zone in enumerate(self.moveable_zones):
            print(f"{i + 1}. {zone}")
            sleep(0.5)

        sprint("Enter the number of the zone you would like to move to: ")

        valid = False
        user_input = ""
        while not valid:
            try:
                user_input = input("> ")
                sleep(1)

                if int(user_input) not in range(1, len(self.moveable_zones) + 1):
                    print("That is not a valid option.")
                    sleep(1)
                    raise ValueError
            except ValueError:
                pass

        self.remove_player()
        new_zone_name = self.moveable_zones[int(user_input) - 1]

        sprint(f"You have moved to {new_zone_name}.")
        sleep(1)

        new_zone: Zone = zone_data[new_zone_name]
        new_zone.place_player()

    def __str__(self) -> str:
        return f"Name: {self.name}, Description: {self.description}"


# ------------------ Zone Descriptions ------------------ #

# This function will create a description for the zone.
# It will use a list of adjectives, nouns, and verbs to create a description.
# For example, "This dark room smells clean."


def create_description():
    adjectives = [
        "dark",
        "mighty",
        "cold",
        "warm",
        "wet",
        "dry",
        "quiet",
        "loud",
        "smelly",
        "clean",
        "dirty",
        "empty",
        "full",
        "bright",
        "giant",
        "tiny",
        "unusual",
        "strange",
        "odd",
        "weird",
    ]
    nouns = [
        "room",
        "tower",
        "ruins",
        "bathroom",
        "bedroom",
        "hut",
        "fort",
        "basement",
        "attic",
        "garage",
        "closet",
        "office",
        "library",
        "garden",
        "yard",
        "field",
        "balcony",
        "staircase",
        "hallway",
        "hallway",
    ]
    verbs = [
        "smells",
        "feels",
        "looks",
        "sounds",
        "tastes",
        "seems",
        "feels",
        "looks",
        "sounds",
        "tastes",
        "smells",
        "feels",
        "looks",
        "sounds",
        "appears",
        "smells",
        "feels",
        "looks",
        "sounds",
        "tastes",
    ]

    return f"This {random.choice(adjectives)} {random.choice(nouns)} {random.choice(verbs)} {random.choice(adjectives)}."


# ------------------- Zone Descriptions ------------------- #

zone_data = {
    "A1": Zone("A1", "This is the starting zone."),
    "A2": Zone("A2", "This is the second zone."),
    "A3": Zone("A3", "This is the third zone."),
    "A4": Zone("A4", "This is the fourth zone."),
    "A5": Zone("A5", "This is the fifth zone."),
    "B1": Zone("B1", "This is the sixth zone."),
    "B2": Zone("B2", "This is the seventh zone."),
    "B3": Zone("B3", "This is the eighth zone."),
    "B4": Zone("B4", "This is the ninth zone."),
    "B5": Zone("B5", "This is the tenth zone."),
    "C1": Zone("C1", "This is the eleventh zone."),
    "C2": Zone("C2", "This is the twelfth zone."),
    "C3": Zone("C3", "This is the thirteenth zone."),
    "C4": Zone("C4", "This is the fourteenth zone."),
    "C5": Zone("C5", "This is the fifteenth zone."),
    "D1": Zone("D1", "This is the sixteenth zone."),
    "D2": Zone("D2", "This is the seventeenth zone."),
    "D3": Zone("D3", "This is the eighteenth zone."),
    "D4": Zone("D4", "This is the nineteenth zone."),
    "D5": Zone("D5", "This is the twentieth zone."),
    "E1": Zone("E1", "This is the twenty-first zone."),
    "E2": Zone("E2", "This is the twenty-second zone."),
    "E3": Zone("E3", "This is the twenty-third zone."),
    "E4": Zone("E4", "This is the twenty-fourth zone."),
    "E5": Zone("E5", "This is the twenty-fifth zone."),
}


# Now that I have created a grid of zones, use the zone class methods to move the player around the grid.
# I want the player to be able to move up, down, left, and right.


if __name__ == "__main__":
    sprint("Welcome to the game!")
    map = Map(5, 5, zone_names)
    # map.print_map()
    c3 = Zone(
        "C3",
        "This is the starting zone.",
    )
    print(c3.moveable_zones)
    c3.move()


# !
# ?
# //
# TODO
# *
