class LevelSystem:
    def __init__(self, player):
        self.player = player
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.abilities_unlocked = set()
        self.unlocks = {
            2: 'Blast',
            5: 'Blaze',
            10: 'Hellfire'
        }

    def add_xp(self, amount):
        self.xp += amount
        print(f"Gained {amount} XP! Total: {self.xp}/{self.xp_to_next}")
        if self.xp >= self.xp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5)
        print(f"Level up! You are now level {self.level}!")

        if self.level in self.unlocks:
            ability = self.unlocks[self.level]
            self.player.abilities.append(ability)
            self.abilities_unlocked.add(ability)
            print(f"Unlocked new ability: {ability}!")

        if self.xp >= self.xp_to_next:
            self.level_up()

