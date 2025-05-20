from ursina import *
from ursina.prefabs.health_bar import HealthBar
from math import radians, sin, cos
import random, os, sys

app = Ursina()
Text.default_font = 'assets/sprites/font/Augusta.ttf'
turn = 'player'

from zonecontrols import ZoneControls, ZONES
from inventory import InventorySystem
from wizard_enemy import WizardEnemy
from uimanager import UIManager
from radialmenu import RadialMenu
from pausemenu import PauseMenu
from combat import CombatController
from player import Player  # ✅ Replaces old inline Player class

# TEMP player to calc zone height
temp_player = Player()
zone_system = ZoneControls(temp_player)

# Real player at correct height
player = Player(position=(-7.5, zone_system.get_zone_y() - 6, 0))
zone_system.set_player(player)
destroy(temp_player)

# UI Setup
ui_manager = UIManager(player)
ui_manager.update_hp()
ui_manager.update_fuel()
ui_manager.update_xp()
ui_manager.create_downzone_button(on_click_callback=zone_system.move_down_zone)

inventory_system = InventorySystem(player, zone_system, ui_manager)

# Background and music
background = Entity(
    model='quad',
    texture='assets/world/2ddungeon.png',
    scale=(32, 18),
    z=10
)
battle_music = Audio('assets/audio/torchybeats.mp3', loop=True, autoplay=True)
battle_music.volume = 1.0

# Enemy and Combat System
enemy = WizardEnemy(position=(7.5, ZONES[1] - 5.3, -0.2))
combat = CombatController(player, zone_system, ui_manager, player.add_xp, lambda: spawn_new_wizard())
combat.set_enemy(enemy)

# Camera setup
camera.orthographic = True
camera.fov = 20
camera.position = (0, 0)
DirectionalLight(y=2, rotation=(45, -45, 0))

# Radial menu
radial_options = [
    ('Attack', lambda: combat.player_attack()),
    ('Abilities', lambda: combat.show_ability_radial()),
    ('Zone', lambda: zone_system.zone_action()),
    ('Inventory', lambda: inventory_system.open_inventory())
]
radial_menu = RadialMenu(radial_options)

from wizard_enemy import StormWizard, IceWizard, PoisonWizard

def spawn_new_wizard():
    global enemy, turn
    scale_factor = 1 + (player.level * 0.2)

    EnemyType = random.choice([StormWizard, IceWizard, PoisonWizard])
    enemy = EnemyType(position=(4.5, ZONES[zone_system.zone_level] - 0.5, -1.5))
    enemy.scale *= scale_factor
    combat.set_enemy(enemy)
    print(f"A {enemy.name} appears!")
    turn = 'player'


def input(key):
    radial_menu.handle_input(key)

def update():
    radial_menu.update_colors()
    combat.update()
pause_menu = PauseMenu()
app.run()

