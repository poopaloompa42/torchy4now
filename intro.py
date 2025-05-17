from ursina import *
#from torchy import start_battle

app = Ursina()

# === SPLASH FLOW ===
def show_splash_screens():
    print('Splash screen flow started')

    def show_chatgpt_credit():
        print('Showing ChatGPT splash')
        SplashScreen(texture='assets/sprites/credits/ChatGPTsplash.png', duration=3, on_destroy=show_us_credit)

    def show_us_credit():
        print('Showing dev splash')
        SplashScreen(texture='assets/sprites/credits/us.png', duration=3, on_destroy=show_ursina_credit)

    def show_ursina_credit():
        print('Showing Ursina splash')
        SplashScreen(texture='ursina_logo', duration=3, dev_text='Made with Ursina Engine', on_destroy=show_title_screen)

    show_chatgpt_credit()


# === SPLASH CLASS ===
class SplashScreen(Sprite):
    def __init__(self, texture, duration=3, on_destroy=None, dev_text=None, **kwargs):
        super().__init__(
            parent=camera.ui,
            texture=texture,
            world_z=camera.overlay.z - 1,
            scale=(camera.aspect_ratio * 2, 2),
            color=color.clear,
            **kwargs
        )
        camera.overlay.animate_color(color.black, duration=.1)
        self.animate_color(color.white, duration=1, delay=0.5, curve=curve.out_quint)
        self._on_destroy_callback = on_destroy
        invoke(self.finish, delay=duration)

        # Optional dev text that fades in
        if dev_text:
            self.dev_text = Text(
                text=dev_text,
                parent=camera.ui,
                y=-0.35,
                scale=1.5,
                origin=(0, 0),
                color=color.clear
            )
            invoke(self.dev_text.animate_color, color.red, delay=1.8, duration=1.2, curve=curve.linear)

    def input(self, key):
        if key in ('space', 'gamepad a', 'escape', 'left mouse down'):
            self.finish()

    def finish(self):
        destroy(self)

    def on_destroy(self):
        camera.overlay.animate_color(color.clear, duration=.25)
        if self._on_destroy_callback:
            self._on_destroy_callback()


# === TITLE SCREEN ===
def show_title_screen():
    print('Showing title screen')

    for e in scene.entities:
        destroy(e)

    # Fix camera for 2D view
    camera.orthographic = True
    camera.fov = 20
    camera.position = (0, 0)

    Entity(model='quad', texture='assets/world/2ddungeon.png', scale=(32, 18), z=10)

    Text("TORCHY", y=0.3, scale=3, origin=(0,0), color=color.white)
    Button(text="Demo", scale=(.2, .1), y=-.2, on_click=start_battle)



# === RUN GAME ===
show_splash_screens()
app.run()

