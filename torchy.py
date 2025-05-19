
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
from levelup import LevelSystem



class Player(Animation):
    def __init__(self, **kwargs):
        super().__init__(
            'sprites/player1/idle/torchy',
            fps=6,
            loop=True,
            scale=(1.5, 2),
            z=-1,
            **kwargs
        )
        self.name = 'Torchy'
        self.hp = 100
        self.max_hp = 100
        self.fuel = 10
        self.max_fuel = 10
        self.abilities = []
        self.xp_segments_full = 0
        self.max_xp_segments = 5

    def get_heart_count(self):
        return self.hp // 25


# Temporary player just to calculate zone height
temp_player = Player()
zone_system = ZoneControls(temp_player)

# Now create the real player at the correct zone height
player = Player(position=(-7.5, zone_system.get_zone_y() - 6, 0))
zone_system.set_player(player)

destroy(temp_player)

# UI Manager using the real player
ui_manager = UIManager(player)
ui_manager.update_hp()
ui_manager.update_fuel()
ui_manager.update_xp()
ui_manager.create_downzone_button(on_click_callback=zone_system.move_down_zone)

# Background and music
background = Entity(
    model='quad',
    texture='assets/world/2ddungeon.png',
    scale=(32, 18),
    z=10
)
battle_music = Audio('assets/audio/torchybeats.mp3', loop=True, autoplay=True)
battle_music.volume = 1.0

# Inventory
inventory_system = InventorySystem(player, zone_system, ui_manager)

enemy = WizardEnemy(position=(7.5, ZONES[1] - 5.3, -0.2))

ui_manager = UIManager(player)


from levelup import LevelSystem
level_system = LevelSystem(player)

camera.orthographic = True
camera.fov = 20
camera.position = (0, 0)
DirectionalLight(y=2, rotation=(45, -45, 0))

ability_buttons = []
 

radial_options = [
    ('Attack', lambda: attack()),
    ('Abilities', lambda: show_ability_radial()),
    ('Zone', lambda: zone_system.zone_action()),  # 
    ('Inventory', lambda: inventory_system.open_inventory())

]

radial_menu = RadialMenu(radial_options)


def set_idle_animation():
    enemy.enabled = True

def enemy_turn():
    global turn
    print("Enemy attacks!")
    enemy.enabled = False

    # Get Y zone for current attack
    zone_y = ZONES[zone_system.zone_level]
    wizard_pos = Vec3(4, zone_y - 0.5, -0.5)  # Adjusted to match visual layout

    # Wizard attack animation
    attack_anim = Animation(
        'sprites/enemies/enemy attack/Wizard attack prototype',
        fps=10,
        loop=False,
        scale=(2, 3),
        position=wizard_pos,
        z=-0.5
    )

    def spawn_projectile(target_y):
        start_pos = Vec3(3.5, target_y, -0.6)
        end_pos = Vec3(-4, target_y, -0.6)

        projectile = Animation(
            'sprites/Generic Stuff/Wizard attack projectile',
            fps=6,
            loop=False,
            position=start_pos,
            scale=(1.5, 1.5),
        )
        projectile.animate_position(end_pos, duration=1.2, curve=curve.linear)

        def hit_player():
            if abs(player.y - target_y) < 0.3:
                player.hp = max(0, player.hp - 25)
                ui_manager.update_hp()
                print("Player hit in zone", ZONES.index(target_y))
                if player.hp == 0:
                    print("Torchy defeated!")
                    destroy(player)
                    show_reset_prompt()
            destroy(projectile)

        invoke(hit_player, delay=1.2)

    # Randomize the 3 zones the enemy attacks
    attack_zones = random.sample(ZONES, 3)
    for i, z in enumerate(attack_zones):
        invoke(lambda z=z: spawn_projectile(z), delay=0.5 + i * 0.3)

    # Cleanup and reset
    invoke(destroy, attack_anim, delay=1.4)
    invoke(set_idle_animation, delay=1.5)
    turn = 'player'

def attack():
    global turn
    if turn != 'player':
        print("It's not your turn!")
        return
    if not enemy.enabled:
        print("Enemy is already defeated.")
        return

    print("Torchy attacks!")

    # === Play punch/fireball animation ===
    punch_anim = Animation(
        'sprites/player1/punch/attack/Prototype fire ball attack',
        fps=10,
        loop=False,
        position=player.position + Vec3(0.5, 0, -0.5),
        scale=(1.2, 1.2)
    )
    punch_anim.animate_position(enemy.position + Vec3(-0.5, 0, -0.5), duration=0.6, curve=curve.linear)

    def on_hit():
        destroy(punch_anim)
        camera.shake(duration=0.15, magnitude=1.0)
        zone_system.fuel += 1
        ui_manager.update_ui(zone_level=zone_system.zone_level, fuel=zone_system.fuel)

        enemy.health_bar.value = max(0, enemy.health_bar.value - 10)
        print("Enemy takes 10 damage!")

        if enemy.health_bar.value == 0:
            print("Wizard defeated!")
            enemy.animate_scale(Vec3(0.1, 0.1, 0.1), duration=0.2, curve=curve.in_expo)
            destroy(enemy)
            destroy(enemy.health_bar)
            level_system.add_xp(50)
            spawn_new_wizard()
        else:
            global turn
            turn = 'enemy'
            invoke(enemy_turn, delay=1.0)

    invoke(on_hit, delay=0.6)  # wait for punch to reach enemy

def show_ability_radial():
    for btn in ability_buttons:
        destroy(btn)
    ability_buttons.clear()

    labels = player.abilities
    actions_map = {
        'Blast': blast,
        'Blaze': blaze,
        'Hellfire': hellfire
    }

    for i, label in enumerate(labels):
        angle = radians(90 * i)
        pos = Vec2(cos(angle), sin(angle)) * 0.1 + Vec2(.7, -.2)
        btn = Button(
            text=label,
            scale=(.08, .08),
            position=pos,
            parent=camera.ui,
            color=color.gray,
            on_click=actions_map.get(label, lambda: print(f"{label} not implemented"))
        )
        ability_buttons.append(btn)


def input(key):
    radial_menu.handle_input(key)

def update():
    radial_menu.update_colors()


def show_reset_prompt():
    ui_manager.show_message("Game Over!")
    ui_manager.show_reset_button(reset_game)


def reset_game():
    application.quit()
    os.execl(sys.executable, sys.executable, *sys.argv)

pause_menu = PauseMenu()
app.run()
