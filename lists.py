

# stats for each spell: cost, damage, element, accuracy penalty, special effect, bonus, duration (if
# applicable)
spells = {
    'fireball': [10, 30, 'fire', 10, None, 0],
    'arcane bolt': [5, 15, 'occult', 5, None, 0],
    'eagle eye': [5, 0, None, 0, 'accuracy_boost', 20, 3],
    'mist veil': [9, 0, None, 0, 'accuracy_penalty', 10, 3],
    'bone chill': [15, 20, 'ice', 15, 'chilled', 0, 3],
    'haste': [20, 0, None, 0, 'agility_boost']
}

# adjustments are, in order: hp, mp, str, defense, magic, resistance, agility
char_class = {'warrior': [10, -5, 8, 5, -5, -8, 4],
              'mage': [2, 10, 2, -5, 8, 5, 5],
              'rogue': [6, -3, 6, -3, 4, -3, 10],
              'berserker': [15, -10, 10, 10, -10, -10, 0]}

# monster class adjustment hp, mp, str, defense, magic, resistance, agility, abilities
monster_class = {'goblin': [20, 10, 15, 12, 10, 10, 9, ['sunder']],
                 'ogre': [30, 10, 25, 15, 0, 10, 5, ['rend', 'sunder']],
                 'orc': [40, 5, 30, 20, 5, 2, 10, ['rend', 'thrash']]

                 }

actions = ['strike', 'defend', 'magic', 'item']

# weapon stats are: cost, weapon bonus and accuracy penalty
char_weapons = {
    'unarmed': [0, 1, 0],
    'dagger': [10, 5, 0],
    'bronze sword': [12, 8, 5],
    'bronze axe': [18, 12, 8],
    'club': [15, 9, 7],
    'sling': [5, 2, 6],

}

char_armor = {}

# ability stats are: attack bonus, cooldown, accuracy penalty, element, special effect, effect intensity, effect duration
monster_abilities = {
    'rend': [10, 2, 10, 'physical', None, 0, 0],
    'sunder': [5, 3, 15, 'physical', 'defense_down', 10, 3],
    'thrash': [20, 5, 25, 'physical', None, 0, 0],
    'fire breath': [50, 8, 5, 'fire', None, 0, 0],
    'frost breath': [45, 8, 5, 'ice', 'speed_penalty', 20, 4],
    'lightning breath': [45, 8, 5, 'lightning', 'accuracy_penalty', 30, 4]
}