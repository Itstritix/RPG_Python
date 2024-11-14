import os
import random
from time import sleep

from help_function import is_number
from menu_func import fight_menu_choice, show_fight_menu

Loot_table = ["Health Potion", "Defense Potion", "Attack Potion"]

class Entity:
    def __init__(self, name="Pit", hp=20, defense=0, attack=0, level=1, experience=0):
        self.name = name
        self.max_hp = hp
        self.hp = self.max_hp
        self.default_attack = attack
        self.attack = self.default_attack
        self.default_defense = defense
        self.defense = self.default_defense
        self.level = level
        self.experience = experience

    def __str__(self):
        return (">> Character name: " + self.name + " <<" + "\n" +
                ">> HP: " + str(self.hp) + "/" + str(self.max_hp) + " <<" + "\n" +
                ">> Attack: " + str(self.attack) + " <<" + "\n" +
                ">> Defense: " + str(self.defense) + " <<" + "\n" +
                ">> Level: " + str(self.level) + " <<"
                )

    def take_damage(self, opponent):
        damage_formula = opponent.attack*1.5 - self.defense
        if damage_formula <= 0:
            self.hp -= 1
            print(self.name + " took " + str(1) + " damage ")
        else:
            self.hp -= damage_formula
            print(self.name + " took " + str(opponent.attack * 1.5 - self.defense) + " damage ")

    def show_status(self):
        pass


class Player(Entity):
    def __init__(self, username, hp, defense, attack, x, y, level, experience):
        super().__init__(username, hp, defense, attack, level, experience)
        self.inventory = []
        self.x = x
        self.y = y

    def show_position(self, map, biome):
        print("Location: " + biome[map[self.y][self.x]]["name"])
        print("Description: " + biome[map[self.y][self.x]]["Desc"])

    def move(self, user_input):
        if int(user_input) == 1 or user_input == "go north" and self.y > 0:
            self.y -= 1
        elif int(user_input) == 4 or  user_input == "go south" and self.y < 5:
            self.y += 1
        elif int(user_input) == 2 or  user_input == "go east" and self.x < 5:
            self.x += 1
        elif int(user_input) == 3 or  user_input == "go west" and self.x > 0:
            self.x -= 1

    def start_fight(self, monster):
        fight_toggle = True
        if monster.level < self.level:
            monster.level_up()

        while fight_toggle:
            player_turn = True
            player_action = 0
            while player_turn:
                show_fight_menu()
                print(self.show_status())
                print(monster.show_status())
                player_action = fight_menu_choice()
                os.system("cls")
                if int(player_action) == 1:
                    monster.take_damage(self)
                    player_turn = False
                elif int(player_action) == 2:
                    self.show_inventory(True)
                    if len(self.inventory) > 0:
                        print("Which item would you like to use")
                        inventory_choice = input(">> ")
                        if is_number(inventory_choice) and int(inventory_choice) <= len(self.inventory) and int(inventory_choice) > 0:
                            self.inventory[int(inventory_choice)-1].use_potion(int(inventory_choice)-1, self)
                            player_turn = False
                        else:
                            player_action = 0
                    else:
                        player_action = int(0)
                elif int(player_action) == 3:
                    fight_toggle = False
                    player_turn = False
                else:
                    print("Please select a correct action")
                    sleep(2)

            if monster.hp <= 0:
                print("Congrats you've beat the " + monster.name)
                monster.monster_loot(self)
                monster.hp = monster.max_hp
                if self.experience / 7 > self.level:
                    self.level_up()

                return True
            self.take_damage(monster)
            self.defense = self.default_defense
            self.attack = self.default_attack
            sleep(2)

        return False

    def show_inventory(self, fight):
        if len(self.inventory) > 0:
            for i in range(0, len(self.inventory), 1):
                print(">> " + str(i + 1) + ". " + self.inventory[i].name + " <<")
                if len(self.inventory) == i+1 and fight == True:
                    print(">> " + str(i + 2) + ". Back <<")

        else:
            print("Your inventory is empty")
            sleep(3)

    def level_up(self):
        self.level += 1
        self.attack += 15
        self.defense += 15
        self.max_hp += 20
        self.hp += 20

    def show_status(self):
        return "You have " + str(self.hp) + " HP left"

class Monster(Entity):
    def __init__(self, name, hp, attack, defense, type):
        super().__init__(name, hp, attack, defense)
        self.type = type

    def monster_loot(self, player):
        player.experience += random.randint(3, self.level*7)

    def show_status(self):
        if self.type.lower() == "boss":
            return self.name + " has " + str(self.hp) + " HP left"
        else:
            return "The " + self.name + " has " + str(self.hp) + " HP left and is level " + str(self.level)

    def level_up(self):
        self.level += 1
        self.attack += 10
        self.defense += 10
        self.max_hp += 20
        self.hp += 10

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return (self.name + "\n" +
                self.description)

class Potion(Item):
    def __init__(self, name, description, effect):
        super().__init__(name, description)
        self.effect = effect

    def add_potion(self, entity):
        entity.inventory.append(self)

    def use_potion(self, inv_index, player):
        if player.inventory[inv_index - 1].name == "Health Potion":
            if player.hp + self.effect*player.level > player.max_hp:
                player.hp = player.max_hp
                print("You drink your bottle and feel better, you just got all your hp back")
            else:
                player.hp += self.effect*player.level
                print("You drink your bottle and feel better, you just got" + str(self.effect) + " HP back")
            player.inventory.pop(inv_index - 1)
        elif player.inventory[inv_index - 1].name == "Defense Potion":
            player.defense += self.effect*player.level
            player.inventory.pop(inv_index - 1)
            print("You feel resistances going through your body, you just got " + str(self.effect) + " defense")
        elif player.inventory[inv_index - 1].name == "Attack Potion":
            player.attack += self.effect*player.level
            player.inventory.pop(inv_index - 1)
            print("You feel a lot stronger, you just got " + str(self.effect) + " attack")
        else:
            print("This potion either doesn't exist or you don't have it in your inventory")


