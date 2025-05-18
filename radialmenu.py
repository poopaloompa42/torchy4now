from math import radians, sin, cos
from ursina import *

class RadialMenu(Entity):
    def __init__(self, options, center=Vec2(0.7, -0.4), radius=0.1, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        self.options = options
        self.center = center
        self.radius = radius
        self.selected_index = None
        self.normal_color = color.dark_gray
        self.highlight_color = color.azure
        self.hover_color = color.orange
        self.create_buttons()

    def create_buttons(self):
        self.buttons.clear()
        for i, (label, action) in enumerate(self.options):
            angle = radians(90 * i)
            pos = Vec2(cos(angle), sin(angle)) * self.radius + self.center
            btn = Button(
                text=label,
                scale=(.1, .1),
                position=pos,
                parent=camera.ui,
                color=self.normal_color,
                on_click=action
            )
            self.buttons.append(btn)

    def update_colors(self):
        for i, btn in enumerate(self.buttons):
            if btn.hovered:
                self.selected_index = i
                btn.color = self.hover_color
            else:
                btn.color = self.highlight_color if i == self.selected_index else self.normal_color

    def handle_input(self, key):
        if key in ('w', 'arrow up'):
            self.selected_index = 0
        elif key in ('d', 'arrow right'):
            self.selected_index = 1
        elif key in ('s', 'arrow down'):
            self.selected_index = 2
        elif key in ('a', 'arrow left'):
            self.selected_index = 3
        elif key == 'space':
            if self.selected_index is not None:
                self.buttons[self.selected_index].on_click()
            else:
                print("Spacebar with no selection")
