from ursina import *
import random
import time
from math import radians, sin, cos
from zonecontrols import ZONES

turn = 'player'

class CombatController:
    def __init__(self, player, zone_system, ui_manager, xp_callback, spawn_enemy_func):
        self.player = player
        self.zone_system = zone_system
        self.ui_manager = ui_manager
        self.xp_callback = xp_callback
        self.enemy = None
        self.ability_buttons = []
        self.spawn_enemy_func = spawn_enemy_func

    def set_enemy(self, enemy):
        self.enemy = enemy

    def start_enemy_turn(self):
        if not self.enemy or not self.enemy.enabled:
            print("Enemy is not active. Skipping turn.")
            return

        print(f"{self.enemy.name} attacks!")
        self.enemy.enabled = False

        wizard_pos = self.enemy.position

        attack_anim = Animation(
            'sprites/enemies/enemy attack/Wizard attack prototype',
            fps=10,
            loop=False,
            scale=(2, 3),
            position=wizard_pos,
            z=-0.5
        )

        def spawn_projectile(target_y):
            start_pos = Vec3(wizard_pos.x, target_y, -0.6)
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
                if abs(self.player.y - target_y) < 0.3:
                    self.player.take_damage(25, self.ui_manager)
                    print(f"Player hit in zone {ZONES.index(target_y)}")
                    if hasattr(self.enemy, 'status_effect'):
                        print(f"Torchy is affected by {self.enemy.status_effect}!")

                destroy(projectile)

            invoke(hit_player, delay=1.2)

        attack_zones = self.get_attack_zones()
        for i, z in enumerate(attack_zones):
            invoke(lambda z=z: spawn_projectile(z), delay=0.5 + i * 0.3)

        invoke(destroy, attack_anim, delay=1.4)
        invoke(lambda: setattr(self.enemy, "enabled", True), delay=1.5)

    def get_attack_zones(self):
        player_zone = min(ZONES, key=lambda z: abs(z - self.player.y))

        if hasattr(self.enemy, 'attack_style'):
            if self.enemy.attack_style == 'safe_challenge':
                return [z for z in ZONES if z != player_zone][:3]
            elif self.enemy.attack_style == 'target_player':
                other_zones = [z for z in ZONES if z != player_zone]
                return [player_zone] + random.sample(other_zones, 2)

        return random.sample(ZONES, 3)

    def player_attack(self):
        global turn
        if turn != 'player':
            print("It's not your turn!")
            return

        if not self.enemy.enabled:
            print("Enemy is already defeated.")
            return

        print("Torchy attacks!")
        punch_anim = Animation(
            'sprites/player1/punch/attack/Prototype fire ball attack',
            fps=10,
            loop=False,
            position=self.player.position + Vec3(0.5, 0, -0.5),
            scale=(1.2, 1.2)
        )
        punch_anim.animate_position(self.enemy.position + Vec3(-0.5, 0, -0.5), duration=0.6)

        def on_hit():
            destroy(punch_anim)
            camera.shake(duration=0.15, magnitude=1.0)
            self.zone_system.fuel += 1
            self.ui_manager.update_ui(zone_level=self.zone_system.zone_level, fuel=self.zone_system.fuel)

            self.enemy.health_bar.value = max(0, self.enemy.health_bar.value - 25)
            print("Enemy takes 25 damage!")

            if self.enemy.health_bar.value == 0:
                print("Wizard defeated!")
                self.enemy.animate_scale(Vec3(0.1, 0.1, 0.1), duration=0.2)
                destroy(self.enemy)
                destroy(self.enemy.health_bar)
                self.xp_callback(50, self.ui_manager)
                self.spawn_enemy_func()
                turn = 'player'
            else:
                turn = 'enemy'
                invoke(self.start_enemy_turn, delay=1.0)

        invoke(on_hit, delay=0.6)

    def use_blast(self):
        global turn
        if turn != 'player':
            print("It's not your turn!")
            return

        if not self.enemy.enabled:
            print("Enemy is already defeated.")
            return

        if self.player.fuel < 1:
            self.ui_manager.show_message("Not enough fuel to use Blast!")
            return

        print("Torchy uses BLAST!")
        self.player.fuel -= 1
        self.ui_manager.update_fuel()

        blast_anim = Animation(
            'sprites/player1/attacks/blast_animation',
            fps=10,
            loop=False,
            position=self.player.position + Vec3(1, 0, -0.5),
            scale=(2, 2)
        )
        blast_anim.animate_position(self.enemy.position + Vec3(-0.5, 0, -0.5), duration=0.4)

        def on_hit():
            destroy(blast_anim)
            camera.shake(duration=0.2, magnitude=1.2)

            self.enemy.health_bar.value = max(0, self.enemy.health_bar.value - 30)
            print("Enemy takes 30 damage from BLAST!")

            if self.enemy.health_bar.value == 0:
                print("Wizard defeated!")
                self.enemy.animate_scale(Vec3(0.1, 0.1, 0.1), duration=0.2)
                destroy(self.enemy)
                destroy(self.enemy.health_bar)
                self.xp_callback(50, self.ui_manager)
                self.spawn_enemy_func()
                turn = 'player'
            else:
                turn = 'enemy'
                invoke(self.start_enemy_turn, delay=1.0)

        invoke(on_hit, delay=0.4)

    def use_blaze(self):
        global turn
        if turn != 'player':
            print("It's not your turn!")
            return

        if not self.enemy.enabled:
            print("Enemy is already defeated.")
            return

        print("Torchy uses BLAZE!")

        blaze_anim = Animation(
            'sprites/player1/attacks/blaze_animation',
            fps=12,
            loop=False,
            position=self.player.position + Vec3(1, 0, -0.5),
            scale=(2.5, 2.5)
        )
        blaze_anim.animate_position(self.enemy.position + Vec3(-0.5, 0, -0.5), duration=0.5)

        def on_hit():
            destroy(blaze_anim)
            camera.shake(duration=0.25, magnitude=1.5)

            self.enemy.health_bar.value = max(0, self.enemy.health_bar.value - 40)
            print("Enemy takes 40 damage from BLAZE!")

            self.enemy.status_effect = 'burn'
            self.enemy.burn_ticks = 3
            print("Enemy is now BURNING!")

            if self.enemy.health_bar.value == 0:
                print("Wizard defeated!")
                self.enemy.animate_scale(Vec3(0.1, 0.1, 0.1), duration=0.2)
                destroy(self.enemy)
                destroy(self.enemy.health_bar)
                self.xp_callback(50, self.ui_manager)
                self.spawn_enemy_func()
                turn = 'player'
            else:
                turn = 'enemy'
                invoke(self.start_enemy_turn, delay=1.0)

        invoke(on_hit, delay=0.5)

    def update(self):
        if self.enemy and hasattr(self.enemy, 'burn_ticks') and self.enemy.burn_ticks > 0:
            if not hasattr(self.enemy, 'last_burn_time'):
                self.enemy.last_burn_time = time.time()

            if time.time() - self.enemy.last_burn_time >= 1.0:
                self.enemy.burn_ticks -= 1
                self.enemy.health_bar.value = max(0, self.enemy.health_bar.value - 5)
                print("🔥 Burn deals 5 damage!")

                self.enemy.last_burn_time = time.time()

                if self.enemy.health_bar.value <= 0:
                    print("Enemy burned to ash!")
                    destroy(self.enemy)
                    destroy(self.enemy.health_bar)
                    self.xp_callback(50, self.ui_manager)
                    self.spawn_enemy_func()
                    global turn
                    turn = 'player'

    def show_ability_radial(self):
        for btn in self.ability_buttons:
            destroy(btn)
        self.ability_buttons.clear()

        labels = self.player.abilities
        actions_map = {
            'Blast': self.use_blast,
            'Blaze': self.use_blaze,
            'Hellfire': lambda: print("Torchy uses HELLFIRE!")  # placeholder
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
            self.ability_buttons.append(btn)


