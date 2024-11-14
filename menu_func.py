import os


def show_fight_menu():
    os.system("cls")
    print(">> 1. ATTACK <<")
    print(">> 2. ITEMS <<")
    print(">> 3. RUN AWAY <<")

def fight_menu_choice():
    print("Please select one of the options above (write the number)")
    action_choice = input(">> ")
    while action_choice not in ["1", "2", "3"]:
        action_choice = input(">> ")
    return action_choice

def show_action_menu():
    os.system("cls")
    print(">> 1. GO NORTH <<")
    print(">> 2. GO EAST <<")
    print(">> 3. GO WEST <<")
    print(">> 4. GO SOUTH <<")
    print(">> 5. SHOW STATS <<")
    print(">> 6. SAVE & RETURN TO MENU <<")
    print("")

def action_menu_choice():
    action_choices = input(">> ")
    while action_choices not in ["1", "2", "3", "4", "5", "6"]:
        action_choices = input(">> ")
    return action_choices
