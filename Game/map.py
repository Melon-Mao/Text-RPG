"""
This file contains the Map class, which is used to represent the map of the game.
"""
# ! Major overhaul underway.

# ------------------ Importing Modules ------------------ #


import random
from time import sleep
import matplotlib.pyplot as plt
import networkx as nx

# ------------------ Map Class ------------------ #


class Map:  # TODO - Major overhaul of this class, including the map generation.
    def __init__(self, width, height, zone_data):
        self.width = width
        self.height = height
        self.zone_map = self.create_map(zone_data)

    # * Use the networkx library and the code at the bottom of this file to generate a map.

    def create_map(self, zone_data: dict) -> nx.Graph:
        zone_map = nx.Graph()
        zone_map.add_nodes_from(zone_data.keys())

        def create_edges():
            node = ""
            for node in zone_map.nodes:
                split_name = [x for x in node]
                if split_name[0] != "A":
                    yield (node, chr(ord(split_name[0]) - 1) + split_name[1])
                if split_name[0] != "E":
                    yield (node, chr(ord(split_name[0]) + 1) + split_name[1])
                if split_name[1] != "1":
                    yield (node, split_name[0] + str(int(split_name[1]) - 1))
                if split_name[1] != "5":
                    yield (node, split_name[0] + str(int(split_name[1]) + 1))

        zone_map.add_edges_from(create_edges())

        return zone_map

    def print_map(self):
        pos = {}
        for node in self.zone_map.nodes:
            split_name = [x for x in node]
            pos[node] = (ord(split_name[0]) - 65, int(split_name[1]) - 1)

        nx.draw(self.zone_map, pos=pos, with_labels=True)
        plt.show()

    def __str__(self):
        return f"Width: {self.width}, Height: {self.height}"


# ------------------ Zone Class ------------------ #


class Zone(Map):  # TODO - Revamp movement system with the new map.
    def __init__(self, name, description="", is_player_here=False, map=Map(5, 5)):
        self.height = map.height
        self.name = name
        self.description = description
        self.is_player_here = is_player_here
        # What other information do we need to store about a zone?
        self.tb, self.bb, self.lb, self.rb, self.loaded_zones = self.check_border()

    def place_player(self):
        self.is_player_here = True

    def remove_player(self):
        self.is_player_here = False

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"

    def check_border(self):
        loaded_zones = [self.name]
        at_top_border, at_bottom_border, at_left_border, at_right_border = (
            False,
            False,
            False,
            False,
        )
        split_name = [x for x in self.name]

        if split_name[1] == "1":
            at_top_border = True
        else:
            loaded_zones.append(split_name[0] + str(int(split_name[1]) - 1))

        if split_name[1] == str(self.height):
            at_bottom_border = True
        else:
            loaded_zones.append(split_name[0] + str(int(split_name[1]) + 1))

        if split_name[0] == "A":
            at_left_border = True
        else:
            loaded_zones.append(chr(ord(split_name[0]) - 1) + split_name[1])

        if split_name[0] == chr(self.height + 64):
            at_right_border = True
        else:
            loaded_zones.append(chr(ord(split_name[0]) + 1) + split_name[1])

        return (
            at_top_border,
            at_bottom_border,
            at_left_border,
            at_right_border,
            loaded_zones,
        )

    def move(self, game_data):
        print("Where would you like to go?")
        print("1. Up")
        print("2. Down")
        print("3. Left")
        print("4. Right")
        print("5. Exit")
        choice = input("> ")
        if choice == "1":
            self.up(game_data)
        elif choice == "2":
            self.down(game_data)
        elif choice == "3":
            self.left(game_data)
        elif choice == "4":
            self.right(game_data)
        elif choice == "5":
            pass
        else:
            print("Invalid choice.")
            sleep(1)
            self.move(game_data)

    def up(self, game_data):
        if game_data.tb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone(
                (split_name[0] + str(int(split_name[1]) - 1)),
                description=create_description(),
            )
            new_zone.place_player()
        else:
            print("You can't go any further up.")
            sleep(1)
            self.move(game_data)

    def down(self, game_data):
        if game_data.bb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone(
                (split_name[0] + str(int(split_name[1]) + 1)),
                description=create_description(),
            )
            new_zone.place_player()
        else:
            print("You can't go any further down.")
            sleep(1)
            self.move(game_data)

    def left(self, game_data):
        if game_data.lb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone(
                (chr(ord(split_name[0]) - 1) + split_name[1]),
                description=create_description(),
            )
            new_zone.place_player()
        else:
            print("You can't go any further left.")
            sleep(1)
            self.move(game_data)

    def right(self, game_data):
        if game_data.rb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone(
                (chr(ord(split_name[0]) + 1) + split_name[1]),
                description=create_description(),
            )
            new_zone.place_player()
        else:
            print("You can't go any further right.")
            sleep(1)
            self.move(game_data)


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


# !
# ?
# //
# TODO
# *
