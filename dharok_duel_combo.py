import random

from player import Player

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

def find_optimal_threshold(n_sims=100):
    thresholds = range(2, 61)
    threshold_wins = {threshold: 0 for threshold in thresholds}
    max_total_fights = 0
    
    for threshold1 in thresholds:
        wins = 0
        total_fights=0
        
        thresholds_2 = range(2, 61)
        for threshold2 in thresholds_2:
            if threshold1 != threshold2:
                for _ in range(n_sims):
                    total_fights+=1
                    winner = simulate_game(strategy1, threshold1, threshold2)
                    if winner == "Player 1":
                        threshold_wins[threshold1] += 1
                    max_total_fights = max(total_fights, max_total_fights) # could just calc this once
    
    optimal_threshold = max(threshold_wins, key=threshold_wins.get)
    
    max_wins = threshold_wins[optimal_threshold]
    
    return optimal_threshold, max_wins, max_total_fights

optimal_threshold, max_wins, max_total_fights = find_optimal_threshold(n_sims=100)
print(f"Optimal HP threshold for strategy1 is {optimal_threshold} with {max_wins} out of {max_total_fights}")
