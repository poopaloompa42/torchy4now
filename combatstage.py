from ursina import *
import random
from os import listdir

app = Ursina()
window.color = color.black
camera.orthographic = True
camera.fov = 10

# === Load animations ===
def load_animation_folder(path):
    frames = sorted([f for f in listdir(path) if f.endswith('.png')])
    return [load_texture(f'{path}/{f}') for f in frames]

player1_anims = {
    'walk': load_animation_folder('assets/sprites/player1/walk'),
    'idle': load_animation_folder('assets/sprites/player1/idle'),
    'jump': load_animation_folder('assets/sprites/player1/jump'),
    'hurt': load_animation_folder('assets/sprites/player1/hurt'),
    'punch': load_animation_folder('assets/sprites/player1/punch'),
}

# === Animated Sprite Class ===
class AnimatedSprite(Entity):
    def __init__(self, animations: dict[str, list], **kwargs):
        super().__init__(model='quad', texture=animations['idle'][0], **kwargs)
        self.animations = animations
        self.current_anim = 'idle'
        self.current_frame = 0
        self.frame_delay = 0.1
        self.timer = 0
        self.playing = True

    def play_anim(self, name):
        if name != self.current_anim:
            self.current_anim = name
            self.current_frame = 0
            self.texture = self.animations[name][0]
            self.timer = 0
            self.playing = True

    def update(self):
        if not self.playing: return
        self.timer += time.dt
        if self.timer >= self.frame_delay:
            self.timer = 0
            frames = self.animations[self.current_anim]
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.texture = frames[self.current_anim][self.current_frame]

# === Create Entities ===
player = AnimatedSprite(player1_anims, scale=(1.5, 2), position=(-3, 0, 0), color=color.white)
enemy = Entity(model='quad', color=color.red, scale=(1, 2), position=(3, 0, 0))

attack_zones = ['high', 'mid', 'low']
current_zone = 1  # starts at mid

# === UI Text ===
action_text = Text('', y=0.45, origin=(0,0), scale=2)

# === Input Handler ===
def input(key):
    global current_zone

    if key == 'up arrow':
        current_zone = max(0, current_zone - 1)
    elif key == 'down arrow':
        current_zone = min(2, current_zone + 1)
    elif key == 'space':
        resolve_turn()
    elif key == 'w':
        player.play_anim('walk')

app.run()

