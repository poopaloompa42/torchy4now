from ursina import *
from ursina.prefabs.health_bar import HealthBar

# === PauseMenu definition (same as above) ===
# [Insert the class code from above here]
from ursina import *
from ursina.prefabs.health_bar import HealthBar

# === PauseMenu CLASS DEFINITION GOES HERE ===
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

# === Add PauseMenu ===
pause_menu = PauseMenu()

app.run()
