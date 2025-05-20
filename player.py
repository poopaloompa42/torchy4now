from ursina import *

class Player(Animation):
    def __init__(self, **kwargs):
        super().__init__(
            'sprites/player1/idle/torchy', 
            fps=6,
            loop=True,
            scale=(2, 2.7),
            z=-1,
            **kwargs
        )
        self.name = 'Torchy'

        # Core Stats
        self.hp = 100
        self.max_hp = 100
        self.fuel = 10
        self.max_fuel = 10

        # Leveling / XP
        self.level = 1
        self.xp = 0
        self.max_xp = 100
        self.xp_segments_full = 0
        self.max_xp_segments = 5

        # Abilities
        self.abilities = []

        # Memory Input System
        self.memorized_sequence = []
        self.is_memorizing = False

    def take_damage(self, amount, ui_manager=None):
        self.hp = max(0, self.hp - amount)
        print(f"{self.name} takes {amount} damage! Current HP: {self.hp}")
        if ui_manager:
            ui_manager.update_hp()
        if self.hp <= 0:
            print(f"{self.name} has been defeated!")
            destroy(self)
            return True
        return False

    def heal(self, amount, ui_manager=None):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} heals {amount} HP. Current HP: {self.hp}")
        if ui_manager:
            ui_manager.update_hp()

    def restore_fuel(self, amount, ui_manager=None):
        self.fuel = min(self.max_fuel, self.fuel + amount)
        print(f"{self.name} restores {amount} fuel. Current fuel: {self.fuel}")
        if ui_manager:
            ui_manager.update_fuel()

    def unlock_abilities_by_level(self):
        if self.level >= 2 and 'Blast' not in self.abilities:
            self.abilities.append('Blast')
        if self.level >= 5 and 'Blaze' not in self.abilities:
            self.abilities.append('Blaze')
        if self.level >= 10 and 'Hellfire' not in self.abilities:
            self.abilities.append('Hellfire')

    def add_xp(self, amount, ui_manager=None):
        self.xp += amount
        print(f"{self.name} gains {amount} XP. Total: {self.xp}/{self.max_xp}")
        while self.xp >= self.max_xp:
            self.level_up(ui_manager)
        if ui_manager:
            ui_manager.update_xp()

    def level_up(self, ui_manager=None):
        self.level += 1
        self.xp -= self.max_xp
        self.max_xp = int(self.max_xp * 1.5)
        print(f"{self.name} leveled up to {self.level}!")

        if ui_manager:
            ui_manager.show_level_up_choices(self.level, self)
        else:
            self.unlock_abilities_by_level()

    def start_memorizing(self):
        self.is_memorizing = True
        self.memorized_sequence = []
        print("Memorization started.")

    def add_memorized_input(self, direction):
        if self.is_memorizing:
            self.memorized_sequence.append(direction)
            print(f"Input '{direction}' added to memory sequence.")

    def increase_max_hp(self, amount):
        self.max_hp += amount
        self.hp = self.max_hp
        print(f"{self.name}'s max HP increased to {self.max_hp}")

    def increase_max_fuel(self, amount):
        self.max_fuel += amount
        self.fuel = self.max_fuel
        print(f"{self.name}'s max fuel increased to {self.max_fuel}")

    def unlock_ability(self, name):
        if name not in self.abilities:
            self.abilities.append(name)
            print(f"{self.name} unlocked ability: {name}")
