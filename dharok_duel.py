import random

from player import Player
    
def strategy1(player, opponent):
    if player.hp < 45 and player.shark_count > 0 and player.karambwan_count > 0:
        player.eat_shark_and_karambwan()
    else:
        player.throw_knives(opponent)
        player.attack(opponent)

def strategy2(player, opponent):
    if player.zamorak_brew_count > 0 and player.hp > 11:
        player.drink_zamorak_brew()
    player.throw_knives(opponent)
    player.attack(opponent)

def strategy3(player, opponent):
    def aggressive_move():
        if player.zamorak_brew_count > 0 and player.hp > 11:
            player.drink_zamorak_brew()
        player.throw_knives(opponent)
        player.attack(opponent)
    if player.shark_count == 0 and player.karambwan_count == 0:
        aggressive_move()
    else:
        choice = random.choice(['attack', 'shark', 'shark_and_karambwan'])
        player.accurate_axe_style = random.random() < 0.5
        if choice == 'attack':
            aggressive_move()
        elif choice == 'shark' and player.shark_count > 0:
            player.eat_shark()
        else:
            player.eat_shark_and_karambwan()

def strategy4(player, opponent):
    if player.hp < 40 and player.shark_count > 0 and player.karambwan_count > 0:
        player.eat_shark_and_karambwan()
    elif player.hp < 60 and player.shark_count > 0:
        player.eat_shark()
    else:
        if player.zamorak_brew_count > 0 and player.hp > 60:
            player.drink_zamorak_brew()
        player.throw_knives(opponent)
        player.attack(opponent)

def strategy5(player, opponent):
    if opponent.hp < player.hp:
        if player.zamorak_brew_count > 0 and player.hp > 11:
            player.drink_zamorak_brew()
        player.throw_knives(opponent)
        player.attack(opponent)
    elif player.hp < 40 and player.shark_count > 0 and player.karambwan_count > 0:
        player.eat_shark_and_karambwan()
    else:
        player.throw_knives(opponent)
        player.attack(opponent)

def strategy6(player, opponent):
    opponent_max_hit = 44 + (42 * ((99 - opponent.hp) // 98))
    if player.zamorak_brew_count > 0 and player.hp > (opponent_max_hit + 11):
        player.drink_zamorak_brew()
    if opponent_max_hit < player.hp:
        player.throw_knives(opponent)
        player.attack(opponent)
    else:
        if player.hp + 38 <= 99 and player.shark_count > 0 and player.karambwan_count > 0:
            player.eat_shark_and_karambwan()
        elif player.shark_count > 0:
            player.eat_shark()
        else:
            player.throw_knives(opponent)
            player.attack(opponent)

def simulate_game(strategy1, strategy2, debug=False): # we should probably pass strategy names into player names
    player1 = Player("Player 1", debug=debug)
    player2 = Player("Player 2", debug=debug)
    player1.strategy = strategy1
    player2.strategy = strategy2
    
    players = [player1, player2]
    random.shuffle(players)
    
    while player1.hp > 0 and player2.hp > 0:
        current_player = players[0]
        opponent = players[1]
        current_player.choose_action(opponent)
        
        if opponent.hp <= 0:
            return current_player.name
        
        players.reverse()

def run_simulations(n_sims=100):
    strategies = [strategy1, strategy2, strategy3, strategy4, strategy5, strategy6]
    strategy_names = ["2-tick", "yolo", "???", "Safer", "Opponent hp", "actual safer"]
    results = {name: {name: 0 for name in strategy_names} for name in strategy_names}
    
    for i, strat1 in enumerate(strategies):
        for j, strat2 in enumerate(strategies):
            if i != j:
                wins = 0
                for _ in range(n_sims):
                    winner = simulate_game(strat1, strat2)
                    if winner == "Player 1":
                        wins += 1
                results[strategy_names[i]][strategy_names[j]] = wins
                results[strategy_names[j]][strategy_names[i]] = n_sims - wins

    return results

results = run_simulations(n_sims=1000)
for strategy, outcomes in results.items():
    print(f"{strategy} results:")
    for opponent_strategy, wins in outcomes.items():
        print(f"  Against {opponent_strategy}: {wins} wins")
