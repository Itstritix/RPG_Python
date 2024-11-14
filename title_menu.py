import os
from time import sleep

from game_class import Player
from help_function import is_number
from save import save_data, load_save

def create_character():
    os.system('cls')
    print("Hi adventurer, what is your name?")
    player_name = input(">> ")
    player_data = Player(player_name, 100, 10, 20, 1, 4, 1, 7)
    return player_data

def show_title_menu():
    os.system('cls')
    print(">> 1. NEW GAME <<")
    print(">> 2. LOAD GAME <<")
    print(">> 3. QUIT GAME <<")
    print("")


def title_menu_choice():
    have_save_file = os.path.isfile("./save/save.pickle")
    print("Please select one of the options above(write the number)")
    title_choice = input(">> ")
    if is_number(title_choice):
        if int(title_choice) == 1:
            return create_character()
        elif int(title_choice) == 2 and have_save_file:
            return load_save()
        elif int(title_choice) == 2 and not have_save_file:
            print("You don't have any saves")
            sleep(2)
        elif int(title_choice) == 3:
            exit()