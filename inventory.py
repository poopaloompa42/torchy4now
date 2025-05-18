from ursina import *

class InventorySystem:
    def __init__(self, player, zone_system, ui_manager):
        self.player = player
        self.zone_system = zone_system
        self.ui_manager = ui_manager
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
            self.player.hp = min(self.player.max_hp, self.player.hp + 50)
            self.zone_system.add_fuel(2)
            print("Torchy drank Vodka, healed 50 and gained 2 fuel!")
            self.ui_manager.update_hp()  # <-- now safe to use

        destroy(self.menu)
        for b in self.buttons:
            destroy(b)
        self.buttons.clear()

