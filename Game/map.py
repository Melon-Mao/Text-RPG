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
# ! Add biomes
# TODO: add items to areas.

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


# ------------------ Zone & Area descriptions ------------------ #

zone_descriptions: list[tuple[str, str]] = [
    (
        "A1",
        "The starting zone, where your home is. There's not much here, but your prefer it that way,",
    ),
    (
        "A2",
        "The second zone. You are still close to your home, you can almost make out a vague outline of it in the distance. You shouldn't be in any danger here.",
    ),
    (
        "A3",
        "The third zone. You can truly see the beauty of the natural world, with greenery in the form of forests and groves scattered about.",
    ),
    (
        "A4",
        "The fourth zone. Nature still reigns over this part of the world. There's less trees which is made up for by the giant stretches of grass and shrubbery.",
    ),
    (
        "A5",
        "The fifth zone. A smaller zone, containing a nice spring and something that's a bit more sinister.",
    ),
    (
        "B1",
        "The sixth zone. North of your home, is a small village. People, humans, live here. Somewhere where you can feel safe in the presence of others. The village consists of a main square, surrounded by houses, shops and other buildings.",
    ),
    (
        "B2",
        "The seventh zone. On the eastern side of village, there isn't much here. The only notable thing is a farm, containing a few livestock.",
    ),
    (
        "B3",
        "The eighth zone. The further you go from the civilised world, the more dangerous it becomes. However, there may also be untold riches to be found.",
    ),
    (
        "B4",
        "The ninth zone. As you go along, things may differ from what you expect. There is a large valley here, but not much else.",
    ),
    (
        "B5",
        "The tenth zone. People of different cultures tend to make foreign things. Here, you'll find a small pond, and some other oddities.",
    ),
    (
        "C1",
        "The eleventh zone. Now north of the village, there is a well which supplies people with water. Above, are some mysteries.",
    ),
    (
        "C2",
        "The twelfth zone. You are approaching dangerous terriotry. Be wary, and check your pockets lest you've been robbed.",
    ),
    (
        "C3",
        "The thirteenth zone. Go back, you've been here long enough already. Go back.",
    ),
    (
        "C4",
        "The fourteenth zone. Safety? At least you have nature tp keep you company. It seems a bit extraordiary though.",
    ),
    (
        "C5",
        "The fifteenth zone. As arachnids scatter about from your presence, you wonder if you should turn back.",
    ),
    (
        "D1",
        "The sixteenth zone. What a breathtaking sight. These mountains are truly magnificent, stretching as far as the eye can see.",
    ),
    (
        "D2",
        "The seventeenth zone. It seems that there have been fights here. Char marks are visible on the ground and the faint smell of smoke lingers in the air.",
    ),
    (
        "D3",
        "The eighteenth zone. Beyond lies more mysteries. A strange crypt, tomb, tar? Be careful.",
    ),
    (
        "D4",
        "The nineteenth zone. Magic is in the air. That must be the case, as there's not other explanation for the most unusual atmosphere here.",
    ),
    (
        "D5",
        "The twentieth zone. You feel and overwhelming sense of dissapointment and failure, seeping out of this place. It may be best to leave, before you get affected too.",
    ),
    (
        "E1",
        "The twenty-first zone. At the road between sea and land, you can see the ocean clearly victorious. A harbour lies, sunken, fading away.",
    ),
    (
        "E2",
        "The twenty-second zone. Here, there exists a dangerous people. They do not live or fight by our rules and they are not to be trifled with. Although, there may be something of value here.",
    ),
    (
        "E3",
        "The twenty-third zone. They say nothing in life is free. To get the rewards most valuable, you must pay the price through blood, sweat and tears. A frosty mist hangs in the air, chilling your bones.",
    ),
    (
        "E4",
        "The twenty-fourth zone. Frost, bugs and fungus. What more could you ask for?",
    ),
    (
        "E5",
        "The twenty-fifth zone. Withered away, crumbling to dust. The undead seek their prey.",
    ),
]

zone_names: tuple[str, ...] = list(zip(*zone_descriptions))[0]


area_descriptions: dict[str, list[tuple[str, str]]] = {
    "A1": [
        (
            "Home",
            "This is your home, it is quite small but it's all you need. You didn't always live here though. In fact, you moved in quite recently. You don't remember why you decided to move here or where you came from originally. Not yet at least.",
        ),
        (
            "Abandoned House",
            "This house appears to have been abandoned for a long time, considering it's in a state of disrepair. Peering in, you get a feel of the dark and eerie atmosphere. You aren't sure what kind of things could be housed in such a place, and you don't really want to find out.",
        ),
        (
            "Lake",
            "A tranquil, soothing lake. It is very peaceful here, the water's still and the birds chirp in the distance. You can't imagine finding anything dangerous, though nature can be quite deceptive at times.",
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
    "B1": [
        (
            "Village Square",
            "A large, open square in the middle of the village. You see people walking around, talking to their neighbours and going about their daily lives.",
        ),
        (
            "Village Inn",
            "A small, cosy inn. You can see a few people sitting at the bar, drinking and chatting. You can also see a few people sitting at tables, eating and drinking.",
        ),
        (
            "Village Shop",
            "A small shop selling various goods. You can see a few people browsing the shelves, looking for something to buy. You can look around yourself if you want.",
        ),
        (
            "Village House",
            "It looks to be the home of one of the local villagers. I'm sure they wouldn't mind if you took a look around.",
        ),
        (
            "Village Church",
            "A small, quaint church. You can see a few people praying inside. A priest is standing at the front, giving a sermon.",
        ),
        (
            "Village Cemetery",
            "A small cemetery. You can see a few graves, some of which are covered in flowers. You can see a few people walking around, visiting the graves of their loved ones. You don't have any loved ones, at least you don't remember having any.",
        ),
        (
            "Village Brewery",
            "A small brewery. You can see a few people drinking beer at the bar. You may want to go to the counter and try to get something for yourself.",
        ),
        (
            "Village Wall",
            "A giant stone wall surrounds the village. You can see a few guards patrolling. What thing could possibly require the construction a wall such as this?",
        ),
    ],
    "B2": [
        (
            "Village Outskirts",
            "The outskirts of the village. You have to be a bit more careful, there must be a reason why the village hasn't expanded this far.",
        ),
        (
            "Farm",
            "A modest farm that operates at the outskirts of the village. You can see a few people working in the fields, herding cattle and tending to the crops.",
        ),
    ],
    "B3": [
        (
            "Mysterious Vault",
            "A mysterious vault. It is covered in sheets of steel. There is no way you could open it, without the right tools",
        ),
        (
            "Lone Tree",
            "At the end of the forest lies a single tree. It is distict from the rest of the nature around, towering over the clouds.",
        ),
        (
            "Orchard",
            "You see a small group of trees, all bearing bright fruit. The aroma is intoxicating, drawing you in. You can see a few people picking the fruit, this must be their livelihood.",
        ),
        (
            "Orcish Hunting Party",
            "A small group of orcs are hunting distant from their main camp. They are brutish warriors, you should be careful. Their presence may prove to be a threat to the village nearby.",
        ),
    ],
    "B4": [
        (
            "Elven Idol",
            "A large idol of an elven god. It seems to be contructed out of stone, though the details have be lost to time.",
        ),
        (
            "Valley",
            "A vast valley, streatching as far as the eye can see. It seems empty though, strangely so.",
        ),
    ],
    "B5": [
        (
            "Spiritual Mound",
            "A large mound of dirt and grass in the middle of field. It seems out of place, perhaps it is a grave of some sort. You have to be careful, you don't want to disturb the dead.",
        ),
        (
            "Large Cave",
            "A large cave, you aren't sure what lies inside. You can hear the scurrying of tiny creatures and the dripping of water from the roof. It certainly gives off a creepy, ominous vibe. One thing is for sure, there is some danger inside.",
        ),
        (
            "Spider Den",
            "The entrance to the den of a spider. These arachnids give you the creeps, with the way the scitter along the walls and catch their prey in webs. Hopefuly you aren't their prey.",
        ),
        (
            "Pond",
            "A small pond, surrounded by pebbles and grass. This seems to be the only normal thing here. You should rest, while you can.",
        ),
    ],
    "C1": [
        (
            "Village Well",
            "A well found past the northern border of the village. It seems that these peopl didn't have the ability to hide it behind their walls. You can see a few people carrying buckets of water, presumably to their homes.",
        ),
        (
            "Mountainous Path",
            "A path leading up a mountain. It seems to have been cobbled together by the villagers with rocks and dirt. You aren't sure why though, as there doesn't seem to be anyone using it.",
        ),
        (
            "Hill",
            "A moderately sized hill located near the cobbled path. It seems that this is only the start of a mountain range. You see a few goats grazing up on the hill, they do have a great ability to climb.",
        ),
    ],
    "C2": [
        (
            "Shaman Shrine",
            "A shrine coated by layers of decay. A skull, attached to a stick had been put at the top of the shrine, indicating it's relation to shamanism. You must be careful, these tribalistic people are known to be quite hostile, especially if you are an outsider in their sacred lands.",
        ),
        (
            "Goblin Camp",
            "A camp of goblins. They seem to be quite hostile, running about frenziedly and attacking anything that moves. You must be careful, while one of them may be weak, they have no obligation to fight fair.",
        ),
        (
            "Pasture",
            "A field of well kept grass, just north of the farm. You can see a a few cows grazing on the grass, content with their lives. Spears scattered around indicate that goblins frequently raid this area.",
        ),
        (
            "Blacksmith Remnants",
            "The remains of a rather grandiouse looking blacksmith. It must have been the destructive goblins that destroyed and looted it. Perhaps you can salvage somthing from the remains.",
        ),
    ],
    "C3": [
        (
            "Monolith",
            "Unamed soul, turn back now. That is the only warning you will recieve.",
        ),
    ],
    "C4": [
        (
            "Mystical Forest",
            "A forest of mystical proportions. You see no further than a metre or two as the trees look over you, seemingly as judges. It's humorous, perhaphs they know you more than you know yourself.",
        ),
        (
            "Clearing",
            "A small clearing in the middle of the forest. Here you can really feel the presence of the cyan and magenta trees as they surround you. It should feel menacing but it doesn't. You could almost say it feels like home.",
        ),
        (
            "Fallen Tree",
            "With a base as wide as a house and roots that peer into the Earth's core, you wander how such a tree could have even wobbled. It seems that some created have made the sleeping giant their home, skittering about.",
        ),
        (
            "Engravings",
            "Near the fallen tree, lies a stone slab with engravings carved into it. The runes seem to have a faint, enchanting glow that you would have missed if you were only walking by. They mean something, you are sure of it, but it would take something special to decipher them.",
        ),
    ],
    "C5": [
        (
            "Spider Nest",
            "So this is where they come from. The thought of there being hundreds, if not thousands of these creepy arachnids in one place is enough to make you shiver. Wherever there is a nest, there is a queen. Be careful.",
        ),
        (
            "Silk Vein",
            "A large vein of silk, wrapped around trees and rocks. It is important to not disturb it, as you feel some sort of life force emanating from it. Perhaps it would be best to leave this place.",
        ),
        (
            "Carcase",
            "The carcass of a large animal. The flesh has been stripped entirely and all that remains is a skeleton of a once great creature. You can see the pure white colour of silk against the yellowish decaying bones. Spiders, you think to yourself.",
        ),
        (
            "Elven Arch",
            "A large arch, with the apparant architercture of elves. The walls are built from chiseled stone slabs and there seems to be openings at the two top corners, a safe place to shoot arrows from. In an area festering with nightmares, it makes sense these peaceful people would need something like this.",
        ),
    ],
    "D1": [
        (
            "Hidden Mountain Pass",
            "You have found a path hidden from the main path. Perhaps this is why the villagers cobbled together a crude road. Be wary, you don't know what lies ahead.",
        ),
        (
            "Dwarven Temple",
            "A temple engineered by dwarves. You can tell by the unqiue architecture, including the way the stones are cut and placed to form a circular base. You see what seem to be dwarves, with their red beards and warrior like appearance, walking around the temple.",
        ),
        (
            "Dwarven Forge",
            "A forge, used by the dwarves to make their weapons and armour. You can see a few pieces lying around, crafted using various materials. Perhaps you can take some for yourself.",
        ),
        (
            "Large Mountain",
            "You see a mountain so tall it reaches the clouds. You can't help but feel small in comparison, wondering if you could ever reach the top. You see what you make out to be dwarves, going up and down the mountain, carrying various materials.",
        ),
    ],
    "D2": [
        (
            "Dwarven Guard Post",
            "This place is flocking with dwarves, suited with the best armour one could make. The abnormal presence could be due to the raiding goblins. After all, you wouldn't want some green skinned thieves to ransack your home.",
        ),
        (
            "Destroyed Camp",
            "A camp that looks familiar. The low quality leather used for the tents indicate that these belonged to the goblins. The green blood splattered might also suggest that. There must have been a recent skirmish.",
        ),
        (
            "Burning Burial Site",
            "The smell of burning flesh is repungent. You can make out some of the skulls that are being engulfed in flames. They are goblins, you are sure of it. Despite the the trouble that they cause to every livig being, you cannot help but feel a little sorry for them. What transgression could have warranted this?",
        ),
    ],
    "D3": [
        (
            "Quarry",
            "You see a large quarry, lined with rails. This must be where the dwarves get their stone from. You can see carts filled with stone going up and down the rails. This might be a good place to get some resources.",
        ),
        (
            "Crypt",
            "A green skull and crossbones painted on the door of the crypt. Torches are lit giving off a faint light, creating a chilling atmoshpere. You may not want to disturb the goblins, or whatever else is in there.",
        ),
        (
            "Tar Resevoir",
            "Here lies a giant pool of tar. It is a dark, viscous liquid that is easily flammable. Do not touch as it burns most things. Tar is a sign of danger, be hesitant.",
        ),
        (
            "Sealed Tomb",
            "A pyramid like structure stands alone. The area around it has been stripped of life, grey grass and charred trees. The door is sealed shut, multiple locks and chains keeping it closed. Perhaps, there is a good reason for it.",
        ),
    ],
    "D4": [
        (
            "Sorcerer's Tower",
            "A tower erected from glass and stone. It is a sight to behold, as the sun's rays reflect off the pristine glass. A figure stands at the top, looking over the land. A strage glow emanates from the tower. Par the course for a sorcerer.",
        ),
        (
            "Laboratory",
            "A simple yet elegant lab. The walls are lined with dozens upon dozens of large hardback books. You can see the affect that time has had on them, their covers are worn and the pages are yellowed. You smell a strange mixture of chemicals in the air, though you also so some little creatures scurrying about. You know the dangers of mixing chemicals with animals, do not let your guard down.",
        ),
    ],
    "D5": [
        (
            "Zombie Horde",
            "A horde of mindless creatures. You aren't even sure if they notice you, it seems that they are just on a regular migration. Their impact is certain though, you can see the remains of the living, scattered across. You must stay careful, if they spot you, they are sure to attack.",
        ),
        (
            "Failed Experiment",
            "At first glance, you would think that it's just a pile of bones. You would be decieved, as you see green mist spewing out. It's faint but visible. The longer you stay here, the more alive the skeleton appears. You are a brave soul, but sometimes, it's best to leave things alone.",
        ),
        (
            "Merchant's holdout",
            "A small hut, with a sign that was been clearly ripped off. You should check if there's anyone inside. This is a dangerous place, you don't know what could be lurking around.",
        ),
    ],
    "E1": [
        (
            "Sunken Harbour",
            "A once busy and flourishing harbour, now reclaimed by the sea. You can still see some remnants of the old buildings, as sink deeper and deeper with every passing year. In the distance, you see some sort of building. Perhaps, if you had a method of transport across water, you could reach it.",
        ),
        (
            "Witch's Hut",
            "Perhaps coming here wasn't the best idea. The hut stands with shame, broken and burnt. A sinister aura compels you to enter. Is that a death sentence?",
        ),
    ],
    "E2": [
        (
            "Orc Encampment",
            "A large encampment of orcs, which appears to be their main base. They are large, brutish creatures with a penchant for violence. You do not want to get in their way.",
        ),
        (
            "Lava Pit",
            "A giant pit of lava, bubbling spewing molten rock. The pit seems off, you could swear you saw something moving in it. The world around you is deceptive. Be wary.",
        ),
        (
            "Lost Village",
            "This village, you recognise. It's like the other one, but this is torn down. You see the few buildings standing, in too good of a state to be abandoned. You should check it out in case there's anyone left.",
        ),
    ],
    "E3": [
        (
            "Troll's Keep",
            "Even from across the land, you hear of stories. Stories of valiant warriors meeting their ends at the hands of trolls. They are ferocious, but not bright. If you believe you can take them and collect the treasure guarded, then do so.",
        ),
        (
            "Goblin Lair",
            "What seems like an ordinary cave, is actually packed to the brim with little green fiends. They are not to be underestimated, as they are cunning amd have numbers on their side. Do not let your guard down.",
        ),
        (
            "Ice Cavern",
            "A cave filled to the brim with ice. The floors are slippery and you feel as if there's a looming threat of your head getting impaled by one of the iciles on the ceiling. Besides that, you thought you heard some strange grumblings in the distance.",
        ),
        (
            "Igloo",
            "A small structure carved from snow and ice. It has a little sign inviting you in. What a breath of fresh air from the dangers around. You should stay while you can.",
        ),
    ],
    "E4": [
        (
            "Cryo Chamber",
            "A large domed building, labeled with numerous warning signs. The air around is warm, though you feel a chill in your bones. This unnatural atmosphere could be a sign of magic, and is not to be trusted. You should stay clear.",
        ),
        (
            "Hive",
            "A large icosahedron like structure, constructed of a seemingly organic material. When you hear the sound of little bugs, you feel repulsed. Who knows how many of them are inside. You'd rather not have to think about it.",
        ),
        (
            "Mushroom Grove",
            "A grove, small in size but containing massive mushroom trees. They are a sight to behold, but they also seem to be releasing a strange, noxious gas. It makes you feel nauseous, as if you were about to pass out. Do not linger.",
        ),
    ],
    "E5": [
        (
            "Fungal Forest",
            "A larger, denser forest with even larger mushrooms. They are wrapped in multi coloured vines of fungi. The bright vibrant colours give off a vivid aura. You feel as if everything is alive, watching you. The smell is even stronger, likely due to the dense amount of spores in the air. You aren't sure if you can stay here for long.",
        ),
        (
            "Undead Spore Site",
            "A large, dark, ominous cloud. It is almost opaque, but you can see the faint outlines of bones. The smell is really trying to kill you now, as the spores clench on to your lungs, draining your life away. Such a site is certainly not natural, the dead do not raise themselves.",
        ),
        (
            "Lich's Haunt",
            "Imminent danger. You can feel the aura of the undead. It is quiet, strangely quiet. You can hear your own heartbeat, regular and steady. The revenant lies here, you know it.",
        ),
        (
            "Necropolis",
            "Crumbling, shattered, withered away. The city of the dead. Hundreds of graves are neatly arranged, none with a name. The immense presence of death overwhelms you. You know that you are not alone.",
        ),
        (
            "Skeletal Altar",
            "A large altar, made with tens of thousands of bones. They are arranged in a symmetrical lattice, with a large skull in the middle. You can see smoke rising, a faint flickering light. These ritualistic grounds are not to be disturbed, lest you should awaken something.",
        ),
    ],
}

# ------------------ Map Class ------------------ #


class Map:
    """Creates the map of the game as a networkx graph which can be displayed to the player."""

    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        zone_names: tuple[str, ...] = zone_names,
    ):
        """Initialises the map class.

        Args:
            width (int, optional): Width of map. Defaults to 5.
            height (int, optional): Height of map. Defaults to 5.
            zone_names (tuple[str], optional): Names of zones used to create map. Defaults to zone_descriptions.
        """

        self.width = width
        self.height = height
        self.zone_map: nx.Graph = self.create_map(zone_names)
        # I only have the widh and height to be referenced in __str__, no other use for them.

    def create_map(self, zone_names: tuple[str, ...]) -> nx.Graph:
        """Creates a map as a networkx graph using the names pf the zones.

        Args:
            zone_names (tuple[str]): The names of the zones that will be used to create the map.

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
        map: Map = Map(width=5, height=5, zone_names=zone_names),
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

        sprint(f"\nYou have moved to {new_zone_name}.")
        sleep(1)

        new_zone: Zone = zone_data[new_zone_name]
        new_zone.place_player()

        sprint(new_zone.description)
        sleep(1)

        # When the player moves to a new zone, they'll be placed in the first area of that zone.

        new_area_name = new_zone.areas[0][0]
        new_area = area_data[new_zone.name][new_area_name]

        sprint(f"\nYou have entered: {new_area.name}")
        sleep(1)

        sprint(new_area.description)
        sleep(2)

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
        biome: str = "",
    ):
        self.parent_zone: Zone = parent_zone
        self.name = name
        self.description = description
        self.is_player_here = is_player_here
        self.biome = biome
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
        if len(self.moveable_areas) == 0:
            sprint("There are no other areas to move to.")
            sleep(1)
            return self

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

        sprint(f"\nYou have moved to: {new_area_name}")
        sleep(1)

        new_area: Area = area_data[self.parent_zone.name][new_area_name]
        new_area.place_player()

        sprint(new_area.description)
        sleep(2)

        return new_area

    def __str__(self) -> str:
        return f"Name: {self.name}, Description: {self.description}"


# ------------------- Zone & Area Data ------------------- #


zone_data: dict[str, Zone] = {
    "A1": (a1 := Zone("A1", zone_descriptions[0][1], areas=area_descriptions["A1"])),
    "A2": (a2 := Zone("A2", zone_descriptions[1][1], areas=area_descriptions["A2"])),
    "A3": (a3 := Zone("A3", zone_descriptions[2][1], areas=area_descriptions["A3"])),
    "A4": (a4 := Zone("A4", zone_descriptions[3][1], areas=area_descriptions["A4"])),
    "A5": (a5 := Zone("A5", zone_descriptions[4][1], areas=area_descriptions["A5"])),
    "B1": (b1 := Zone("B1", zone_descriptions[5][1], areas=area_descriptions["B1"])),
    "B2": (b2 := Zone("B2", zone_descriptions[6][1], areas=area_descriptions["B2"])),
    "B3": (b3 := Zone("B3", zone_descriptions[7][1], areas=area_descriptions["B3"])),
    "B4": (b4 := Zone("B4", zone_descriptions[8][1], areas=area_descriptions["B4"])),
    "B5": (b5 := Zone("B5", zone_descriptions[9][1], areas=area_descriptions["B5"])),
    "C1": (c1 := Zone("C1", zone_descriptions[10][1], areas=area_descriptions["C1"])),
    "C2": (c2 := Zone("C2", zone_descriptions[11][1], areas=area_descriptions["C2"])),
    "C3": (c3 := Zone("C3", zone_descriptions[12][1], areas=area_descriptions["C3"])),
    "C4": (c4 := Zone("C4", zone_descriptions[13][1], areas=area_descriptions["C4"])),
    "C5": (c5 := Zone("C5", zone_descriptions[14][1], areas=area_descriptions["C5"])),
    "D1": (d1 := Zone("D1", zone_descriptions[15][1], areas=area_descriptions["D1"])),
    "D2": (d2 := Zone("D2", zone_descriptions[16][1], areas=area_descriptions["D2"])),
    "D3": (d3 := Zone("D3", zone_descriptions[17][1], areas=area_descriptions["D3"])),
    "D4": (d4 := Zone("D4", zone_descriptions[18][1], areas=area_descriptions["D4"])),
    "D5": (d5 := Zone("D5", zone_descriptions[19][1], areas=area_descriptions["D5"])),
    "E1": (e1 := Zone("E1", zone_descriptions[20][1], areas=area_descriptions["E1"])),
    "E2": (e2 := Zone("E2", zone_descriptions[21][1], areas=area_descriptions["E2"])),
    "E3": (e3 := Zone("E3", zone_descriptions[22][1], areas=area_descriptions["E3"])),
    "E4": (e4 := Zone("E4", zone_descriptions[23][1], areas=area_descriptions["E4"])),
    "E5": (e5 := Zone("E5", zone_descriptions[24][1], areas=area_descriptions["E5"])),
}

area_data: dict[str, dict[str, Area]] = {
    "A1": {
        area_descriptions["A1"][0][0]: (
            home := Area(
                a1, area_descriptions["A1"][0][0], area_descriptions["A1"][0][1]
            )
        ),
        area_descriptions["A1"][1][0]: (
            abandoned_house := Area(
                a1, area_descriptions["A1"][1][0], area_descriptions["A1"][1][1]
            )
        ),
        area_descriptions["A1"][2][0]: (
            lake := Area(
                a1, area_descriptions["A1"][2][0], area_descriptions["A1"][2][1]
            )
        ),
    },
    "A2": {
        area_descriptions["A2"][0][0]: (
            ruins := Area(
                a2, area_descriptions["A2"][0][0], area_descriptions["A2"][0][1]
            )
        ),
        area_descriptions["A2"][1][0]: (
            shack := Area(
                a2, area_descriptions["A2"][1][0], area_descriptions["A2"][1][1]
            )
        ),
        area_descriptions["A2"][2][0]: (
            small_cave := Area(
                a2, area_descriptions["A2"][2][0], area_descriptions["A2"][2][1]
            )
        ),
    },
    "A3": {
        area_descriptions["A3"][0][0]: (
            forest := Area(
                a3, area_descriptions["A3"][0][0], area_descriptions["A3"][0][1]
            )
        ),
        area_descriptions["A3"][1][0]: (
            grove := Area(
                a3, area_descriptions["A3"][1][0], area_descriptions["A3"][1][1]
            )
        ),
        area_descriptions["A3"][2][0]: (
            elven_outpost := Area(
                a3, area_descriptions["A3"][2][0], area_descriptions["A3"][2][1]
            )
        ),
    },
    "A4": {
        area_descriptions["A4"][0][0]: (
            shrubbery := Area(
                a4, area_descriptions["A4"][0][0], area_descriptions["A4"][0][1]
            )
        ),
        area_descriptions["A4"][1][0]: (
            grassy_field := Area(
                a4, area_descriptions["A4"][1][0], area_descriptions["A4"][1][1]
            )
        ),
        area_descriptions["A4"][2][0]: (
            river := Area(
                a4, area_descriptions["A4"][2][0], area_descriptions["A4"][2][1]
            )
        ),
    },
    "A5": {
        area_descriptions["A5"][0][0]: (
            spring := Area(
                a5, area_descriptions["A5"][0][0], area_descriptions["A5"][0][1]
            )
        ),
        area_descriptions["A5"][1][0]: (
            dark_pit := Area(
                a5, area_descriptions["A5"][1][0], area_descriptions["A5"][1][1]
            )
        ),
    },
    "B1": {
        area_descriptions["B1"][0][0]: (
            village_square := Area(
                b1, area_descriptions["B1"][0][0], area_descriptions["B1"][0][1]
            )
        ),
        area_descriptions["B1"][1][0]: (
            village_inn := Area(
                b1, area_descriptions["B1"][1][0], area_descriptions["B1"][1][1]
            )
        ),
        area_descriptions["B1"][2][0]: (
            village_shop := Area(
                b1, area_descriptions["B1"][2][0], area_descriptions["B1"][2][1]
            )
        ),
        area_descriptions["B1"][3][0]: (
            village_house := Area(
                b1, area_descriptions["B1"][3][0], area_descriptions["B1"][3][1]
            )
        ),
        area_descriptions["B1"][4][0]: (
            village_church := Area(
                b1, area_descriptions["B1"][4][0], area_descriptions["B1"][4][1]
            )
        ),
        area_descriptions["B1"][5][0]: (
            village_cemetery := Area(
                b1, area_descriptions["B1"][5][0], area_descriptions["B1"][5][1]
            )
        ),
        area_descriptions["B1"][6][0]: (
            village_brewery := Area(
                b1, area_descriptions["B1"][6][0], area_descriptions["B1"][6][1]
            )
        ),
        area_descriptions["B1"][7][0]: (
            village_wall := Area(
                b1, area_descriptions["B1"][7][0], area_descriptions["B1"][7][1]
            )
        ),
    },
    "B2": {
        area_descriptions["B2"][0][0]: (
            village_outskirts := Area(
                b2, area_descriptions["B2"][0][0], area_descriptions["B2"][0][1]
            )
        ),
        area_descriptions["B2"][1][0]: (
            farm := Area(
                b2, area_descriptions["B2"][1][0], area_descriptions["B2"][1][1]
            )
        ),
    },
    "B3": {
        area_descriptions["B3"][0][0]: (
            mysterious_vault := Area(
                b3, area_descriptions["B3"][0][0], area_descriptions["B3"][0][1]
            )
        ),
        area_descriptions["B3"][1][0]: (
            lone_tree := Area(
                b3, area_descriptions["B3"][1][0], area_descriptions["B3"][1][1]
            )
        ),
        area_descriptions["B3"][2][0]: (
            orchard := Area(
                b3, area_descriptions["B3"][2][0], area_descriptions["B3"][2][1]
            )
        ),
        area_descriptions["B3"][3][0]: (
            orcish_hunting_party := Area(
                b3, area_descriptions["B3"][3][0], area_descriptions["B3"][3][1]
            )
        ),
    },
    "B4": {
        area_descriptions["B4"][0][0]: (
            elven_idol := Area(
                b4, area_descriptions["B4"][0][0], area_descriptions["B4"][0][1]
            )
        ),
        area_descriptions["B4"][1][0]: (
            valley := Area(
                b4, area_descriptions["B4"][1][0], area_descriptions["B4"][1][1]
            )
        ),
    },
    "B5": {
        area_descriptions["B5"][0][0]: (
            spiritual_mound := Area(
                b5, area_descriptions["B5"][0][0], area_descriptions["B5"][0][1]
            )
        ),
        area_descriptions["B5"][1][0]: (
            large_cave := Area(
                b5, area_descriptions["B5"][1][0], area_descriptions["B5"][1][1]
            )
        ),
        area_descriptions["B5"][2][0]: (
            spider_den := Area(
                b5, area_descriptions["B5"][2][0], area_descriptions["B5"][2][1]
            )
        ),
        area_descriptions["B5"][3][0]: (
            pond := Area(
                b5, area_descriptions["B5"][3][0], area_descriptions["B5"][3][1]
            )
        ),
    },
    "C1": {
        area_descriptions["C1"][0][0]: (
            village_well := Area(
                c1, area_descriptions["C1"][0][0], area_descriptions["C1"][0][1]
            )
        ),
        area_descriptions["C1"][1][0]: (
            mountainous_path := Area(
                c1, area_descriptions["C1"][1][0], area_descriptions["C1"][1][1]
            )
        ),
        area_descriptions["C1"][2][0]: (
            hill := Area(
                c1, area_descriptions["C1"][2][0], area_descriptions["C1"][2][1]
            )
        ),
    },
    "C2": {
        area_descriptions["C2"][0][0]: (
            shaman_shrine := Area(
                c2, area_descriptions["C2"][0][0], area_descriptions["C2"][0][1]
            )
        ),
        area_descriptions["C2"][1][0]: (
            goblin_camp := Area(
                c2, area_descriptions["C2"][1][0], area_descriptions["C2"][1][1]
            )
        ),
        area_descriptions["C2"][2][0]: (
            pasture := Area(
                c2, area_descriptions["C2"][2][0], area_descriptions["C2"][2][1]
            )
        ),
        area_descriptions["B5"][3][0]: (
            blacksmith_remnants := Area(
                b5, area_descriptions["B5"][3][0], area_descriptions["B5"][3][1]
            )
        ),
    },
    "C3": {
        area_descriptions["C3"][0][0]: (
            monolith := Area(
                c3, area_descriptions["C3"][0][0], area_descriptions["C3"][0][1]
            )
        ),
    },
    "C4": {
        area_descriptions["C4"][0][0]: (
            mystical_forest := Area(
                c4, area_descriptions["C4"][0][0], area_descriptions["C4"][0][1]
            )
        ),
        area_descriptions["C4"][1][0]: (
            clearing := Area(
                c4, area_descriptions["C4"][1][0], area_descriptions["C4"][1][1]
            )
        ),
        area_descriptions["C4"][2][0]: (
            fallen_tree := Area(
                c4, area_descriptions["C4"][2][0], area_descriptions["C4"][2][1]
            )
        ),
        area_descriptions["C4"][3][0]: (
            engravings := Area(
                c4, area_descriptions["C4"][3][0], area_descriptions["C4"][3][1]
            )
        ),
    },
    "C5": {
        area_descriptions["C5"][0][0]: (
            spider_nest := Area(
                c5, area_descriptions["C5"][0][0], area_descriptions["C5"][0][1]
            )
        ),
        area_descriptions["C5"][1][0]: (
            silk_vein := Area(
                c5, area_descriptions["C5"][1][0], area_descriptions["C5"][1][1]
            )
        ),
        area_descriptions["C5"][2][0]: (
            carcase := Area(
                c5, area_descriptions["C5"][2][0], area_descriptions["C5"][2][1]
            )
        ),
        area_descriptions["C5"][3][0]: (
            elven_arch := Area(
                c5, area_descriptions["C5"][3][0], area_descriptions["C5"][3][1]
            )
        ),
    },
    "D1": {
        area_descriptions["D1"][0][0]: (
            hidden_mountain_pass := Area(
                d1, area_descriptions["D1"][0][0], area_descriptions["D1"][0][1]
            )
        ),
        area_descriptions["D1"][1][0]: (
            dwarven_temple := Area(
                d1, area_descriptions["D1"][1][0], area_descriptions["D1"][1][1]
            )
        ),
        area_descriptions["D1"][2][0]: (
            dwarven_forge := Area(
                d1, area_descriptions["D1"][2][0], area_descriptions["D1"][2][1]
            )
        ),
        area_descriptions["D1"][3][0]: (
            large_mountain := Area(
                d1, area_descriptions["D1"][3][0], area_descriptions["D1"][3][1]
            )
        ),
    },
    "D2": {
        area_descriptions["D2"][0][0]: (
            dwarven_guard_post := Area(
                d2, area_descriptions["D2"][0][0], area_descriptions["D2"][0][1]
            )
        ),
        area_descriptions["D2"][1][0]: (
            destroyed_camp := Area(
                d2, area_descriptions["D2"][1][0], area_descriptions["D2"][1][1]
            )
        ),
        area_descriptions["D2"][2][0]: (
            burning_burial_site := Area(
                d2, area_descriptions["D2"][2][0], area_descriptions["D2"][2][1]
            )
        ),
    },
    "D3": {
        area_descriptions["D3"][0][0]: (
            quarry := Area(
                d3, area_descriptions["D3"][0][0], area_descriptions["D3"][0][1]
            )
        ),
        area_descriptions["D3"][1][0]: (
            crypt := Area(
                d3, area_descriptions["D3"][1][0], area_descriptions["D3"][1][1]
            )
        ),
        area_descriptions["D3"][2][0]: (
            tar_reservoir := Area(
                d3, area_descriptions["D3"][2][0], area_descriptions["D3"][2][1]
            )
        ),
        area_descriptions["D3"][3][0]: (
            sealed_tomb := Area(
                d3, area_descriptions["D3"][3][0], area_descriptions["D3"][3][1]
            )
        ),
    },
    "D4": {
        area_descriptions["D4"][0][0]: (
            sorcerers_tower := Area(
                d4, area_descriptions["D4"][0][0], area_descriptions["D4"][0][1]
            )
        ),
        area_descriptions["D4"][1][0]: (
            laboratory := Area(
                d4, area_descriptions["D4"][1][0], area_descriptions["D4"][1][1]
            )
        ),
    },
    "D5": {
        area_descriptions["D5"][0][0]: (
            zombie_horde := Area(
                d5, area_descriptions["D5"][0][0], area_descriptions["D5"][0][1]
            )
        ),
        area_descriptions["D5"][1][0]: (
            failed_experiment := Area(
                d5, area_descriptions["D5"][1][0], area_descriptions["D5"][1][1]
            )
        ),
        area_descriptions["D5"][2][0]: (
            merchants_holdout := Area(
                d5, area_descriptions["D5"][2][0], area_descriptions["D5"][2][1]
            )
        ),
    },
    "E1": {
        area_descriptions["E1"][0][0]: (
            sunken_harbour := Area(
                e1, area_descriptions["E1"][0][0], area_descriptions["E1"][0][1]
            )
        ),
        area_descriptions["E1"][1][0]: (
            witchs_hut := Area(
                e1, area_descriptions["E1"][1][0], area_descriptions["E1"][1][1]
            )
        ),
    },
    "E2": {
        area_descriptions["E2"][0][0]: (
            orc_encampment := Area(
                e2, area_descriptions["E2"][0][0], area_descriptions["E2"][0][1]
            )
        ),
        area_descriptions["E2"][1][0]: (
            lava_pit := Area(
                e2, area_descriptions["E2"][1][0], area_descriptions["E2"][1][1]
            )
        ),
        area_descriptions["E2"][2][0]: (
            lost_village := Area(
                e2, area_descriptions["E2"][2][0], area_descriptions["E2"][2][1]
            )
        ),
    },
    "E3": {
        area_descriptions["E3"][0][0]: (
            trolls_keep := Area(
                e3, area_descriptions["E3"][0][0], area_descriptions["E3"][0][1]
            )
        ),
        area_descriptions["E3"][1][0]: (
            goblin_lair := Area(
                e3, area_descriptions["E3"][1][0], area_descriptions["E3"][1][1]
            )
        ),
        area_descriptions["E3"][2][0]: (
            ice_cavern := Area(
                e3, area_descriptions["E3"][2][0], area_descriptions["E3"][2][1]
            )
        ),
        area_descriptions["E3"][3][0]: (
            igloo := Area(
                e3, area_descriptions["E3"][3][0], area_descriptions["E3"][3][1]
            )
        ),
    },
    "E4": {
        area_descriptions["E4"][0][0]: (
            cryo_chamber := Area(
                e4, area_descriptions["E4"][0][0], area_descriptions["E4"][0][1]
            )
        ),
        area_descriptions["E4"][1][0]: (
            hive := Area(
                e4, area_descriptions["E4"][1][0], area_descriptions["E4"][1][1]
            )
        ),
        area_descriptions["E4"][2][0]: (
            mushroom_grave := Area(
                e4, area_descriptions["E4"][2][0], area_descriptions["E4"][2][1]
            )
        ),
    },
    "E5": {
        area_descriptions["E5"][0][0]: (
            fungal_forest := Area(
                e5, area_descriptions["E5"][0][0], area_descriptions["E5"][0][1]
            )
        ),
        area_descriptions["E5"][1][0]: (
            undead_spore_site := Area(
                e5, area_descriptions["E5"][1][0], area_descriptions["E5"][1][1]
            )
        ),
        area_descriptions["E5"][2][0]: (
            lichs_haunt := Area(
                e5, area_descriptions["E5"][2][0], area_descriptions["E5"][2][1]
            )
        ),
        area_descriptions["E5"][3][0]: (
            necropolis := Area(
                e5, area_descriptions["E5"][3][0], area_descriptions["E5"][3][1]
            )
        ),
        area_descriptions["E5"][4][0]: (
            skeletal_altar := Area(
                e5, area_descriptions["E5"][4][0], area_descriptions["E5"][4][1]
            )
        ),
    },
}


if __name__ == "__main__":
    sprint("Welcome to the game!")
    map = Map(width=5, height=5, zone_names=zone_names)
    current_zone = a1
    current_area = home
    current_zone.place_player()
    current_area.place_player()
    for _ in range(2):
        current_area = current_area.move_area()
        sleep(1)
    current_zone, current_area = current_zone.move()
    for _ in range(2):
        current_area = current_area.move_area()
        sleep(1)


# !
# ?
# //
# TODO
# *
