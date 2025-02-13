from player import *
from monster import *
import pickle
from lists import *


def fight_loop(player, monster):
    player_counter = 0
    monster_counter = 0
    for item in lists.actions:
        print(item.capitalize())

    while player.hp > 0 and monster.hp > 0: # Player goes first
        player_counter += 1
        if player.agility > monster.agility:
            while player.action_used != player.action_points:
                print(f'It\'s {player.name}\'s turn!')
                print(f'{player.hp}/{player.hp_max}')
                action = input(f'What will {player.name} do?')
                player.action_used += 1
                if action.lower == 'strike' or 'magic':
                    query = input('Are they targeting themself? ')
                    if query.lower() == 'y' or query.lower() == 'yes':
                        player.action(action)
                    else:
                        player.action(action, monster)

            player.action_used = 0
            if monster.hp == 0:
                break
            monster_counter += 1
            while monster.action_used != monster.action_number:
                action = input(f'What will {monster.name} do?')
                if action.lower() == 'strike' or 'magic':
                    query = input('Are they targeting themself? ')
                    monster.action_used += 1
                    if query.lower() == 'y' or query.lower() == 'yes':
                        monster.action(action)
                    else:
                        monster.action(action, player)

            monster.action_used = 0

        else: # Monster goes first
            monster_counter += 1
            while monster.action_used != monster.action_number:
                action = input(f'What will {monster.name} do?')
                if action.lower == 'strike' or 'magic':
                    query = input('Are they targeting themself? ')
                    if query.lower() == 'y' or query.lower() == 'yes':
                        monster.action(action)
                    else:
                        monster.action(action, player)
            monster.action_used = 0

            if player.hp == 0:
                break

            player_counter += 1

            while player.action_used != player.action_points:
                print(f'It\'s {player.name}\'s turn!')
                action = input(f'What will {player.name} do?')
                player.action_used += 1
                if action.lower == 'strike' or 'magic':
                    query = input('Are they targeting themself? ')
                    if query.lower() == 'y' or query.lower() == 'yes':
                        player.action(action)
                    else:
                        player.action(action, monster)

    if player.hp > 0:

        gold_gain = 100 * player_counter
        player.gold += gold_gain
        exp_gain = 50 * player_counter
        player.exp += exp_gain
        points_gain = monster_counter
        monster.points += points_gain
        player.wins += 1
        print(f'{player.name} is victorious!')
        print(f'{player.name} gains {gold_gain} gold and {exp_gain} experience!')
        print(f'{monster.name} gains only {points_gain} points')
        if player.exp >= player.exp_max:
            player.level += 1
            print(f'{player.name} is now level {player.level}!')
            player.class_adjust(player.char_class)

    elif player.hp <= 0:  # Player loses
        gold_gain = 50 * player_counter
        player.gold += gold_gain
        exp_gain = 25 * player_counter
        player.exp += exp_gain
        points_gain = monster_counter*2
        monster.points += points_gain
        player.losses += 1
        print(f"{player.name} has been defeated!")
        print(f'{player.name} gains only {gold_gain} gold and {exp_gain} experience.')
        print(f'{monster.name} gains {points_gain} points')
        if player.exp >= player.exp_max:
            player.level += 1
            print(f'{player.name} is now level {player.level}.')
            player.class_adjust(player.char_class)


def new_game():
    new_name = input('Input player name: ')
    new_char_class = input('Input class ')
    player = Player(new_name, new_char_class)

    new_mon = input('Name your foe: ')
    monster = Monster(new_mon, 'goblin')

    return player, monster


def save(entity):
    name = input('Input save name: ')
    filename = name + '.pkl'
    with open(filename, 'wb') as output:
        pickle.dump(entity, output, pickle.HIGHEST_PROTOCOL)


def load_player():
    name = input('Input save name: ')
    filename = name + '.pkl'
    with open(filename, 'rb') as inp:
        result = pickle.load(inp)
    return result


def load_monster():
    name = input('Input save name: ')
    filename = name + '.pkl'
    with open(filename, 'rb') as inp:
        result = pickle.load(inp)
    return result


def main():
    player = None
    monster = None
    query = input('Load a player? ')
    if query in ['y', 'yes']:
        player = load_player()

    query = input('Load a monster? ')
    if query in ['y', 'yes']:
        monster = load_monster()

    if player is None or monster is None:
        player, monster = new_game()
    fight_loop(player, monster)

    save()


if __name__ == '__main__':
    main()






