from ursina import *
import numpy as np
from PIL import Image

app = Ursina()

# === Load Terrain from Grayscale ===
img = Image.open('assets/world/grayscale.png').convert('L')
height_data = np.asarray(img) / 255.0
size_x, size_y = height_data.shape
scale_factor = 5.0

mesh = Mesh(vertices=[], uvs=[], triangles=[], mode='triangle')

for y in range(size_y - 1):
    for x in range(size_x - 1):
        z1 = height_data[x][y] * scale_factor
        z2 = height_data[x + 1][y] * scale_factor
        z3 = height_data[x][y + 1] * scale_factor
        z4 = height_data[x + 1][y + 1] * scale_factor

        p1 = Vec3(x, z1, y)
        p2 = Vec3(x + 1, z2, y)
        p3 = Vec3(x, z3, y + 1)
        p4 = Vec3(x + 1, z4, y + 1)

        i = len(mesh.vertices)
        mesh.vertices += [p1, p2, p3, p2, p4, p3]
        mesh.uvs += [(0, 0), (1, 0), (0, 1), (1, 0), (1, 1), (0, 1)]
        mesh.triangles += [i, i + 1, i + 2, i + 3, i + 4, i + 5]

mesh.generate()
terrain = Entity(model=mesh, texture='assets/world/grayscale.png', collider='mesh', scale=(2, 1, 2))

# === Zones ===
zones = [3, 1, -1]  # y positions: high, mid, low
zone_index = 1

# === Load Textures ===
punch_textures = [load_texture(f'assets/sprites/player1/punch/punch_{i:03}.png') for i in range(8)]
idle_textures = [load_texture(f'assets/sprites/player1/idle/idle00{i}.png') for i in range(10)]
enemy_idle_textures = [load_texture(f'assets/sprites/enemies/idle/idle00{i}.png') for i in range(10)]
print("Enemy Idle Textures Loaded:", [bool(t) for t in enemy_idle_textures])

# === Entities ===
torchy = Entity(
    model='quad',
    texture=idle_textures[0],
    scale_y=2,
    position=(-10, zones[zone_index], 10),
    collider='box'
)

enemy = Entity(
    model='quad',
    texture=enemy_idle_textures[0], # Will idle here too unless you add idle anim
    scale=(2, 3),
    position=(10, 1, 10),
    collider='box',
    rotation_y=180  # Mirrored to face Torchy
)

# === Animation State ===
current_animation = 'idle'
idle_index = 0
punch_index = 0
hurt_index = 0
anim_timer = 0

idle_speed = 3
punch_speed = 12
hurt_speed = 8

is_attacking = False
enemy_reacting = False



def update():
    global idle_index, punch_index, anim_timer, is_attacking
    global hurt_index, enemy_reacting, current_animation

    anim_timer += time.dt

    if is_attacking and current_animation == 'punch':
        if anim_timer >= 1 / punch_speed:
            punch_index += 1
            if punch_index >= len(punch_textures):
                is_attacking = False
                current_animation = 'idle'
                idle_index = 0
                torchy.texture = idle_textures[0]
            else:
                torchy.texture = punch_textures[punch_index]
            anim_timer = 0

    elif not is_attacking:
        if anim_timer >= 1 / idle_speed:
            idle_index = (idle_index + 1) % len(idle_textures)
            torchy.texture = idle_textures[idle_index]
            anim_timer = 0

    if enemy_reacting and anim_timer >= 1 / hurt_speed:
        hurt_index += 1
        if hurt_index >= len(hurt_textures):
            enemy_reacting = False
        else:
            enemy.texture = enemy_idle_textures[enemy_idle_index]
        anim_timer = 0

    # Camera lock
    #camera.position = Vec3(0, 15, -30)
    #camera.look_at(torchy.position)
# === Camera zoom control ===
zoom_speed = 20

def input(key):
    global zone_index, is_attacking, punch_index, anim_timer, current_animation
    global enemy_reacting, hurt_index

    # Zone switching
    if key == 'up arrow':
        zone_index = max(0, zone_index - 1)
        torchy.y = zones[zone_index]
    elif key == 'down arrow':
        zone_index = min(2, zone_index + 1)
        torchy.y = zones[zone_index]

    # Zoom controls
    elif key == 'scroll up':
        camera.position += Vec3(0, 0, zoom_speed * time.dt)
    elif key == 'scroll down':
        camera.position -= Vec3(0, 0, zoom_speed * time.dt)

    # Attack
    elif key == 'space' and not is_attacking:
        is_attacking = True
        punch_index = 0
        current_animation = 'punch'
        torchy.texture = punch_textures[0]
        anim_timer = 0

        enemy_reacting = True
        hurt_index = 0
        enemy.texture = hurt_textures[0]


Sky()
DirectionalLight(y=2, rotation=(45, -45, 0))
app.run()