from ursina import *
import os, sys

app = Ursina()
Text.default_font = 'assets/sprites/font/Augusta.ttf'

# Set background to your title screen art
background = Entity(
    model='quad',
    texture='assets/ui/title.png',  # your new image
    scale=(32, 18),
    z=10
)

# Title text (optional if title.png already has it visually)
title = Text("Torchy Demo", scale=3, y=0.3, origin=(0, 0), color=color.orange)

# Title music (optional)
# title_music = Audio('assets/audio/title_theme.mp3', loop=True, autoplay=True)

# Demo start
import subprocess

def start_demo():
    print("Loading demo...")
    try:
        subprocess.Popen(['python', 'torchy.py'], cwd=os.getcwd())
    except Exception as e:
        print("Failed to start demo:", e)
    application.quit()



# Quit game
def quit_game():
    print("Exiting game.")
    application.quit()

# Buttons
demo_button = Button(
    text="Start Demo",
    scale=(0.3, 0.1),
    y=-0.1,
    color=color.azure,
    on_click=start_demo
)

quit_button = Button(
    text="Quit",
    scale=(0.3, 0.1),
    y=-0.25,
    color=color.red,
    on_click=quit_game
)

camera.orthographic = True
camera.fov = 20
camera.position = (0, 0)

app.run()
