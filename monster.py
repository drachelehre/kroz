from creature import Creature
import lists
import random


class Monster(Creature):
    def __init__(self, name, mon_class):
        super().__init__(name, char_class=mon_class)
        self.hp_max = 0
        self.hp = self.hp_max
        self.mp_max = 0
        self.mp = self.mp_max
        self.str = 0
        self.defense = 0
        self.magic = 0
        self.resistance = 0
        self.agility = 0
        self.weapon = 'unarmed'  # Store weapon as a string
        self.weapon_bonus = 0  # Track attack boost separately
        self.armor = 'unarmored'
        self.attack = self.str
        self.toughness = self.defense
        self.effects = {}
        self.abilities = []
        self.monster_adjust(mon_class)
        self.accuracy = 100

    def __repr__(self):
        return (f'name={self.name}, max_hp={self.hp_max}, mp_max={self.mp_max}, '
                f'str={self.str}, def={self.defense}, magic={self.magic}, res={self.resistance}, '
                f'agility={self.agility}, weapon={self.weapon}, abilities={self.abilities}')

    def monster_adjust(self, mon_class):
        mon_class = mon_class.lower()
        stats = lists.monster_class.get(mon_class)

        if stats is None:
            print(f"Warning: Monster class '{mon_class}' not found! Using default stats.")
            self.hp_max = 10
            self.hp = self.hp_max
            self.mp_max = 0
            self.mp = self.mp_max
            self.str = 5
            self.defense = 5
            self.magic = 0
            self.resistance = 5
            self.agility = 5
            self.abilities = []
            return

        # Unpack stats safely
        (hp, mp, strength, defense, magic, res, agility, abilities) = stats

        # Apply stats
        self.hp_max = hp
        self.hp = self.hp_max
        self.mp_max = mp
        self.mp = self.mp_max
        self.str = strength
        self.defense = defense
        self.magic = magic
        self.resistance = res
        self.agility = agility
        self.abilities = abilities or []  # Ensure abilities is always a list

    def strike(self, target):
        weapon = lists.char_weapons[self.weapon]
        _, bonus, accuracy_penalty = weapon
        weapon_accuracy = max(0, self.accuracy - accuracy_penalty)  # Ensure accuracy isn't negative
        check = random.randint(1, 100)  # Use 1-100 instead of 0-101

        print(f"Weapon Accuracy: {weapon_accuracy} | Roll: {check}")  # Debugging info

        if check > weapon_accuracy:
            print("Missed!")
            return

        base_damage = self.str + bonus

        if base_damage > 0:
            min_damage = int(base_damage * 0.9)  # 90% of base damage
            max_damage = int(base_damage * 1.1)  # 110% of base damage
            final_damage = random.randint(min_damage, max_damage)  # Pick a random value in range
            print(f"{self.name} hits {target.name} with {self.weapon} for {final_damage} damage!")
            target.take_damage(final_damage)
        return True

    def use_ability(self, ability_name, target=None):
        print(f"Spellbook: {self.abilities}")  # Debugging output

        # Ensure the spell exists and the player has learned it
        if ability_name not in lists.monster_abilities or ability_name not in self.abilities:
            print(f"Spell '{ability_name}' not found or not learned!")
            return False

        spell = lists.spells[ability_name]
        cost, base_damage, element, accuracy_penalty, special_effect, bonus, *duration = spell

        # Ensure the player has enough MP
        if self.mp < cost:
            print(f"{self.name} does not have enough MP to cast {ability_name}!")
            return False

        self.mp -= cost  # Deduct MP cost
        print(f"{self.name} casts {ability_name}!")

        # Default target to self if not specified
        if target is None:
            target = self

        # Handle spell effects
        if special_effect == 'accuracy_boost':
            duration = duration if duration else 3  # Default duration 3 turns if not specified
            target.effects['accuracy_boost'] = [bonus, duration]
            target.accuracy += bonus  # Apply buff immediately
            print(f"{target.name}'s accuracy increased by {bonus} for {duration} turns!")
        if special_effect == 'accuracy_penalty':
            duration = duration if duration else 3  # Default duration 3 turns if not specified
            target.effects['accuracy_penalty'] = [bonus, duration]
            target.accuracy -= bonus  # Apply buff immediately
            print(f"{target.name}'s accuracy decreased by {bonus} for {duration} turns!")
        if special_effect == 'chilled':
            duration = duration if duration else 3  # Default duration 3 turns if not specified
            target.effects['chilled'] = [bonus, duration]
            target.agility /= 2  # Apply buff immediately
            print(f"{target.name}'s agility cut in half for {duration} turns!")


        # Apply 10% damage variation (±10%)
        if base_damage > 0:
            # Determine if spell hits
            ability_accuracy = max(0, self.accuracy - accuracy_penalty)  # Ensure accuracy isn't negative
            check = random.randint(1, 100)  # Use 1-100 instead of 0-101

            print(f"Spell Accuracy: {ability_accuracy} | Roll: {check}")  # Debugging info

            if check > ability_accuracy:
                print("Missed!")
                return

            min_damage = int(base_damage * 0.9)  # 90% of base damage
            max_damage = int(base_damage * 1.1)  # 110% of base damage
            final_damage = random.randint(min_damage, max_damage)  # Pick a random value in range
            target.hp -= max(0, final_damage)  # Ensure damage isn't negative
            print(f"{ability_name} hits {target.name} for {final_damage} {element} damage!")
            target.take_damage(final_damage)
        return True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def heal(self, heal):
        self.hp += heal
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def effect_check(self):
        """Processes active buffs and removes expired ones at the start of each turn."""
        to_remove = []

        for effect, (value, turns) in self.effects.items():
            if turns > 1:
                self.effects[effect][1] -= 1  # Decrease effect duration
            else:
                # Remove expired buffs
                to_remove.append(effect)

        # Remove buffs and revert effects
        for effect in to_remove:
            value, _ = self.effects.pop(effect)
            if effect == "accuracy_boost":
                self.accuracy -= value  # Revert accuracy boost
                print(f"{self.name}'s accuracy returned to normal!")
            if effect == 'accuracy_penalty':
                self.accuracy += value
                print(f"{self.name} can see target normally again!")
            if effect == "attack_boost":
                self.attack -= value  # Revert attack boost
                print(f"{self.name}'s attack returned to normal!")
            if effect == 'attack_penalty':
                self.attack += value
                print(f"{self.name} feels strong again!")
            if effect == "defending":
                self.toughness = self.defense
                print(f'{self.name} lowers their defense.')
            if effect == 'chilled':
                self.agility *= 2
                self.agility = int(self.agility)  # return to integer
                print(f'{self.name}\'s temperature is back to normal!')
            if effect == 'speed_boost':
                self.agility /= 2
                self.agility = int(self.agility)  # return to integer
                print(f'{self.name}\'s speed is back to normal')

