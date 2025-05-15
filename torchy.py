
from ursina import *
from math import sin, cos, radians

app = Ursina()

# === ENVIRONMENT SETUP ===
ground = Entity(model='plane', scale=100, texture='grass', collider='box')

# === TORCHY MODEL ===
torchy = Entity(
    model='torchy1.glb',
    scale=1,
    y=1,
    collider='box'
)

# === MOVEMENT CONFIG ===
speed = 7
dash_force = 15
velocity = Vec3(0, 0, 0)

# === COMBAT ZONE STATE ===
current_zone = 1  # 0 = high, 1 = mid, 2 = low

# === CAMERA CONFIG ===
camera_distance = 20
camera_angle = Vec2(30, 0)

# === GAME LOOP ===
def update():
    global velocity, camera_distance

    # Movement
    direction = Vec3(
        held_keys['a'] - held_keys['d'],
        0,
        held_keys['s'] - held_keys['w']
    ).normalized()

    if direction != Vec3(0, 0, 0):
        velocity += direction * speed * time.dt

    if held_keys['space']:
        velocity += direction * dash_force * time.dt

    torchy.position += velocity * time.dt
    velocity *= 0.98

    # Camera zoom
    if held_keys['scroll up']:
        camera_distance -= 1
    if held_keys['scroll down']:
        camera_distance += 1
    camera_distance = clamp(camera_distance, 5, 40)

    # Camera positioning
    camera_x = torchy.x + camera_distance * sin(radians(camera_angle.y)) * cos(radians(camera_angle.x))
    camera_y = torchy.y + camera_distance * sin(radians(camera_angle.x))
    camera_z = torchy.z + camera_distance * cos(radians(camera_angle.y)) * cos(radians(camera_angle.x))
    camera.position = (camera_x, camera_y, camera_z)
    camera.look_at(torchy)

# === INPUT HANDLER (CAMERA + COMBAT) ===
def input(key):
    global current_zone

    # Camera rotation
    if held_keys['right mouse']:
        camera_angle.y += mouse.velocity[0] * 100
        camera_angle.x -= mouse.velocity[1] * 100
        camera_angle.x = clamp(camera_angle.x, 10, 80)

    # Combat controls (basic placeholder logic)
    if key == 'up arrow':
        current_zone = max(0, current_zone - 1)
        print(f"Switched to zone: {current_zone} (HIGH=0, MID=1, LOW=2)")
    elif key == 'down arrow':
        current_zone = min(2, current_zone + 1)
        print(f"Switched to zone: {current_zone} (HIGH=0, MID=1, LOW=2)")
    elif key == 'space':
        print("Resolve turn (placeholder function)")
        # resolve_turn()  # Add your function here
    elif key == 'w':
        print("Torchy plays walk animation (placeholder)")
        # torchy.play_anim('walk')  # Uncomment if you have an animation

app.run()
