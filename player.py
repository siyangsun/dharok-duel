import random

MAX_LEVEL = 99

class Player:
    def __init__(self, name, attack_level=MAX_LEVEL, defense_level=MAX_LEVEL, debug=False):
        self.name = name
        self.hp = MAX_LEVEL
        self.shark_count = 6
        self.karambwan_count = 2
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.strategy = None
        self.debug = debug

    def reset(self):
        self.hp = MAX_LEVEL
        self.shark_count = 6
        self.karambwan_count = 2

    def attack(self, opponent):
        max_hit = 44 + (42 * ((MAX_LEVEL - self.hp) // 98))
        debug_message = ""
        if self.hit_success(opponent):
            hit = random.randint(0, int(max_hit))
            opponent.hp -= hit
            debug_message += f"{self.name} hit {opponent.name} for {hit} damage, leaving them at {opponent.hp} health. \n"
        else:
            debug_message += "attack missed. \n"
        if self.debug:
            print(debug_message)

    def hit_success(self, opponent):
        attack_roll = self.attack_level * (self.attack_level + 64)
        defense_roll = opponent.defense_level * (opponent.defense_level + 64)
        hit_chance = attack_roll / (attack_roll + defense_roll)
        return random.random() < hit_chance

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