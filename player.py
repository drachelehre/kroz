from creature import *
import lists
import random


class Player(Creature):
    def __init__(self, name, char_class):
        super().__init__(name, char_class)
        self.level = 1
        self.exp = 0
        self.gold = 100
        self.hp_max = 10
        self.hp = self.hp_max
        self.mp_max = 10
        self.mp = self.mp_max
        self.str = 10
        self.defense = 10
        self.magic = 10
        self.resistance = 10
        self.agility = 10
        self.weapon = None  # Store weapon as a string
        self.weapon_bonus = 0  # Track attack boost separately
        self.armor = None
        self.attack = self.str
        self.toughness = self.defense
        self.effects = {}
        self.accuracy = 100
        self.spellbook = []
        self.class_adjust(char_class)

    def __repr__(self):
        return (f'name={self.name}, level={self.level}, exp={self.exp}, max_hp={self.hp_max}, mp_max={self.mp_max}, '
                f'str={self.str}, def={self.defense}, magic={self.magic}, res={self.resistance}, '
                f'agility={self.agility}, weapon={self.weapon}')

    def class_adjust(self, char_class):
        char_class = char_class.lower()
        stats = lists.char_class.get(char_class)

        if stats:
            (hp_bonus, mp_bonus, str_bonus, def_bonus, magic_bonus, res_bonus, agility_bonus) = stats

            # Apply stat adjustments, ensuring no negative values where necessary
            self.hp_max = max(1, self.hp_max + hp_bonus)
            self.hp = self.hp_max  # Restore HP to new max
            self.mp_max = max(0, self.mp_max + mp_bonus)  # Ensure MP doesn't go negative
            self.mp = self.mp_max
            self.str = max(1, self.str + str_bonus)
            self.defense = max(0, self.defense + def_bonus)  # Defense can be 0, but not negative
            self.magic = max(0, self.magic + magic_bonus)
            self.resistance = max(0, self.resistance + res_bonus)
            self.agility = max(1, self.agility + agility_bonus)

        else:
            print("Class doesn’t exist or isn’t implemented.")

        if char_class == 'mage':
            self.spellbook.append('arcane bolt')  # Add a starting spell for mages

    def equip_weapon(self, weapon):
        weapon_stats = lists.char_weapons.get(weapon)

        if weapon_stats:
            # Unequip current weapon first (to remove its attack bonus)
            if self.weapon:
                self.unequip_weapon()

            self.weapon = weapon
            self.weapon_bonus = weapon_stats[1]  # Store attack boost separately
            self.attack = self.str + self.weapon_bonus  # Ensure attack is correctly recalculated
            print(f'{self.name} equipped the {weapon}')
        else:
            print(f'{weapon} is not a valid weapon.')

    def unequip_weapon(self):
        if self.weapon:
            print(f'{self.name} unequipped the {self.weapon}')
            self.attack = self.str  # Reset attack to base strength
            self.weapon = None
            self.weapon_bonus = 0
        else:
            print(f'{self.name} has no weapon equipped.')

    def learn_spell(self, spell_name):
        if spell_name.lower() not in lists.spells:
            print('Spell is misspelled or does not exist!')
            return False
        self.spellbook.append(spell_name.lower())
        return True

    def cast_spell(self, spell_name, target=None):
        print(f"Spellbook: {self.spellbook}")  # Debugging output

        # Ensure the spell exists and the player has learned it
        if spell_name not in lists.spells or spell_name not in self.spellbook:
            print(f"Spell '{spell_name}' not found or not learned!")
            return False

        spell = lists.spells[spell_name]
        cost, base_damage, element, accuracy_penalty, special_effect, bonus, *duration = spell

        # Ensure the player has enough MP
        if self.mp < cost:
            print(f"{self.name} does not have enough MP to cast {spell_name}!")
            return False

        self.mp -= cost  # Deduct MP cost
        print(f"{self.name} casts {spell_name}!")

        # Determine if spell hits
        spell_accuracy = max(0, self.accuracy - accuracy_penalty)  # Ensure accuracy isn't negative
        check = random.randint(1, 100)  # Use 1-100 instead of 0-101

        print(f"Spell Accuracy: {spell_accuracy} | Roll: {check}")  # Debugging info

        if check > spell_accuracy:
            print("Missed!")
            return

        # Default target to self if not specified
        if target is None:
            target = self

        # Handle spell effects
        if special_effect == 'accuracy_boost':
            duration = duration[0] if duration else 3  # Default duration 3 turns if not specified
            target.effects['accuracy_boost'] = [bonus, duration]
            target.accuracy += bonus  # Apply buff immediately
            print(f"{target.name}'s accuracy increased by {bonus} for {duration} turns!")
        if special_effect == 'accuracy_penalty':
            duration = duration[0] if duration else 3  # Default duration 3 turns if not specified
            target.effects['accuracy_penalty'] = [bonus, duration]
            target.accuracy -= bonus  # Apply buff immediately
            print(f"{target.name}'s accuracy decreased by {bonus} for {duration} turns!")

        # Apply 10% damage variation (±10%)
        if base_damage > 0:
            min_damage = int(base_damage * 0.9)  # 90% of base damage
            max_damage = int(base_damage * 1.1)  # 110% of base damage
            final_damage = random.randint(min_damage, max_damage)  # Pick a random value in range
            target.hp -= max(0, final_damage)  # Ensure damage isn't negative
            print(f"{spell_name} hits {target.name} for {final_damage} {element} damage!")


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
                print(f"{self.name}'s can see target normally again!")