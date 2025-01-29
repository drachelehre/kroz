from creature import *


class Monster(Creature):
    def __init__(self, name, char_class):
        super().__init__(name, char_class)
        self.level = 1
        self.exp = 0
        self.weapon = None
        self.armor = None
        self.spellbook = []
