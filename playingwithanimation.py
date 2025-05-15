from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# === Load Heightmap ===
terrain_entity = Entity(
    model='plane',
    texture='assets/world/grayscale.png',
    collider='mesh',
    scale=(100, 1, 100),
    y=0
)

# === Deform Based on Grayscale ===
from PIL import Image
import numpy as np

img = Image.open('assets/world/grayscale.png').convert('L')
height_data = np.asarray(img) / 255  # normalize to 0-1

mesh = Mesh(vertices=[], uvs=[], triangles=[], mode='triangle')
size_x, size_y = height_data.shape
scale_factor = 0.5  # bumpiness

for y in range(size_y-1):
    for x in range(size_x-1):
        z1 = height_data[x][y] * scale_factor
        z2 = height_data[x+1][y] * scale_factor
        z3 = height_data[x][y+1] * scale_factor
        z4 = height_data[x+1][y+1] * scale_factor

        # 4 corners of the square
        p1 = Vec3(x, z1, y)
        p2 = Vec3(x+1, z2, y)
        p3 = Vec3(x, z3, y+1)
        p4 = Vec3(x+1, z4, y+1)

        i = len(mesh.vertices)

        mesh.vertices += [p1, p2, p3, p2, p4, p3]
        mesh.uvs += [(0,0), (1,0), (0,1), (1,0), (1,1), (0,1)]
        mesh.triangles += [i, i+1, i+2, i+3, i+4, i+5]

mesh.generate()

terrain_entity.model = mesh
terrain_entity.texture = 'assets/world/grayscale.png'

# === Character ===
# === Load walk & idle frames ===
walk_textures = [load_texture(f'assets/sprites/player1/walk/twalk00{i}.png') for i in range(8)]
idle_textures = [load_texture(f'assets/sprites/player1/idle/idle00{i}.png') for i in range(10)]

# === Create player entity ===
player = Entity(
    model='quad',
    texture=idle_textures[0],
    scale_y=2,
    position=(10, 2, 10),
    collider='box'
)

# === Animation state ===
current_animation = 'idle'
walk_index = 0
idle_index = 0
anim_timer = 0
walk_speed = 6  # frames/sec
idle_speed = 3

def update():
    global walk_index, idle_index, anim_timer, current_animation

    speed = 5
    direction = Vec3(
        held_keys['d'] - held_keys['a'],
        0,
        held_keys['w'] - held_keys['s']
    ).normalized()

    moving = direction != Vec3(0, 0, 0)

    if moving:
        player.position += direction * time.dt * speed
        player.look_at(player.position + direction)
        if current_animation != 'walk':
            current_animation = 'walk'
            walk_index = 0
            player.texture = walk_textures[walk_index]
            anim_timer = 0
    else:
        if current_animation != 'idle':
            current_animation = 'idle'
            idle_index = 0
            player.texture = idle_textures[idle_index]
            anim_timer = 0

    # Animate
    anim_timer += time.dt
    if current_animation == 'walk' and anim_timer >= 1 / walk_speed:
        walk_index = (walk_index + 1) % len(walk_textures)
        player.texture = walk_textures[walk_index]
        anim_timer = 0
    elif current_animation == 'idle' and anim_timer >= 1 / idle_speed:
        idle_index = (idle_index + 1) % len(idle_textures)
        player.texture = idle_textures[idle_index]
        anim_timer = 0

    # Camera follow
    camera.position = player.position + Vec3(0, 5, -10)
    camera.look_at(player.position)



Sky()

app.run()