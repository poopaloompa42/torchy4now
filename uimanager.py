from ursina import *

class UIManager:
    def __init__(self, player):
        self.player = player
        self.hp_icons = []
        self.fuel_icons = []
        self.xp_icons = []

        self.inventory_bg = None
        self.down_zone_button = None

    def update_meter(self, icon_type, value, max_value, icon_list, start_pos, spacing):
        for icon in icon_list:
            destroy(icon)
        icon_list.clear()

        for i in range(max_value):
            suffix = 'f' if i < value else 'e'
            texture = f'assets/sprites/premade buttons/{icon_type}{suffix}.jpg'
            icon = Sprite(
                texture=texture,
                parent=camera.ui,
                position=(start_pos[0] + i * spacing, start_pos[1]),
                scale=0.1
            )
            icon_list.append(icon)

    def update_hp(self):
        hearts = int(self.player.hp / 25)
        max_hearts = int(self.player.max_hp / 25)
        self.update_meter('hp', hearts, max_hearts, self.hp_icons, start_pos=(-0.45, 0.45), spacing=0.09)

    def update_fuel(self):
        self.update_meter('fuel', self.player.fuel, self.player.max_fuel, self.fuel_icons, start_pos=(-0.5, 0.38), spacing=0.06)

    def update_xp(self):
        self.update_meter('exp', self.player.xp_segments_full, self.player.max_xp_segments, self.xp_icons, start_pos=(-0.5, 0.31), spacing=0.06)

    def update_ui(self, zone_level=None, fuel=None):
        pass

    def create_downzone_button(self, on_click_callback):
        self.down_zone_button = Button(
            texture='assets/sprites/premade buttons/downzone.jpg',
            parent=camera.ui,
            position=(0.4, -0.45),
            scale=(0.12, 0.12),
            on_click=on_click_callback
        )

    def show_inventory(self):
        if not self.inventory_bg:
            self.inventory_bg = Sprite(
                texture='assets/sprites/premade buttons/inventory.jpg',
                parent=camera.ui,
                position=(0, 0),
                scale=(1.5, 1)
            )

    def hide_inventory(self):
        if self.inventory_bg:
            destroy(self.inventory_bg)
            self.inventory_bg = None

    def show_message(self, text):
        popup = Text(text, origin=(0, 0), scale=2, y=0.2, parent=camera.ui)
        destroy(popup, delay=2)

    def show_reset_button(self, callback):
        Button(text='Reset', scale=(.2, .1), y=-0.1, parent=camera.ui, on_click=callback)

    def show_level_up_choices(self, level, player):
        print(f"Torchy leveled up to {level} — choose a bonus!")

        bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.black66,
            scale=(1.5, 0.6),
            z=-10
        )

        self.level_up_ui = [bg]

        if level == 2:
            options = [
                ("+10 Max HP", lambda: player.increase_max_hp(10)),
                ("Unlock Blaze", lambda: player.unlock_ability("Blaze")),
                ("+2 Fuel", lambda: player.increase_max_fuel(2)),
            ]
        elif level == 5:
            options = [
                ("Unlock Hellfire", lambda: player.unlock_ability("Hellfire")),
                ("+25 Max HP", lambda: player.increase_max_hp(25)),
                ("+3 Fuel", lambda: player.increase_max_fuel(3)),
            ]
        else:
            options = [
                ("+25 HP", lambda: player.heal(25)),
                ("+1 Fuel", lambda: player.restore_fuel(1)),
                ("+1 Max XP Segment", lambda: setattr(player, "max_xp_segments", player.max_xp_segments + 1))
            ]

        message = Text(
            text=f"Level {level} Up! Choose an upgrade:",
            scale=2,
            y=0.3,
            parent=camera.ui
        )
        self.level_up_ui.append(message)

        for i, (label, action) in enumerate(options):
            btn = Button(
                text=label,
                scale=(.28, .1),
                y=0.05 - i * 0.15,
                parent=camera.ui,
                color=color.azure,
                on_click=lambda a=action: self._apply_upgrade(a)
            )
            self.level_up_ui.append(btn)

    def _apply_upgrade(self, action):
        action()
        self.cleanup_levelup_ui()
        print("Level-up choice applied.")

    def cleanup_levelup_ui(self):
        if hasattr(self, 'level_up_ui'):
            for e in self.level_up_ui:
                destroy(e)
            self.level_up_ui.clear()

