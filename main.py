from player import *

test = Player('test', 'warrior')
test2 = Player('test', 'mage')
test3 = Player('test', 'rogue')
test4 = Player('test', 'berserker')

test2.action('magic', test2)

print(test2.accuracy)
test2.learn_spell('mist veil')
test2.cast_spell('mist veil', test2)
print(test2.accuracy)

