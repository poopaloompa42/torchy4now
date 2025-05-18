from ursina import *

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
