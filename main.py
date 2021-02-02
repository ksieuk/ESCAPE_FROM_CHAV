import os
import sys
import pygame
import random
import math
from threading import Timer

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))
clock = pygame.time.Clock()
TILE_WIDTH = TILE_HEIGHT = 50
VOLUME = 0.1
background_music = ['colonel_bg.mp3', 'blood_bg.mp3', 'dont_bg.mp3', 'osen_bg.mp3', 'zarya_bg.mp3']


def load_music(name, type=None):
    fullname = os.path.join(r"data/music", name)

    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        sys.exit()

    sound = None

    try:
        if type == 'song':
            pygame.mixer.music.load(fullname)
            pygame.mixer.music.set_volume(VOLUME)

        elif type == 'sound':
            sound = pygame.mixer.Sound(fullname)
        else:
            print('Unexpected type')
            return
    except pygame.error as message:
        print("Cannot load sound ", name)
        raise SystemExit(message)

    return sound


FPS = 50
PLAYER_STEP = 8
ENEMY_STEP = 5

# основной персонаж
# player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join(r'data/textures/', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image ", name)
        raise SystemExit(message)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    show = True
    menu_background = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

    # escape_btn = Button(512, 160)

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        screen.blit(menu_background, (0, 0))
        # escape_btn.draw(300, 200, 'escape', None)
        pygame.display.flip()
        clock.tick(FPS)


def load_level(name):
    filename = os.path.join(r'data/levels/', name)
    if not os.path.isfile(filename):
        print(f"Файл с уровнем '{filename}' не найден")
        sys.exit()
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    new_enemies = []

    for y in range(len(level)):
        for x in range(len(level[y])):
            tile_name = map_symbols[level[y][x]]
            if tile_name == 'spawn':
                Tile(tile_name, x, y)
                new_player = Player(x, y)
            elif tile_name == 'enemy':
                new_enemies.append(Enemy(x, y))
            elif tile_name.startswith('roof'):
                Wall(tile_name, x, y)
            else:
                Tile(tile_name, x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, new_enemies, x, y


# словарь для карты
map_symbols = {
    '@': 'spawn',
    '$': 'enemy',
    '.': 'simple_road',
    '-': 'asphalt_horizontal',
    'I': 'asphalt_vertical',
    '#': 'roof',
    '1': 'roof_tilt_45',
    '2': 'roof_tilt_45_revert',
    '3': 'roof_building_vertical',
    '4': 'roof_c4',
    'b': 'roof_bottle',
    'O': 'ped',
    '>': 'asphalt_turn_1',
    '<': 'asphalt_turn_2',
    '?': 'asphalt_turn_3',
    ',': 'asphalt_turn_4',
    '+': 'asphalt_junction',
    'T': 'asphalt_triple_1',
    'E': 'asphalt_triple_2',
    'Y': 'asphalt_triple_3',
    'L': 'asphalt_triple_4',
    'G': 'grass',
    'A': 'roof_1',
    'S': 'roof_2',
    'D': 'roof_3',
    'F': 'roof_4',
    'o': 'asphalt_luke',
}

tile_images = {
    'asphalt_triple_1': load_image('asphalt_triple_1.png'),
    'asphalt_turn_1': load_image('asphalt_turn_1.png'),
    'asphalt_turn_2': load_image('asphalt_turn_2.png'),
    'asphalt_turn_3': load_image('asphalt_turn_3.png'),
    'asphalt_turn_4': load_image('asphalt_turn_4.png'),
    'asphalt_triple_2': load_image('asphalt_triple_2.png'),
    'asphalt_triple_3': load_image('asphalt_triple_3.png'),
    'asphalt_triple_4': load_image('asphalt_triple_4.png'),
    'asphalt_junction': load_image('asphalt_junction.png'),
    'ped': load_image('ped_road.png'),
    'roof': load_image('roof.png'),  # TEST
    'roof_tilt_45': load_image('roof_front.png'),
    'roof_tilt_45_revert': load_image('roof_back.png'),
    'roof_building_vertical': load_image('roof_building.png'),
    'roof_c4': load_image('roof_corner_4.png'),
    'spawn': load_image('center.png'),
    'simple_road': load_image('asphalt_black.png'),
    'asphalt_vertical': load_image('asphalt_vertical.png'),
    'asphalt_horizontal': load_image('asphalt_horizontal.png'),
    'grass': load_image('grass.png'),
    'roof_bottle': load_image('roof_bottle.png'),
    'roof_1': load_image('roof_1.png'),
    'roof_2': load_image('roof_2.png'),
    'roof_3': load_image('roof_3.png'),
    'roof_4': load_image('roof_4.png'),
    'asphalt_luke': load_image('asphalt_luke.png')
}
player_image = load_image('main.png')
enemy_image = load_image('musor.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type: str, pos_x: int, pos_y: int):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.name = tile_type


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type: str, pos_x: int, pos_y: int):
        super().__init__(walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image_left = player_image
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)

    def update(self):
        speed_x = speed_y = 0

        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            speed_x = -PLAYER_STEP
            self.image = self.image_left
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            speed_x = PLAYER_STEP
            self.image = self.image_right
        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            speed_y = -PLAYER_STEP
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            speed_y = PLAYER_STEP

        self.rect.x += speed_x

        walls_list = pygame.sprite.spritecollide(self, walls_group, False)
        for block in walls_list:
            if speed_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += speed_y

        walls_list = pygame.sprite.spritecollide(self, walls_group, False)
        for block in walls_list:
            if speed_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image_left = enemy_image
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5 - 50)
        self.state = "peaceful"
        self.direction = "left"
        self.directions = {"up": "down",
                           "down": "up",
                           "left": "right",
                           "right": "left"}
        self.tile_previous = None
        self.possible_directions = list(self.directions.values())
        self.possible_directions.remove(self.direction)
        self.freeze_time = 3.0

    def update(self) -> None:
        if self.state == "peaceful":
            self.peaceful_walking()
        elif self.state == "go_to_road":
            self.go_to_road()
        elif self.state == "dashing":
            self.dashing()
        elif self.state == "murderous":
            self.murderous_run()
        elif self.state == "freezing":
            return

        distance = self.check_distance()[0]
        if distance < 10:
            if self.state != "freezing":
                self.state = "freezing"
                freezing = Timer(self.freeze_time, self.stop_freezing)
                freezing.start()
        elif distance < 100:
            if self.state != "murderous":
                self.state = "murderous"
        elif distance < 200:
            if self.state != "dashing":
                self.state = "dashing"
        elif self.state != "peaceful":
            self.state = "go_to_road"

    def check_distance(self):
        enemy_x, enemy_y = self.rect.x, self.rect.y
        player_x, player_y = player.rect.x, player.rect.y
        delta_x, delta_y = enemy_x - player_x, enemy_y - player_y
        return int(math.hypot(delta_x, delta_y)), delta_x, delta_y

    def peaceful_walking(self):
        speed_x = speed_y = 0
        if self.direction == "right":
            speed_x += ENEMY_STEP
            self.image = self.image_right
        if self.direction == "left":
            speed_x -= ENEMY_STEP
            self.image = self.image_left
        if self.direction == "down":
            speed_y += ENEMY_STEP
        if self.direction == "up":
            speed_y -= ENEMY_STEP

        walls = pygame.sprite.spritecollide(self, walls_group, False, collided=pygame.sprite.collide_rect_ratio(1))
        free_tiles = pygame.sprite.spritecollide(self, tiles_group, False)
        if walls:
            speed_x = -speed_x
            speed_y = -speed_y
            self.possible_directions = list(self.directions.values())
            self.possible_directions.remove(self.direction)
            self.direction = self.directions[self.direction]

        tile_name = free_tiles[0].name
        if self.tile_previous != tile_name:
            self.change_direction(tile_name)

        self.rect.x += speed_x
        self.rect.y += speed_y
        self.tile_previous = tile_name

    def go_to_road(self):
        free_tiles = pygame.sprite.spritecollide(self, tiles_group, False)
        tile_name = free_tiles[0].name
        if tile_name.startswith("asphalt") and tile_name != "asphalt_black":
            self.state = "peaceful"
            if tile_name == "asphalt_horizontal":
                self.direction = random.choice(("right", "left"))
            elif tile_name == "asphalt_vertical":
                self.direction = random.choice(("up", "down"))
            else:
                self.change_direction(tile_name)
        self.peaceful_walking()

    def dashing(self):
        distance, delta_x, delta_y = self.check_distance()

        delta_x /= distance
        delta_y /= distance

        speed_x = -delta_x * ENEMY_STEP
        speed_y = -delta_y * ENEMY_STEP

        self.rect.x += speed_x
        self.rect.y += speed_y

        walls_list = pygame.sprite.spritecollide(self, walls_group, False)
        for block in walls_list:
            if speed_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        walls_list = pygame.sprite.spritecollide(self, walls_group, False)
        for block in walls_list:
            if speed_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def murderous_run(self):
        distance, delta_x, delta_y = self.check_distance()
        if distance == 0:
            self.state = "freezing"
            return

        delta_x /= distance
        delta_y /= distance

        speed_x = -delta_x * ENEMY_STEP * 3
        speed_y = -delta_y * ENEMY_STEP * 3

        self.rect.x += speed_x
        self.rect.y += speed_y

        walls_list = pygame.sprite.spritecollide(self, walls_group, False)
        for block in walls_list:
            if speed_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        walls_list = pygame.sprite.spritecollide(self, walls_group, False)
        for block in walls_list:
            if speed_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def stop_freezing(self):
        self.state = "go_to_road"

    def change_direction(self, tile_name):

        if 'asphalt_junction' == tile_name:
            self.direction = random.choice(self.possible_directions)

        elif 'asphalt_triple_1' == tile_name:
            possible_directions = self.possible_directions[:]
            if "up" in possible_directions:
                possible_directions.remove("up")
            self.direction = random.choice(possible_directions)

        elif 'asphalt_triple_2' == tile_name:
            possible_directions = self.possible_directions[:]
            if "right" in possible_directions:
                possible_directions.remove("right")
            self.direction = random.choice(possible_directions)

        elif 'asphalt_triple_3' == tile_name:
            possible_directions = self.possible_directions[:]
            if "down" in possible_directions:
                possible_directions.remove("down")
            self.direction = random.choice(possible_directions)

        elif 'asphalt_triple_4' == tile_name:
            possible_directions = self.possible_directions[:]
            if "left" in possible_directions:
                possible_directions.remove("left")
            self.direction = random.choice(possible_directions)

        elif 'asphalt_turn_1' == tile_name:
            possible_directions = ["down", "right"]
            block_direction = self.directions[self.direction]
            if block_direction in possible_directions:
                possible_directions.remove(block_direction)
            self.direction = random.choice(possible_directions)

        elif 'asphalt_turn_2' == tile_name:
            possible_directions = ["down", "left"]
            block_direction = self.directions[self.direction]
            if block_direction in possible_directions:
                possible_directions.remove(block_direction)
            self.direction = random.choice(possible_directions)

        elif 'asphalt_turn_3' == tile_name:
            possible_directions = ["up", "left"]
            block_direction = self.directions[self.direction]
            if block_direction in possible_directions:
                possible_directions.remove(block_direction)
            self.direction = random.choice(possible_directions)

        elif 'asphalt_turn_4' == tile_name:
            possible_directions = ["up", "right"]
            block_direction = self.directions[self.direction]
            if block_direction in possible_directions:
                possible_directions.remove(block_direction)
            self.direction = random.choice(possible_directions)

        self.possible_directions = list(self.directions.values())
        self.possible_directions.remove(self.directions[self.direction])


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


camera = Camera()
start_screen()

# playing background music
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
load_music(random.choice(background_music), 'song')
pygame.mixer.music.play(0)
file_name = r"map.txt"

player, enemies, level_x, level_y = generate_level(load_level(file_name))

running = True
while running:
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == SONG_END:
            load_music(random.choice(background_music), 'song')
            pygame.mixer.music.play(0)

    player.update()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    for enemy in enemies:
        enemy.update()

    screen.fill(pygame.Color(0, 0, 255))
    all_sprites.draw(screen)
    player_group.draw(screen)
    enemies_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
