from ursina import *

class Player(Animation):
    def __init__(self, **kwargs):
        super().__init__(
            'sprites/player1/idle/torchy', 
            fps=6,
            loop=True,
            scale=(2, 2.7),
            position=(-4.5, -2.5, 0),
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

        # Memory Input System (future mechanic)
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
            return True  # player died
        return False

    def unlock_abilities_by_level(self):
        if self.level >= 2 and 'Blast' not in self.abilities:
            self.abilities.append('Blast')
        if self.level >= 5 and 'Blaze' not in self.abilities:
            self.abilities.append('Blaze')
        if self.level >= 10 and 'Hellfire' not in self.abilities:
            self.abilities.append('Hellfire')
