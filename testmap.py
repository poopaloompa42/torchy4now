from ursina import *
app = Ursina()

camera.orthographic = True
camera.fov = 16
camera.position = (0, 0)

# === Load textures ===
walk_textures = [load_texture(f'assets/sprites/player1/walk/twalk00{i}.png') for i in range(8)]
idle_textures = [load_texture(f'assets/sprites/player1/idle/idle00{i}.png') for i in range(10)]

# === ASCII map layout ===
ascii_map = [
    "################################################",
    "#...................#.........................##",
    "#.######..#########.#.#####..######.#######...##",
    "#.#....#..#.......#.#.....#.#....#.#.....#.....#",
    "#.#.##.####.#####.#.#####.#.#.##.#.###.#.#######",
    "#...#........#...#.......#.#..#..#...#.#.......#",
    "####.#########.###########.##.#######.#######.##",
    "#.............#...........#...........#.....#..#",
    "#.###########.#.#########.#.#########.#.###.##.#",
    "#.#.........#.#.......#...#.....#...#.#...#....#",
    "#.#.#######.#.#######.#.#######.#.#.#.###.####.#",
    "#.#.#.....#.#.......#.#.....#...#.#.#...#.#....#",
    "#.#.#.###.#.#######.#.#####.#.###.#.###.#.#.####",
    "#.#.#.#.#.#.......#.......#.#...#.#.#...#.#....#",
    "#.#.#.#.#.#######.#######.#.###.#.#.#.###.####.#",
    "#.#.#.#.#.#.....#.......#.....#.#.#.#.#...#....#",
    "#.#.#.#.#.#.###.#######.#####.#.#.#.#.#.###.####",
    "#.#...#.#.#...#.......#.#...#.#.#.#.#.#.#...#..#",
    "#.#####.#.###.#######.#.#.#.#.#.#.#.#.#.#.###.##",
    "#.......#.....#.......#...#...#...#...#...#.....",
    "################################################"
]

level_map = ascii_map  # use your fancy dungeon map

tile_size = 1
tiles = []

for y, row in enumerate(level_map):
    for x, char in enumerate(row):
        if char == "#":
            block = Entity(
                model='quad',
                color=color.gray,
                scale=tile_size,
                position=(x, -y),
                collider='box'
            )
            tiles.append(block)

# === Player Entity ===
player = Entity(
    model='quad',
    texture=idle_textures[0],
    scale=(1, 1.2),
    position=(2, -5),
    collider='box'
)

# === Animation ===
walk_index = 0
idle_index = 0
anim_timer = 0
walk_speed = 10
idle_speed = 3

# === Movement ===
gravity = 0.2
velocity_y = 0
on_ground = False

def update():
    global walk_index, idle_index, anim_timer, velocity_y, on_ground

    dt = time.dt
    anim_timer += dt

    move_x = held_keys['d'] - held_keys['a']
    player.x += move_x * 5 * dt

    # Flip sprite based on direction
    if move_x > 0:
        player.scale_x = abs(player.scale_x)
    elif move_x < 0:
        player.scale_x = -abs(player.scale_x)

    # Animate
    if move_x != 0:
        if anim_timer >= 1 / walk_speed:
            walk_index = (walk_index + 1) % len(walk_textures)
            player.texture = walk_textures[walk_index]
            anim_timer = 0
    else:
        if anim_timer >= 1 / idle_speed:
            idle_index = (idle_index + 1) % len(idle_textures)
            player.texture = idle_textures[idle_index]
            anim_timer = 0

    # Gravity
    velocity_y -= gravity
    player.y += velocity_y

    on_ground = False
    for tile in tiles:
        if player.intersects(tile).hit:
            if velocity_y < 0:
                player.y = tile.y + 0.6
                velocity_y = 0
                on_ground = True

def input(key):
    global velocity_y
    if key == 'space' and on_ground:
        velocity_y = 0.12  # Jump

Sky()
app.run()
