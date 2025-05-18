from ursina import *

class InventorySystem:
    def __init__(self, player, zone_system):
        self.player = player
        self.zone_system = zone_system
        self.items = ['Vodka'] * 12
        self.buttons = []
        self.menu = None

    def open_inventory(self):
        if self.menu:
            destroy(self.menu)
            for b in self.buttons:
                destroy(b)
            self.buttons.clear()
            return

        self.menu = Entity(parent=camera.ui)
        for i, item in enumerate(self.items):
            x = (i % 4) * 0.15 - 0.3
            y = -(i // 4) * 0.15 + 0.3
            btn = Button(
                text=item,
                parent=self.menu,
                position=Vec2(x, y),
                scale=(.12, .12),
                color=color.white,
                on_click=lambda i=i: self.use_item(i)
            )
            self.buttons.append(btn)

    def use_item(self, index):
        item = self.items[index]
        if item == 'Vodka':
            self.player.health_bar.value = min(100, self.player.health_bar.value + 50)
            self.zone_system.add_fuel(2)
            print("Torchy drank Vodka, healed 50 and gained 2 fuel!")

        destroy(self.menu)
        for b in self.buttons:
            destroy(b)
        self.buttons.clear()
