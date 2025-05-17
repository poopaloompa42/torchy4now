from ursina import *
from ursina.prefabs.health_bar import HealthBar
from math import radians, sin, cos

# === PauseMenu CLASS DEFINITION ===
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
                mouse.locked = self.lock_mouse_on_resume

            application.paused = not application.paused
            self.menu.enabled = application.paused

# === Game Setup ===
app = Ursina()

# === Background ===
background = Entity(
    model='quad',
    texture='assets/world/2ddungeon.png',
    scale=(32, 18),
    z=10
)

# === Player ===
player = Entity(
    model='quad',
    texture='assets/sprites/player1/babytorchy.png',
    scale=(1.5, 2),
    position=(-4, -2, 0),
    z=-1
)
player.health_bg = Entity(parent=player, model='quad', color=color.rgb(100, 0, 0), scale=(1.5, 0.1), y=1.2, z=-0.01)
player.health_bar = HealthBar(parent=player, y=1.2, scale=(1.5, 0.1), max_value=100, bar_color=color.lime)

# === Enemy ===
enemy = Entity(
    model='quad',
    texture='assets/sprites/enemies/idle/Wizard2.png',
    scale=(4, 6),
    position=(4, -1, 0),
    z=-1
)
enemy.health_bar = HealthBar(parent=enemy, y=3.5, scale=(2.5, 0.15), max_value=150, bar_color=color.red)
enemy.health_bar.value = 150

# === Camera / Light ===
camera.orthographic = True
camera.fov = 20
camera.position = (0, 0)
DirectionalLight(y=2, rotation=(45, -45, 0))

# === Radial Menu ===
radial_options = ['Attack', 'Abilities', 'Zone', 'Inventory']
radial_buttons = []
selected_index = None
highlight_color = color.azure
normal_color = color.dark_gray
hover_color = color.orange

for i, option in enumerate(radial_options):
    angle = radians(90 * i)
    pos = Vec2(cos(angle), sin(angle)) * 0.1 + Vec2(.7, -.4)
    btn = Button(
        text=option,
        scale=(.1, .1),
        position=pos,
        parent=camera.ui,
        color=normal_color,
        on_click=lambda o=option: print(f"Selected: {o}")
    )
    radial_buttons.append(btn)

# === Input Logic ===
def input(key):
    global selected_index

    directions = ['up', 'right', 'down', 'left']
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

# === Update Highlighting ===
def update():
    global selected_index
    for i, btn in enumerate(radial_buttons):
        if btn.hovered:
            selected_index = i
            btn.color = hover_color
        else:
            btn.color = highlight_color if i == selected_index else normal_color

# === Add PauseMenu ===
pause_menu = PauseMenu()

# === Run Game ===
app.run()
