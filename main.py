from player import *
from monster import *
from lists import *


player = Player('test', 'warrior')

monster = Monster('gob', 'goblin')


def fight_loop():
    player_counter = 0
    monster_counter = 0
    for item in lists.actions:
        print(item.capitalize())
    while player.hp > 0 and monster.hp > 0:
        player_counter += 1
        monster_counter += 1
        if player.agility > monster.agility:
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
            while monster.action_used != monster.action_number:
                action = input(f'What will {monster.name} do?')
                if action.lower() == 'strike' or 'magic':
                    query = input('Are they targeting themself? ')
                    monster.action_used += 1
                    if query.lower() == 'y' or query.lower() == 'yes':
                        monster.action(action)
                    else:
                        monster.action(action, player)
        else:
            while monster.action_used != 0:
                action = input(f'What will {monster.name} do?')
                if action.lower == 'strike' or 'magic':
                    query = input('Are they targeting themself? ')
                    if query.lower() == 'y' or query.lower() == 'yes':
                        monster.action(action)
                    else:
                        monster.action(action, player)
    if player.hp <= 0:
        player.gold += 50 * player_counter
        player.exp += 25 * player_counter
        if player.exp >= player.exp_max:
            player.level += 1
            player.class_adjust(player.char_class)



def main():
    fight_loop()


if __name__ == '__main__':
    main()






