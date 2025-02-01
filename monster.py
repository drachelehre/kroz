from creature import *


class Monster(Creature):
    def __init__(self, name, monster_class):
        super().__init__(name, char_class=monster_class)
        self.level = 1
        self.exp = 0
        self.weapon = None
        self.armor = None
        self.abilities = []
        self.monster_adjust()

    def monster_adjust(self):
        pass