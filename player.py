import random
import math

MAX_LEVEL = 99
CHOSEN_ATTACK_STYLE_BONUS = 3

DHAROK_SET_EQUIPMENT_BONUSES = {
    "attack": 125,
    "strength": 150,
    "defense": 284
}

PIETY_PRAYER_BONUSES = {
    "attack": 1.2,
    "strength": 1.23,
    "defense": 1.25
}

STARTING_INVENTORY = {
    "shark_count": 6,
    "karambwan_count": 2
}

def effective_stat(base_level, boost, prayer_modifier, attack_style_bonus):
    return math.floor((base_level + boost) * prayer_modifier) + 8 + attack_style_bonus

class Player:
    def __init__(self, name, attack_level=MAX_LEVEL, strength_level=MAX_LEVEL, defense_level=MAX_LEVEL, debug=False):
        self.name = name
        self.hp = MAX_LEVEL
        self.shark_count = STARTING_INVENTORY["shark_count"]
        self.karambwan_count = STARTING_INVENTORY["karambwan_count"]
        self.attack_level = attack_level
        self.strength_level = strength_level
        self.defense_level = defense_level
        self.strategy = None
        self.debug = debug

    def reset(self):
        self.hp = MAX_LEVEL
        self.shark_count = STARTING_INVENTORY["shark_count"]
        self.karambwan_count = STARTING_INVENTORY["karambwan_count"]

    @property
    def effective_attack_level(self):
        return effective_stat(self.attack_level, 0, PIETY_PRAYER_BONUSES["attack"], 0) # for now assuming we always use hack instead of chop
    
    @property
    def effective_strength_level(self):
        return effective_stat(self.strength_level, 0, PIETY_PRAYER_BONUSES["strength"], CHOSEN_ATTACK_STYLE_BONUS)
    
    @property
    def effective_defense_level(self):
        return effective_stat(self.defense_level, 0, PIETY_PRAYER_BONUSES["defense"], CHOSEN_ATTACK_STYLE_BONUS)

    def hit_success(self, opponent): # this will need some revamp if we include the knives
        debug_message = ""
        attack_roll = (self.effective_attack_level * (DHAROK_SET_EQUIPMENT_BONUSES["attack"] + 64))
        defense_roll = opponent.effective_defense_level * (DHAROK_SET_EQUIPMENT_BONUSES["defense"] + 64)
        if attack_roll > defense_roll:
            hit_chance = 1 - (defense_roll + 2) / (2 * (attack_roll + 1))
        else:
            hit_chance = attack_roll / (2 * (defense_roll + 1))
        did_hit = random.random() < hit_chance
        debug_message += f"hit was {did_hit} with a {hit_chance} chance to hit"
        if self.debug:
            print(debug_message)
        return did_hit

    def attack(self, opponent):
        debug_message = ""
        max_hit = math.floor((self.effective_strength_level * (DHAROK_SET_EQUIPMENT_BONUSES["strength"] + 64) + 320) / 640)
        if self.hit_success(opponent):
            hit = random.randint(0, int(max_hit))
            opponent.hp -= hit
            debug_message += f"{self.name} hit {opponent.name} for {hit} damage, leaving them at {opponent.hp} health. \n"
        else:
            debug_message += "attack missed. \n"
        if self.debug:
            print(debug_message)

    def eat_shark(self):
        debug_message = ""
        if self.shark_count > 0:
            self.hp += 20
            if self.hp > MAX_LEVEL:
                self.hp = MAX_LEVEL
            self.shark_count -= 1
            debug_message += f"ate a shark to {self.hp} hp. \n"
        else:
            debug_message += "ran out of sharks. \n"
        if self.debug:
            print(debug_message)

    def eat_shark_and_karambwan(self):
        debug_message = ""
        if self.shark_count > 0 and self.karambwan_count > 0:
            self.hp += 38
            if self.hp > MAX_LEVEL:
                self.hp = MAX_LEVEL
            self.shark_count -= 1
            self.karambwan_count -= 1
            debug_message += f"combo ate to {self.hp} hp. \n"
        else:
            debug_message += "ran out of karambwans. \n"
        if self.debug:
            print(debug_message)

    def choose_action(self, opponent):
        return self.strategy(self, opponent)