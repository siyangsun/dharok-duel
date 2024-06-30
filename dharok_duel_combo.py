import random

class Player:
    def __init__(self, name, attack_level=99, defense_level=99):
        self.name = name
        self.hp = 99
        self.shark_count = 6
        self.karambwan_count = 2
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.strategy = None

    def reset(self):
        self.hp = 99
        self.shark_count = 4
        self.karambwan_count = 2

    def attack(self, opponent):
        max_hit = 44 + (42 * ((99 - self.hp) // 98))
        if self.hit_success(opponent):
            hit = random.randint(0, int(max_hit))
            opponent.hp -= hit

    def hit_success(self, opponent):
        attack_roll = self.attack_level * (self.attack_level + 64)
        defense_roll = opponent.defense_level * (opponent.defense_level + 64)
        hit_chance = attack_roll / (attack_roll + defense_roll)
        return random.random() < hit_chance

    def eat_shark(self):
        if self.shark_count > 0:
            self.hp += 20
            if self.hp > 99:
                self.hp = 99
            self.shark_count -= 1

    def eat_shark_and_karambwan(self):
        if self.shark_count > 0 and self.karambwan_count > 0:
            self.hp += 38
            if self.hp > 99:
                self.hp = 99
            self.shark_count -= 1
            self.karambwan_count -= 1

    def choose_action(self, opponent):
        return self.strategy(self, opponent)

def strategy1(player, opponent, threshold):
    if player.hp < threshold and player.shark_count > 0 and player.karambwan_count > 0:
        player.eat_shark_and_karambwan()
    else:
        player.attack(opponent)

def simulate_game(strategy, threshold1, threshold2):
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    player1.strategy = lambda p, o: strategy(p, o, threshold1)
    player2.strategy = lambda p, o: strategy(p, o, threshold2)
    
    players = [player1, player2]
    random.shuffle(players)
    
    while player1.hp > 0 and player2.hp > 0:
        current_player = players[0]
        opponent = players[1]
        current_player.choose_action(opponent)
        
        if opponent.hp <= 0:
            return current_player.name
        
        players.reverse()

def find_optimal_threshold():
    thresholds = range(2, 61)
    threshold_wins = {threshold: 0 for threshold in thresholds}
    max_total_fights = 0
    
    for threshold1 in thresholds:
        wins = 0
        total_fights=0
        
        thresholds_2 = range(2, 61)
        for threshold2 in thresholds_2:
            if threshold1 != threshold2:
                for _ in range(1000):
                    total_fights+=1
                    winner = simulate_game(strategy1, threshold1, threshold2)
                    if winner == "Player 1":
                        threshold_wins[threshold1] += 1
                    max_total_fights = max(total_fights, max_total_fights) # could just calc this once
    
    optimal_threshold = max(threshold_wins, key=threshold_wins.get)
    
    max_wins = threshold_wins[optimal_threshold]
    
    return optimal_threshold, max_wins, max_total_fights

optimal_threshold, max_wins, max_total_fights = find_optimal_threshold()
print(f"Optimal HP threshold for strategy1 is {optimal_threshold} with {max_wins} out of {max_total_fights}")
