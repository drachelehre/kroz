from player import *
from monster import *
from lists import *


player = Player('test', 'warrior')

monster = Monster('gob', 'goblin')
player.hp = 4

def fight_loop():
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
        print(f"{player.name} has been defeated!")
        print(f'{player.name} gains only {gold_gain} gold and {exp_gain} experience.')
        print(f'{monster.name} gains {points_gain} points')
        if player.exp >= player.exp_max:
            player.level += 1
            print(f'{player.name} is now level {player.level}.')
            player.class_adjust(player.char_class)


def main():
    fight_loop()



if __name__ == '__main__':
    main()






