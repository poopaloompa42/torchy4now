from ursina import *
from ursina.prefabs.health_bar import HealthBar
from math import radians, sin, cos

class PauseMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(ignore_paused=True, **kwargs)
        self.menu = Entity(parent=camera.ui, enabled=False)
        self.bg = Entity(parent=self.menu, model='quad', color=color.black, alpha=.5, scale=3)
        self.pause_text = Text(parent=self.menu, text='PAUSED', origin=(0, .3), scale=2)
        self.resume_button = Button(
            text='Resume',
            parent=self.menu,
            y=-.1,
            scale=(.2, .1),
            color=color.azure,
            on_click=self.toggle_pause
        )
        self.quit_button = Button(
            text='Quit',
            parent=self.menu,
            y=-.25,
            scale=(.2, .1),
            color=color.red,
            on_click=application.quit
        )
        self.lock_mouse_on_resume = False

    def on_destroy(self):
        destroy(self.menu)

    def toggle_pause(self):
        mouse.locked = self.lock_mouse_on_resume
        application.paused = False
        self.menu.enabled = False

    def input(self, key):
        if key == 'escape':
            if not application.paused:
                self.lock_mouse_on_resume = mouse.locked
                mouse.locked = False
            else:
                self.lock_mouse_on_resume = mouse.locked

            application.paused = not application.paused
            self.menu.enabled = application.paused

window.borderless = False
window.size = (1280, 720)
window.resizable = True

app = Ursina()

from ursina import Audio
battle_music = Audio('assets/audio/torchybeats.mp3', loop=True, autoplay=True)
battle_music.volume = 1.0

background = Entity(
    model='quad',
    texture='assets/world/2ddungeon.png',
    scale=(32, 18),
    z=10
)

player = Animation(
    'sprites/player1/idle/Prototype fire ball man dude',
    fps=6,
    loop=True,
    scale=(1.5, 2),
    position=(-4, -2, 0),
    z=-1
)
player.health_bar = HealthBar(
    parent=camera.ui,
    position=Vec2(-0.7, 0.45),
    scale=(0.6, 0.05),
    max_value=100,
    bar_color=color.lime
)
player.health_bar.value = 100

enemy = Entity(
    model='quad',
    texture='assets/sprites/enemies/idle/Wizard2.png',
    scale=(4, 6),
    position=(4, -1, 0),
    z=-1
)
enemy.health_bar = HealthBar(
    parent=camera.ui,
    position=Vec2(0.7, 0.45),
    scale=(0.6, 0.05),
    max_value=150,
    bar_color=color.red
)
enemy.health_bar.value = 150

camera.orthographic = True
camera.fov = 20
camera.position = (0, 0)
DirectionalLight(y=2, rotation=(45, -45, 0))

zone_level = 0
fuel = 0

fuel_bar = HealthBar(
    parent=camera.ui,
    position=Vec2(0, 0.38),
    scale=(0.4, 0.03),
    max_value=10,
    bar_color=color.orange
)
fuel_bar.value = fuel

zone_label = Text(text=f"Zone: {zone_level}", position=(-0.05, 0.35), scale=2, parent=camera.ui)
fuel_label = Text(text=f"Fuel: {fuel}", position=(-0.05, 0.3), scale=2, parent=camera.ui)

def attack():
    global fuel
    if not enemy.enabled:
        print("Enemy is already defeated.")
        return

    enemy.health_bar.value = max(0, enemy.health_bar.value - 10)
    print("Enemy takes 10 damage!")
    Audio('assets/audio/hit_sound.mp3')
    camera.shake(duration=0.15, magnitude=1.0)

    fuel += 1
    fuel_label.text = f"Fuel: {fuel}"
    fuel_bar.value = fuel

    if enemy.health_bar.value == 0:
        print("Wizard defeated!")
        enemy.animate_scale(Vec3(0.1, 0.1, 0.1), duration=0.2, curve=curve.in_expo)
        destroy(enemy)
        destroy(enemy.health_bar)
        radial_buttons[0].enabled = False

def zone_action():
    global fuel, zone_level
    if fuel > 0 and zone_level < 2:
        fuel -= 1
        zone_level += 1
        print(f"Zone raised to {zone_level}, fuel remaining: {fuel}")
    else:
        if fuel == 0:
            print("Not enough fuel to raise zone!")
        elif zone_level >= 2:
            print("Already at max zone!")

    fuel_label.text = f"Fuel: {fuel}"
    fuel_bar.value = fuel
    zone_label.text = f"Zone: {zone_level}"
    player.y = -2 + zone_level * 0.5

def placeholder_action(name):
    print(f"{name} action selected (not implemented)")

radial_options = [
    ('Attack', attack),
    ('Abilities', lambda: placeholder_action('Abilities')),
    ('Zone', zone_action),
    ('Inventory', lambda: placeholder_action('Inventory'))
]

radial_buttons = []
selected_index = None
highlight_color = color.azure
normal_color = color.dark_gray
hover_color = color.orange

for i, (label, action) in enumerate(radial_options):
    angle = radians(90 * i)
    pos = Vec2(cos(angle), sin(angle)) * 0.1 + Vec2(.7, -.4)
    btn = Button(
        text=label,
        scale=(.1, .1),
        position=pos,
        parent=camera.ui,
        color=normal_color,
        on_click=action
    )
    radial_buttons.append(btn)

def input(key):
    global selected_index

    if key in ('w', 'arrow up'):
        selected_index = 0
    elif key in ('d', 'arrow right'):
        selected_index = 1
    elif key in ('s', 'arrow down'):
        selected_index = 2
    elif key in ('a', 'arrow left'):
        selected_index = 3
    elif key == 'space':
        if selected_index is not None:
            radial_buttons[selected_index].on_click()
        else:
            print("Spacebar with no selection")

def update():
    global selected_index
    for i, btn in enumerate(radial_buttons):
        if btn.hovered:
            selected_index = i
            btn.color = hover_color
        else:
            btn.color = highlight_color if i == selected_index else normal_color

pause_menu = PauseMenu()
app.run()
