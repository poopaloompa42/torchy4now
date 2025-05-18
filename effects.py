from ursina import *

def show_floating_text(text, position, color=color.white, duration=1):
    label = Text(text, origin=(0,0), position=position, scale=1.5, color=color)
    label.animate_y(label.y + 0.2, duration=duration)
    destroy(label, delay=duration)
