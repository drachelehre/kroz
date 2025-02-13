from creature import Creature
import lists
import random
import gym


class Player(Creature):
    def __init__(self, name, char_class):
        super().__init__(name, char_class)
        self.action_points = 1
        self.bonus_action = 0
        self.action_used = 0
        self.wins = 0
        self.losses = 0
        self.level = 1
        self.exp = 0
        self.exp_max = 150
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
        self.weapon = 'unarmed'  # Store weapon as a string
        self.weapon_bonus = 0 # Track attack boost separately
        self.armor = 'unarmored'
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

    def action(self, act, target=None):
        act = act.lower()  # Normalize input to lowercase

        match act:
            case 'strike':
                self.strike(target)

            case 'defend':
                self.effects['defending'] = [self.toughness * 2, 1]
                print(f"{self.name} braces for impact, doubling defense for 1 turn!")

            case 'magic':
                for spell in self.spellbook:
                    print(spell)

                spell_cast = input("What do you want to cast? ").lower()

                if spell_cast not in self.spellbook:
                    print(f"{self.name} does not know {spell_cast}!")
                    return
                query = input("Are you casting on yourself (y/n)? ")

                if query.lower() == 'y':
                    target = None

                if target is None:
                    self.cast_spell(spell_cast)
                else:
                    self.cast_spell(spell_cast, target)

            case _:
                print("Invalid command. Available actions: strike, defend, magic.")

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
            if special_effect == 'chilled':
                duration = duration[0] if duration else 3  # Default duration 3 turns if not specified
                target.effects['chilled'] = [bonus, duration]
                target.agility /= 2  # Apply buff immediately
                print(f"{target.name}'s agility cut in half for {duration} turns!")

        # Damage calculation for attacking spells
        if base_damage > 0:
            # Determine if spell hits
            spell_accuracy = max(0, self.accuracy - accuracy_penalty)  # Ensure accuracy isn't negative
            check = random.randint(1, 100)  # Use 1-100 instead of 0-101

            print(f"Spell Accuracy: {spell_accuracy} | Roll: {check}")  # Debugging info

            min_damage = int(base_damage * 0.9)  # 90% of base damage
            max_damage = int(base_damage * 1.1)  # 110% of base damage
            final_damage = random.randint(min_damage, max_damage)  # Pick a random value in range
            print(f"{spell_name} hits {target.name} for {final_damage} {element} damage!")
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
        to_remove = list(self.effects.keys())  # Ensure safe removal of expired effects

        for effect in to_remove:
            value, turns = self.effects[effect]

            if turns > 1:
                self.effects[effect][1] -= 1  # Reduce duration
            else:
                self.effects.pop(effect)  # Remove effect

                # Handle effect expiration
                match effect:
                    case "accuracy_boost":
                        self.accuracy -= value
                        print(f"{self.name}'s accuracy returned to normal!")
                    case "accuracy_penalty":
                        self.accuracy += value
                        print(f"{self.name} can see normally again!")
                    case "attack_boost":
                        self.attack -= value
                        print(f"{self.name}'s attack returned to normal!")
                    case "attack_penalty":
                        self.attack += value
                        print(f"{self.name} feels strong again!")
                    case "defending":
                        self.toughness = self.defense
                        print(f"{self.name} lowers their defense.")
                    case "chilled":
                        self.agility *= 2
                        self.agility = int(self.agility)  # Ensure integer agility
                        print(f"{self.name}'s temperature is back to normal!")
                    case "speed_boost":
                        self.agility /= 2
                        self.agility = int(self.agility)
                        print(f"{self.name}'s speed is back to normal!")

    def pass_turn(self, other):
        other.action_used = 0
