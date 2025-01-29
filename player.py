from creature import *


class Player(Creature):
    def __init__(self, name, char_class):
        super().__init__(name, char_class)
        self.level = 1
        self.exp = 0
        self.hp_max = 10
        self.hp = self.hp_max
        self.mp_max = 10
        self.mp = self.mp_max
        self.str = 10
        self.defense = 10
        self.magic = 10
        self.resistance = 10
        self.agility = 10
        self.weapon = None
        self.armor = None
        self.spellbook = []
        self.class_adjust(self.char_class)

    def class_adjust(self, char_class):
        pass

