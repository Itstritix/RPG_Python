import os
import random
from time import sleep

from game_class import Monster, Potion
from menu_func import show_action_menu, action_menu_choice
from save import save_data, load_save
from title_menu import create_character, show_title_menu, title_menu_choice

map = [["plains", "plainsF", "boss tower", "forestF", "plains"],
       ["plains", "plains", "dark forest", "forest", "plains"],
       ["plains", "forest", "mountain", "cliff1", "forest"],
       ["plains", "cliff2", "mountain", "mountain", "forest"],
       ["plains", "home town", "forest", "forest", "forest"]]

p_data = None

wolf_data = Monster("Wolf", 20, 20, 10, "normal monster")
nepenthe_data = Monster("Nepenthe", 20, 20, 10, "normal monster")
boss_data = Monster("Ilfang the Kobold Lord", 120, 100, 80, "boss")

h_potion = Potion("Health Potion", "You feel better after drinking this potion", 5)
d_potion = Potion("Defense Potion", "You feel more resistant after drinking this potion", 5)
a_potion = Potion("Attack Potion", "You feel stronger after drinking this potion", 5)

biome = {
    "plains": {
        "name": "Plains",
        "Desc": "It's a plain, i can see the mountain from here",
        "Encounter": [wolf_data, h_potion, d_potion, a_potion],
    },
    "plainsF": {
        "name": "Plains",
        "Desc": "It's a plain, and you can the tower while facing the east",
        "Encounter": [wolf_data, h_potion, d_potion, a_potion],
    },
    "cliff1": {
        "name": "Cliff",
        "Desc": "I can almost see the end, i see the tower of the boss",
        "Encounter": [nepenthe_data, h_potion, d_potion, a_potion],
    },
    "cliff2": {
        "name": "Cliff",
        "Desc": "I can see my hometown, the adventure just began",
        "Encounter": [nepenthe_data, h_potion, d_potion, a_potion],
    },
    "forest": {
        "name": "Forest",
        "Desc": "It's a forest",
        "Encounter": [nepenthe_data, h_potion, d_potion, a_potion],
    },
    "forestF": {
        "name": "Forest",
        "Desc": "It's a forest, you can see the tower while facing the west",
        "Encounter": [nepenthe_data, h_potion, d_potion, a_potion],
    },
    "dark forest": {
        "name": "Dark Forest",
        "Desc": "It's a dark forest, you can the see boss tower when facing the north",
        "Encounter": [nepenthe_data, wolf_data, h_potion, d_potion, a_potion],
    },
    "mountain": {
        "name": "Mountain",
        "Desc": "You're on a mountain",
        "Encounter": [nepenthe_data, wolf_data, h_potion, d_potion, a_potion],
    },
    "home town": {
        "name": "Home Town",
        "Desc": "Your home town, where everything start",
        "Encounter": [],
    },
    "boss tower": {
        "name": "Boss Tower",
        "Desc": "It's the tower where the boss lives, it's also where the adventure end",
        "Encounter": [boss_data],
    },
}

def start_game():
    if not os.path.isdir("save"):
        os.mkdir("save")
    game_on = True
    while game_on:
        show_title_menu()
        p_data = title_menu_choice()
        waiting_player = True
        is_boss_dead = False
        while p_data is not None and p_data.hp > 0 and not is_boss_dead and waiting_player and p_data is not None:
            show_action_menu()

            p_data.show_position(map, biome)
            print("To move write the number corresponding to the action you want to do")
            user_action = action_menu_choice()
            if user_action in ["1", "2", "3", "4"]:
                p_data.move(user_action)
                random_var = random.randint(1, 100)
                if random_var <= 60:
                    if len(biome[map[p_data.y][p_data.x]]["Encounter"]) == 4:
                        p_data.start_fight(biome[map[p_data.y][p_data.x]]["Encounter"][0])
                    if len(biome[map[p_data.y][p_data.x]]["Encounter"]) == 5:
                        random_mob = random.randint(0, 1)
                        p_data.start_fight(biome[map[p_data.y][p_data.x]]["Encounter"][random_mob])
                if random_var > 60:
                    if len(biome[map[p_data.y][p_data.x]]["Encounter"]) == 4:
                        random_potion = random.randint(1, 3)
                        biome[map[p_data.y][p_data.x]]["Encounter"][random_potion].add_potion(p_data)
                        print("Wow you got a " + biome[map[p_data.y][p_data.x]]["Encounter"][random_potion].name)
                    elif len(biome[map[p_data.y][p_data.x]]["Encounter"]) == 5:
                        random_potion = random.randint(1, 3)
                        print(biome[map[p_data.y][p_data.x]]["Encounter"][random_potion+1])
                        biome[map[p_data.y][p_data.x]]["Encounter"][random_potion+1].add_potion(p_data)
                        print("Wow you got a " + biome[map[p_data.y][p_data.x]]["Encounter"][random_potion+1].name)
                if biome[map[p_data.y][p_data.x]]["name"] == "Boss Tower":
                    is_boss_dead = p_data.start_fight(boss_data)
                    sleep(3)
            elif user_action in ["5", "6"]:
                if user_action == "5":
                    print(p_data.__str__())
                    print()
                    print(">> Inventory <<")
                    p_data.show_inventory(False)
                if user_action == "6":
                    save_data(p_data)
                    waiting_player = False
                    print("Saving...")
                    sleep(8)


            sleep(2)


start_game()

