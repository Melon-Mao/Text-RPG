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

# TODO: Add areas to zones, and add items to areas.

# ------------------ Importing Modules ------------------ #

# import generator type hint

from typing import Generator, Any
import random
from time import sleep
import matplotlib.pyplot as plt
import networkx as nx

# ------------------ Slow Print Function ------------------ #


# Define the function
def sprint(
    text: str | tuple[str, ...] | Any,
    delay: float = 0.05,
    sep: str = "",
    end: str = "\n",
) -> None:
    """Prints text with a delay between each character.

    Args:
        text (str): The text to be printed.
        delay (float, optional): The delay between each character. Defaults to 0.05.
        sep (str, optional): The separator between each character. Defaults to "".
        end (str, optional): The end of the print. Defaults to "\n".

    """
    # Check if the text is a tuple
    if type(text) in (list, tuple, set, dict):
        # If it is, loop through it
        for string in text:
            # And loop through the string
            for char in str(string):
                # Print each character with a delay
                print(char, end=sep, flush=True)
                sleep(delay)
            print(end=end, flush=True)
    else:  # For type str or anything else.
        for char in str(text):
            print(char, end=sep, flush=True)
            sleep(delay)
        print(end=end, flush=True)


# ------------------ Zone & Area names ------------------ #

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

area_descriptions: dict[str, list[tuple[str, str]]] = {
    "A1": [
        (
            "Home",
            "This is your home, it is quite small but it's all you need. You didn't always live here thuough. In fact, you moved in quite recently. You don't remember why you decided to move here or where you came from originally. Not yet at least.",
        ),
        (
            "Abandoned House",
            "This appears to be an abandoned house. It is very dark and eerie. Who knows what could be inside? You're not sure if you want to find out.",
        ),
        (
            "Lake",
            "A tranquil, soothing lake. It is very peaceful here. You can't imagine finding anything dangerous here.",
        ),
    ],
    "A2": [
        (
            "Ruins",
            "This is a ruin of an old building. It is very old and looks like it could collapse at any moment.",
        ),
        (
            "Shack",
            "This looks to be too small to house a human, be careful. You can neer be sure in a world like this.",
        ),
        (
            "Small Cave",
            "This is a small cave, you can almost see the end of it. Shouldn't be too dangerous.",
        ),
    ],
    "A3": [
        (
            "Forest",
            "A dense forest. You can only peer a few metres in. The trees seem to go up to the sky.",
        ),
        (
            "Grove",
            "A small grove of trees, sectioned off from the rest of the forest. Something feels off putting and you aren't sure what.",
        ),
        (
            "Elven Outpost",
            "A small elven outpost next to the forest. It should be safe here, just don't agravate the elves.",
        ),
    ],
    "A4": [
        (
            "Shrubbery",
            "A small patch of grass and bushes, a few critters scurrying about. Nothing more than that.",
        ),
        (
            "Grassy Field",
            "A large, green, grassy field. The sky is bright blue and the sun is shining. What a beautiful place.",
        ),
        (
            "River",
            "You can see a river flowing through the field, The water splashes as it hits the rocks making up the river bed.",
        ),
    ],
    "A5": [
        (
            "Spring",
            "A spring surrounded by bright flourishing flowers. It seems that these flowers bloom all year round. The water is shallow enough for you, or for a small creature, to walk in.",
        ),
        (
            "Dark Pit",
            "This seems to be quite a deep pit. You can go down a bit but afterwards it's too dark to see.",
        ),
    ],
}

# List 10 ideas for an area:
areas_ideas = [
    "Dungeon",
    "Cave",
    "Forest",
    "Town",
    "Village",
    "Castle",
    "House",
    "Shop",
    "Cemetery",
    "Graveyard",
]
areas_ideas2 = []

# ------------------ Map Class ------------------ #


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


class Zone:
    """Creates a zone object, which is a location on the map."""

    def __init__(
        self,
        name: str,
        description: str,
        is_player_here: bool = False,
        map: Map = Map(5, 5, zone_names),
        areas: list[tuple[str, str]] = [],
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
        self.areas: list[tuple[str, str]] = areas

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

    def move(self) -> tuple["Zone", "Area"]:
        """Moves the player to a new zone."""

        sprint("Where would you like to move?")
        sprint("You can move to the following zones:")
        for i, zone in enumerate(self.moveable_zones):
            print(f"{i + 1}. {zone}")
            sleep(0.5)

        sprint("Enter the corresponding number of the zone you would like to move to: ")

        valid = False
        user_input = ""
        while not valid:
            try:
                user_input = input("> ")
                sleep(1)

                if int(user_input) not in range(1, len(self.moveable_zones) + 1):
                    sprint("That is not a valid option. Please try again.")
                    sleep(1)
                    raise ValueError
                valid = True
            except ValueError:
                pass

        self.remove_player()
        new_zone_name = self.moveable_zones[int(user_input) - 1]

        sprint(f"You have moved to {new_zone_name}.")
        sleep(1)

        new_zone: Zone = zone_data[new_zone_name]
        new_zone.place_player()

        # When the player moves to a new zone, they'll be placed in the first area of that zone.

        new_area_name = new_zone.areas[0][0]
        new_area = area_data[new_zone.name][new_area_name]

        return new_zone, new_area

    def __str__(self) -> str:
        return f"Name: {self.name}, Description: {self.description}"


# ------------------ Area Class ------------------ #


class Area(Zone):
    def __init__(
        self,
        parent_zone: Zone,
        name: str,
        description: str = "",
        is_player_here: bool = False,
    ):
        self.parent_zone: Zone = parent_zone
        self.name = name
        self.description = description
        self.is_player_here = is_player_here
        self.moveable_areas: list[tuple[str, str]] = self.get_moveable_areas()

        # self.items: list["Item"] = []
        # self.npcs: list["NPC"] = []
        # self.enemies: list["Enemy"] = []

    def get_moveable_areas(self) -> list[tuple[str, str]]:
        area_descript = area_descriptions[self.parent_zone.name][:]
        # Copies a part of the area_descriptions list, so that the original list is not modified.
        # I tried it without [:] but that created a reference instead of a copy.
        area_descript.remove((self.name, self.description))
        # Before I tried to return the list.remove() but it returned None because it modifies the list,
        # instead of creating a new one.
        return area_descript

    def move_area(self) -> "Area":
        sprint("Where would you like to move?")
        sprint("You can move to the following areas:")
        for i, area in enumerate(self.moveable_areas):
            print(f"{i + 1}. {area[0]}")
            sleep(0.5)

        sprint("Enter the corresponding number of the area you would like to move to: ")

        valid = False
        user_input = ""
        while not valid:
            try:
                user_input = input("> ")
                sleep(1)

                if int(user_input) not in range(1, len(self.moveable_areas) + 1):
                    sprint("That is not a valid option. Please try again.")
                    sleep(1)
                    raise ValueError
                valid = True
            except ValueError:
                pass

        self.remove_player()
        new_area_name = self.moveable_areas[int(user_input) - 1][0]
        new_area_description = self.moveable_areas[int(user_input) - 1][1]

        sprint(f"You have moved to: {new_area_name}.")
        sleep(1)

        new_area: Area = area_data[self.parent_zone.name][new_area_name]

        new_area.place_player()

        return new_area

    def __str__(self) -> str:
        return f"Name: {self.name}, Description: {self.description}"


# ------------------- Zone & Area Data ------------------- #


zone_data: dict[str, Zone] = {
    "A1": (
        a1 := Zone(
            "A1",
            "This is the starting zone.",
            areas=area_descriptions["A1"],
        )
    ),
    "A2": (a2 := Zone("A2", "This is the second zone.")),
    "A3": (a3 := Zone("A3", "This is the third zone.")),
    "A4": (a4 := Zone("A4", "This is the fourth zone.")),
    "A5": (a5 := Zone("A5", "This is the fifth zone.")),
    "B1": (b1 := Zone("B1", "This is the sixth zone.")),
    "B2": (b2 := Zone("B2", "This is the seventh zone.")),
    "B3": (b3 := Zone("B3", "This is the eighth zone.")),
    "B4": (b4 := Zone("B4", "This is the ninth zone.")),
    "B5": (b5 := Zone("B5", "This is the tenth zone.")),
    "C1": (c1 := Zone("C1", "This is the eleventh zone.")),
    "C2": (c2 := Zone("C2", "This is the twelfth zone.")),
    "C3": (c3 := Zone("C3", "This is the thirteenth zone.")),
    "C4": (c4 := Zone("C4", "This is the fourteenth zone.")),
    "C5": (c5 := Zone("C5", "This is the fifteenth zone.")),
    "D1": (d1 := Zone("D1", "This is the sixteenth zone.")),
    "D2": (d2 := Zone("D2", "This is the seventeenth zone.")),
    "D3": (d3 := Zone("D3", "This is the eighteenth zone.")),
    "D4": (d4 := Zone("D4", "This is the nineteenth zone.")),
    "D5": (d5 := Zone("D5", "This is the twentieth zone.")),
    "E1": (e1 := Zone("E1", "This is the twenty-first zone.")),
    "E2": (e2 := Zone("E2", "This is the twenty-second zone.")),
    "E3": (e3 := Zone("E3", "This is the twenty-third zone.")),
    "E4": (e4 := Zone("E4", "This is the twenty-fourth zone.")),
    "E5": (e5 := Zone("E5", "This is the twenty-fifth zone.")),
}

area_data: dict[str, dict[str, Area]] = {
    "A1": {
        "Home": (
            home := Area(
                a1, area_descriptions["A1"][0][0], area_descriptions["A1"][0][1]
            )
        ),
        "Abandoned House": (
            abandoned_house := Area(
                a1, area_descriptions["A1"][1][0], area_descriptions["A1"][1][1]
            )
        ),
    }
}


if __name__ == "__main__":
    sprint("Welcome to the game!")
    map = Map(5, 5, zone_names)
    home.place_player()
    home.move_area()

# !
# ?
# //
# TODO
# *
