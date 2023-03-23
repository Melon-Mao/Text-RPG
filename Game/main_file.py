# This is a text based rpg game that I am working on. It is a work in progress.
# ! Add enemies

# ------------------ Importing Modules ------------------ #

import random
from time import sleep
import os
import copy
import pickle
import abc
import map
from map import sprint


# ------------------ Attack Move Class ------------------ #


class AttackMove:
    def __init__(
        self, name: str, damage: int, defensive: bool = False, defense_bonus: int = 0
    ):
        self.name = name
        self.damage = damage
        self.defensive = defensive
        self.defense_bonus = defense_bonus


# ------------------ Setting Character ------------------ #


class Character(abc.ABC):
    # Prevent this class from being instantiated
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, name, health, attack, defense, magic):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.level = 0
        self.exp = 0
        self.gold = 0
        self.points = 5
        self.attack_moves = []

    def __str__(self):
        return f"Class: {self.__class__.__name__}, Name: {self.name}, Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Magic: {self.magic}, Level: {self.level}"

    def attack_enemy(self, enemy):
        # damage = self.attack - enemy.defense
        # if damage < 0:
        #     damage = 0
        # enemy.health -= damage
        # sprint(f"You attacked the {enemy.name} for {damage} damage!", delay=0.03)
        # sleep(1)
        sprint("Choose an attack move: ")
        for i, move in enumerate(self.attack_moves):
            sprint(f"{i + 1}. {move.name}")

        chosen_move = ""
        while True:
            try:
                chosen_move = int(input("> "))
                if chosen_move > len(self.attack_moves):
                    raise ValueError
                break
            except ValueError:
                sprint("Please enter a valid number.")

        sprint(f"You used {self.attack_moves[chosen_move - 1].name}!")
        sleep(1)
        damage_dealt = self.attack_moves[chosen_move - 1].damage - enemy.defense
        if damage_dealt < 0:
            damage_dealt = 0

        sprint(f"You dealt {damage_dealt} damage to the {enemy.name}!")
        sleep(1)

        return damage_dealt, chosen_move


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 100, 15, 10, 5)
        self.attack_moves = [
            AttackMove("Slash", 10),
            AttackMove("Stab", 15),
            AttackMove("Bash", 20),
            AttackMove("Shield Block", 0, True, 5),
        ]


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 75, 5, 5, 15)


class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, 50, 15, 0, 5)


classes_list = ["Warrior", "Mage", "Rogue"]

# ------------------ Character Selection ------------------ #


def character_selection() -> Character:
    sprint("What do you want your character's name to be?")
    name = input("> ")
    sleep(1)
    sprint("Please select a class: ")
    sprint("Classes:")
    sprint(classes_list)

    chosen_class = ""
    while chosen_class not in classes_list:
        try:
            chosen_class = input("> ").capitalize()
            sleep(1)
            if chosen_class not in classes_list:
                sprint(
                    "Sorry, that is not a valid class. Please try again.\n", delay=0.03
                )
                sleep(1)
                raise ValueError
            break
        except ValueError:
            pass
    player = eval(f"{chosen_class}('{name}')")

    return player


# ------------------ Enemy Class ------------------ #


class Enemy:
    def __init__(self, name, difficulty, health, attack, defense, magic, biome):
        self.name = name
        self.difficulty = difficulty
        self.health = health
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.biome = biome

    def __str__(self):
        return f"Name: {self.name}, Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Magic: {self.magic} Biome: {self.biome}"

    def attack_player(self, player, chosen_move):
        sprint(f"\nThe {self.name} is attacking you!")
        chosen_move = player.attack_moves[chosen_move - 1]
        if chosen_move.defensive:
            sprint("Attempting to parry...")
            player.defense += chosen_move.defense_bonus
            sleep(1)
            damage = self.attack - player.defense
            if damage < 0:
                damage = 0

            if damage == 0:
                sprint("You parried the attack!")
                sleep(1)
            else:
                sprint("You failed to parry the attack!")
            player.defense -= chosen_move.defense_bonus
            sleep(1)

        damage = self.attack - player.defense
        if damage < 0:
            damage = 0

        player.health -= damage
        sprint(f"The {self.name} attacked you for {damage} damage!", delay=0.03)
        sleep(1)


# ------------------ Enemy Selection ------------------ #

enemy_data = {
    "House": {
        "Goblin": Enemy("Goblin", 10, 50, 10, 5, 0, "Forest"),
        "Orc": Enemy("Orc", 5, 100, 15, 10, 0, "Forest"),
        "Skeleton": Enemy("Skeleton", 9, 50, 10, 5, 0, "Forest"),
        "Troll": Enemy("Troll", 30, 150, 20, 15, 0, "Forest"),
    }
}


def enemy_selection(game_data):
    # Each enemy has a biome and a minimum difficulty. The biome is the biome that the enemy is in. The minimum difficulty is the minimum difficulty that the enemy can spawn in. The difficulty is out of 100. The higher the difficulty, the more likely the enemy will spawn.
    biome = game_data.area.biome

    # enemy = random.choice(list(enemy_data[biome].values()))

    # Loop through enemies in biome
    valid_enemies = []
    for enemy in enemy_data[biome].values():
        # Check if enemy difficulty is less than or equal to the area difficulty
        if enemy.difficulty <= game_data.area.difficulty:
            valid_enemies.append(enemy)

    enemy = random.choices(
        valid_enemies, weights=[enemy.difficulty for enemy in valid_enemies], k=1
    )
    # The first enenmy in the list is likely to be the enemy with the lowest diffculty.

    return enemy[0]


# ------------------ Battle System ------------------ #


def roll_for_battle(game_data):
    """This function rolls for a battle. The difficulty for every area is out of 100. The function will roll a number. If the number is less than or equal to the difficulty, then a battle will occur. If the number is greater than the difficulty, then it will return False.

    Args:
        game_data (GameData): The current game data.

    Returns:
        bool: A boolean value that determines if a battle will occur.
    """

    rolled_num = random.randint(1, 100)
    if rolled_num <= game_data.area.difficulty:
        return True
    else:
        return False


def battle(game_data):  # ! WIP

    if not roll_for_battle(game_data):
        return

    # Create a copy of the enemy in the data
    enemy = copy.deepcopy(enemy_selection(game_data))

    os.system("cls")
    print("-" * 50)
    sprint(f"You have encountered a {enemy.name}!", delay=0.03)
    sprint(f"It has {enemy.health} health!", delay=0.03)
    sprint(f"Your health is {game_data.player.health}", delay=0.03)
    sleep(1)

    while True:
        print("-" * 50)
        sprint("| What do you want to do? |", delay=0.03)
        print("-" * 50)
        sprint("| 1. Attack               |", delay=0.03)
        sprint("| 2. Magic                |", delay=0.03)
        sprint("| 3. Run                  |", delay=0.03)
        sprint("| 4. Exit                 |", delay=0.03)
        print("-" * 50)

        user_input = input("> ").lower()

        if user_input == "1" or user_input == "attack":
            damage_dealt, chosen_move = game_data.player.attack_enemy(enemy)
            enemy.health -= damage_dealt
            if enemy.health <= 0:
                sprint("You have defeated the enemy!")
                sprint(f"Current Health: {game_data.player.health}")
                sleep(1)
                break
            else:
                enemy.attack_player(game_data.player, chosen_move)
                if game_data.player.health <= 0:
                    sprint("You have died!")
                    sleep(1)
                    break
        elif user_input == "2" or user_input == "magic":
            game_data.player.magic_attack(enemy)
        elif user_input == "3" or user_input == "run":
            game_data.player.run()
        elif user_input == "4" or user_input == "exit":
            exit()
        else:
            sprint("Sorry, that is not a valid option. Please try again.", delay=0.03)
            sleep(1)
            continue

        print("-" * 50)
        sprint(f"{game_data.player.name}'s Health: {game_data.player.health}")
        sprint(f"{enemy.name}'s Health: {enemy.health}")
        sleep(1)


# ------------------ Stats ------------------ #


def upgrade_stats(player):
    if player.points == 0:
        sprint("You have no points left.")
        sleep(1)
        return player
    sprint("Please select a stat to upgrade: ")
    sprint("1. Health")
    sprint("2. Attack")
    sprint("3. Defense")
    sprint("4. Magic")
    sprint("5. Exit")

    user_input = input("> ")
    sleep(1)
    if user_input == "1":
        player.health += 10
        player.points -= 1
        sprint("You have upgraded your health by 10.", delay=0.03)
        sprint(f"You have {player.points} points left.\n")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "2":
        player.attack += 5
        player.points -= 1
        sprint("You have upgraded your attack by 5.", delay=0.03)
        sprint(f"You have {player.points} points left.\n")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "3":
        player.defense += 5
        player.points -= 1
        sprint("You have upgraded your defense by 5.", delay=0.03)
        sprint(f"You have {player.points} points left.\n")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "4":
        player.magic += 5
        player.points -= 1
        sprint("You have upgraded your magic by 5.", delay=0.03)
        sprint(f"You have {player.points} points left.\n")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "5":
        sprint("You have exited the upgrade menu.")
        sleep(1)
    else:
        sprint("Sorry, that is not a valid option. Please try again.\n", delay=0.03)
        sleep(1)
        upgrade_stats(player)

    return player


# ------------------ Interact ------------------ #


def interact(game_data):
    sprint("\nWhat do you want to do?")
    sprint("1. Move zone")
    sprint("2. Move area")
    sprint("3. View stats")
    sprint("4. Upgrade stats")
    sprint("5. Save game")
    sprint("6. Exit game")

    user_input = input("> ")
    sleep(1)
    print()

    if user_input == "1":
        game_data.zone, game_data.area = game_data.zone.move()
        sleep(1)
        # interact(game_data)
    if user_input == "2":
        game_data.area = game_data.area.move_area()
        sleep(1)
        interact(game_data)
    elif user_input == "3":
        print(game_data.player)
        sleep(1)
        interact(game_data)
    elif user_input == "4":
        game_data.player = upgrade_stats(game_data.player)
        interact(game_data)
    elif user_input == "5":
        game_data.save_menu()
        interact(game_data)
    elif user_input == "6":
        sprint("Do you want to save your game before exiting?(y/n)", delay=0.03)
        user_input2 = input("> ").lower()
        if user_input2 == "y":
            game_data.save_menu()
        elif user_input2 == "n":
            sprint("You have returned to main menu.", delay=0.03)
            game_data.game_is_running = False
            sleep(1)
            main_menu(game_data)
        else:
            sprint("Sorry, that is not a valid option. Please try again.\n")
            sleep(1)
            interact(game_data)
    else:
        sprint("Sorry, that is not a valid option. Please try again.\n")
        sleep(1)
        interact(game_data)


# ------------------ Start Game ------------------ #


def start_game():
    player = character_selection()

    current_zone = map.zone_data["A1"]
    current_area = map.area_data["A1"]["Home"]

    game_data = GameData(
        player=player,
        zone=current_zone,
        area=current_area,
        moveable_zones=["A2", "B1"],
        game_is_running=True,
    )
    sprint(
        "\nYou wake up. Where are you? You realise, this is your home. Last you remember, you were off on an adventure looking for treasure. How did you end up back here?"
    )
    sprint("You get up and look around. It's time to go out and explore once more.\n")
    sleep(1)

    interact(game_data)


# ------------------ View Credits ------------------ #


def view_credits(game_data):
    print("--------------------------------")
    print("           Credits:")
    print("    Created by: Melon Man")
    print("    Designed by: Melon Man")
    print("   Illustrated by: Melon Man")
    print("   Hope you enjoyed the game!")
    print("--------------------------------")
    sleep(5)
    main_menu(game_data)


# ------------------ Save Data ------------------ #


class GameData:
    def __init__(
        self,
        player: Character,
        zone: map.Zone,
        area: map.Area,
        moveable_zones: list[str],
        game_is_running: bool,
    ):
        self.player = player
        self.zone = zone
        self.area = area
        self.moveable_zones = moveable_zones
        self.game_is_running = game_is_running

    def save_menu(self):
        sprint("Do you want to import or export save data?")
        sprint("1. Import")
        sprint("2. Export")
        sprint("3. Exit to Main Menu")
        sprint("4. Exit to Game")

        user_input = input("> ")
        sleep(1)

        if user_input == "1":
            self.import_data()
        elif user_input == "2":
            self.export_data()
        elif user_input == "3":
            if self.game_is_running == True:
                sprint(
                    "Do you not want to return back to the game? You may lose data. (y/n).",
                    delay=0.03,
                )
                user_input2 = input("> ").lower()
                sleep(1)

                if user_input2 == "y":
                    sprint("Returning back to save menu.")
                    sleep(1)
                    self.game_is_running = False
                    self.save_menu()
                elif user_input2 == "n":
                    sprint("Returning back to game.")
                    sleep(1)
                    return self
                else:
                    sprint(
                        "Sorry, that is not a valid option. Please try again.\n",
                        delay=0.03,
                    )
                    sleep(1)
                    self.save_menu()
            else:
                sprint("You have exited the save menu.")
                sleep(1)
                main_menu(self)

        elif user_input == "4":
            if self.game_is_running == True:
                sprint("You have exited the save menu.", delay=0.03)
                sleep(1)
                return self
            else:
                sprint(
                    "You are not currently running a game. Exiting to main menu.",
                    delay=0.03,
                )
                sleep(1)
                main_menu(self)
        else:
            sprint("Sorry, that is not a valid option. Please try again.\n", delay=0.03)
            sleep(1)
            self.save_menu()

    def export_data(self):
        sprint(
            "Please enter the name of the save file you want to export to.(1, 2 or 3) Or enter 4 to exit.",
            delay=0.03,
        )
        user_input = input("> ")
        sleep(1)

        if int(user_input) in range(1, 4):
            sprint("Are you sure, this will overwrite the save file. (y/n)", delay=0.03)
            user_input2 = input("> ").lower()
            sleep(1)

            if user_input2 == "y":
                with open(rf"Game\Save Files\save{user_input}.txt", "wb") as file:
                    pickle.dump(self, file)
                    sprint(
                        f"You have exported your save data to save{user_input}.txt",
                        delay=0.03,
                    )
                    sleep(1)
                self.save_menu()
            elif user_input2 == "n":
                sprint("You have exited the export menu.")
                sleep(1)
                self.save_menu()
            else:
                sprint(
                    "Sorry, that is not a valid option. Please try again.\n", delay=0.03
                )
                sleep(1)
                self.export_data()

        elif user_input == "4":
            print("You have exited the export menu.")
            sleep(1)
            self.save_menu()
        else:
            print("Sorry, that is not a valid option. Please try again.\n")
            sleep(1)
            self.export_data()

    def import_data(self):
        sprint(
            "Please enter the name of the save file you want to import from.(1, 2 or 3) Or enter 4 to exit.",
            delay=0.03,
        )
        user_input = input("> ")
        sleep(1)

        if int(user_input) in range(1, 4):
            sprint(
                "Are you sure, this will overwrite your current save. (y/n)", delay=0.03
            )
            user_input2 = input("> ").lower()
            sleep(1)

            if user_input2 == "y":
                with open(
                    rf"Game\Projects\Text RPG\Save Files\save{user_input}.txt", "rb"
                ) as file:
                    self = pickle.load(file)
                    sprint(f"You have imported save{user_input}.txt")
                    sleep(1)
                self.save_menu()
            elif user_input2 == "n":
                sprint("You have exited the import menu.")
                sleep(1)
                self.save_menu()
            else:
                sprint(
                    "Sorry, that is not a valid option. Please try again.\n", delay=0.03
                )
                sleep(1)
                self.import_data()
        elif user_input == "4":
            sprint("You have exited the import menu.")
            sleep(1)
            self.save_menu()
        else:
            sprint("Sorry, that is not a valid option. Please try again.\n", delay=0.03)
            sleep(1)
            self.import_data()

    def __str__(self):
        return "Player: " + str(self.player) + ""


# ------------------ Main Menu ------------------ #

# This is the main menu that the game_data will see when they start the game.
def main_menu(game_data):
    os.system("cls")
    with open(r"Game\Art\logo.txt", "r") as file:
        logo = file.read()
        sprint(logo, delay=0.001)
    sleep(1)

    sprint("--------------------------------", delay=0.03)
    sprint("Welcome To Melon Man's Text RPG!", delay=0.03)
    sprint("--------------------------------", delay=0.03)
    sprint("Please select an option:", delay=0.08)
    sprint("1. Start game", delay=0.08)
    sprint("2. Exit game", delay=0.08)
    sprint("3. View credits", delay=0.08)
    sprint("4. Open save menu", delay=0.08)
    # print("4. View help")
    # print("5. View high scores")
    # print("6. View settings")
    # print("7. View achievements")
    # print("8. View stats")
    # print("9. View inventory")
    # print("10. View quests")
    # The above are placeholders currently

    valid = False
    while not valid:
        try:
            user_input = input("> ")
            sleep(1)
            if user_input == "1":
                start_game()
                pass
            elif user_input == "2":
                exit()
            elif user_input == "3":
                view_credits(game_data)
            elif user_input == "4":
                game_data.save_menu()
            # elif user_input == "5":
            #     view_help()
            # elif user_input == "6":
            #     view_high_scores()
            # elif user_input == "7":
            #     view_settings()
            # elif user_input == "8":
            #     view_achievements()
            # elif user_input == "9":
            #     view_stats()
            # elif user_input == "10":
            #     view_inventory()
            # elif user_input == "11":
            #     view_quests()
            else:
                sprint("Sorry, that is not a valid option. Please try again.\n")
                sleep(1)
                raise ValueError
            valid = True
        except ValueError:
            pass


# ------------------ Start Game ------------------ #

if __name__ == "__main__":
    # main_menu(
    #     game_data=GameData(
    #         player=Warrior("Placeholder"),
    #         zone=map.zone_data["A1"],
    #         area=map.area_data["A1"]["Home"],
    #         moveable_zones=["A2", "B1"],
    #         game_is_running=False,
    #     )
    # )

    for i in range(100):
        enemy = battle(
            game_data=GameData(
                player=Warrior("Placeholder"),
                zone=map.zone_data["A1"],
                area=map.area_data["A1"]["Home"],
                moveable_zones=["A2", "B1"],
                game_is_running=False,
            )
        )
