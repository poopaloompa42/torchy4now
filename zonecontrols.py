from ursina import *
from ursina.prefabs.health_bar import HealthBar

ZONES = [1.5, 0, -1.5]

class ZoneControls:
    def __init__(self, player):
        self.player = player
        self.zone_level = 1
        self.fuel = 5

        self.fuel_bar = HealthBar(
            parent=camera.ui,
            position=Vec2(0, 0.38),
            scale=(0.4, 0.03),
            max_value=10,
            bar_color=color.orange
        )
        self.fuel_bar.value = self.fuel

        self.zone_label = Text(
            text=f"ZONE: {self.zone_level}",
            position=(-0.05, 0.35),
            scale=2,
            parent=camera.ui
        )
        self.fuel_label = Text(
            text=f"Fuel: {self.fuel}",
            position=(-0.05, 0.3),
            scale=2,
            parent=camera.ui
        )

        self.zone_down_button = Button(
            text='Take Flight',
            parent=camera.ui,
            position=Vec2(-0.7, -0.3),
            scale=(.15, .08),
            color=color.azure,
            on_click=self.lower_zone
        )

    def get_zone_y(self):
        return ZONES[self.zone_level]

    def set_player(self, player):
        self.player = player

    def move_down_zone(self):
        if self.zone_level < len(ZONES) - 1:
            self.zone_level += 1
            self.player.y = self.get_zone_y()
            print(f"Moved to zone {self.zone_level}")
        else:
            print("Already in lowest zone!")
        self.update_ui()

    def zone_action(self):
        if self.fuel > 0 and self.zone_level < len(ZONES) - 1:
            self.fuel -= 1
            self.zone_level += 1
            print(f"Zone raised to {self.zone_level}, fuel remaining: {self.fuel}")
        else:
            if self.fuel == 0:
                print("Not enough fuel to raise zone!")
            elif self.zone_level >= len(ZONES) - 1:
                print("Already at max zone!")
        self.update_ui()
        self.player.y = ZONES[self.zone_level]

    def lower_zone(self):
        if self.zone_level > 0:
            self.zone_level -= 1
            print(f"Zone lowered to {self.zone_level}")
        else:
            print("Already at lowest zone!")
        self.update_ui()
        self.player.y = ZONES[self.zone_level]

    def update_ui(self):
        self.zone_label.text = f"Zone: {self.zone_level}"
        self.fuel_label.text = f"Fuel: {self.fuel}"
        self.fuel_bar.value = self.fuel

    def add_fuel(self, amount):
        self.fuel = min(10, self.fuel + amount)
        self.update_ui()

    def get_zone_and_fuel(self):
        return self.zone_level, self.fuel
