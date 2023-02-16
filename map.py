"""
This file contains the Map class, which is used to represent the map of the game.
"""
import random
from time import sleep


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.visual_map = []
        self.detailed_map = {}


    def create_visual_map(self):
        for _ in range(self.height):
            self.visual_map.append(["□"] * self.width)
    
    def create_detailed_map(self):
        # copy the dictionary detailed_map as current_detailed_map

        for j in range(self.height):
            current_row = []
            for i in range(self.width):
                # Every time the loop runs, I want a counter to increase letter.
                # For example, the first time it will be A, then B, then C, etc.
                current_row.append([chr(i+65) + str(j + 1)])
            self.detailed_map[j+1] = current_row

        return self.detailed_map


    def print_map(self):
        for row in self.visual_map:
            print(" ".join(row))
    
    def __str__(self):
        return f"Width: {self.width}, Height: {self.height}"
    

class Zone(Map):
    def __init__(self, name, description="", is_player_here=False, map=Map(5, 5)):
        self.height = map.height
        self.name = name
        self.description = description
        self.is_player_here = is_player_here

    def place_player(self):
        self.is_player_here = True

    def remove_player(self):
        self.is_player_here = False

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"

    def check_border(self):
        loaded_zones = [self.name]
        at_top_border, at_bottom_border, at_left_border, at_right_border = False, False, False, False
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


        return at_top_border, at_bottom_border, at_left_border, at_right_border, loaded_zones
    
    def move(self, game_data):
        print("Where would you like to go?")
        print("1. Up")
        print("2. Down")
        print("3. Left")
        print("4. Right")
        print("5. Back")
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
            new_zone = Zone((split_name[0] + str(int(split_name[1]) - 1)), description=create_description())
            new_zone.place_player()
        else:
            print("You can't go any further up.")
            sleep(1)
            self.move(game_data)
    
    def down(self, game_data):
        if game_data.bb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone((split_name[0] + str(int(split_name[1]) + 1)), description=create_description())
            new_zone.place_player()
        else:
            print("You can't go any further down.")
            sleep(1)
            self.move(game_data)

    def left(self, game_data):
        if game_data.lb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone((chr(ord(split_name[0]) - 1) + split_name[1]), description=create_description())
            new_zone.place_player()
        else:
            print("You can't go any further left.")
            sleep(1)
            self.move(game_data)
    
    def right(self, game_data):
        if game_data.rb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone((chr(ord(split_name[0]) + 1) + split_name[1]), description=create_description())
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
    adjectives = ["dark", "mighty", "cold", "warm", "wet", "dry", "quiet", "loud", "smelly", "clean", "dirty", "empty", "full", "bright", "giant", "tiny", "unusual", "strange", "odd", "weird"]
    nouns = ["room", "tower", "ruins", "bathroom", "bedroom", "hut", "fort", "basement", "attic", "garage", "closet", "office", "library", "garden", "yard", "field", "balcony", "staircase", "hallway", "hallway"]
    verbs = ["smells", "feels", "looks", "sounds", "tastes", "seems", "feels", "looks", "sounds", "tastes", "smells", "feels", "looks", "sounds", "appears", "smells", "feels", "looks", "sounds", "tastes"]
    
    return f"This {random.choice(adjectives)} {random.choice(nouns)} {random.choice(verbs)} {random.choice(adjectives)}."
