class Creature:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class

        # Base stats for all creatures (default values)
        self.hp_max = 10
        self.hp = self.hp_max
        self.mp_max = 5
        self.mp = self.mp_max
        self.str = 5
        self.defense = 5
        self.magic = 5
        self.resistance = 5
        self.agility = 5
        self.effects = {}  # Dictionary to track buffs/debuffs

    def class_adjust(self, char_class):
        """This method should be overridden by subclasses."""
        raise NotImplementedError(f"{self.__class__.__name__} must implement class_adjust()")

    def action(self, act, target=None):
        """This should be overridden in Player or Monster."""
        raise NotImplementedError(f"{self.__class__.__name__} must implement action()")

    def __repr__(self):
        return (f"name={self.name}, class={self.char_class}, max_hp={self.hp_max}, hp={self.hp}, "
                f"mp_max={self.mp_max}, mp={self.mp}, str={self.str}, defense={self.defense}, "
                f"magic={self.magic}, res={self.resistance}, agility={self.agility}")
