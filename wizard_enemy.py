from ursina import *
from ursina.prefabs.health_bar import HealthBar

class WizardEnemy(Animation):
    def __init__(self, **kwargs):
        super().__init__(
            'sprites/enemies/idle/idle glow/Wizard staff glow',
            fps=6,
            loop=True,
            scale=(2, 3),
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


class StormWizard(WizardEnemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Storm Wizard'
        self.color = color.rgb(255, 255, 100)  # ⚡ pale yellow
        self.attack_style = 'target_player'
        self.status_effect = 'shock'


class IceWizard(WizardEnemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Ice Wizard'
        self.color = color.rgb(100, 200, 255)
        self.attack_style = 'safe_challenge'
        self.status_effect = 'freeze'


class PoisonWizard(WizardEnemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Poison Wizard'
        self.color = color.lime
        self.attack_style = 'random'
        self.status_effect = 'poison'
