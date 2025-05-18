from ursina import *
from ursina.prefabs.health_bar import HealthBar

class WizardEnemy(Animation):
    def __init__(self, **kwargs):
        super().__init__(
            'sprites/enemies/idle/idle glow/Wizard staff glow',
            fps=6,
            loop=True,
            scale=(4, 6),
            z=-1,
            **kwargs
        )
        self.name = 'Wizard'
        self.hp = 150

        self.health_bar = HealthBar(
            parent=camera.ui,
            position=Vec2(0.7, 0.45),
            scale=(0.6, 0.05),
            max_value=self.hp,
            bar_color=color.red
        )
        self.health_bar.value = self.hp
