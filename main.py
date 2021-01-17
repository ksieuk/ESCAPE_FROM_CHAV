import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))
clock = pygame.time.Clock()
TILE_WIDTH = TILE_HEIGHT = 50

FPS = 50
STEP = 5

# основной персонаж
# player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)

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
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
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
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('simple_road', x, y)
            elif level[y][x] == '-':
                Tile('asphalt_horizontal', x, y)
            elif level[y][x] == 'I':
                Tile('asphalt_vertical', x, y)
            elif level[y][x] == '#':
                Wall('wall', x, y)
            elif level[y][x] == 'O':
                Tile('ped', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '>':
                Tile('asphalt_turn_1', x, y)
            elif level[y][x] == '<':
                Tile('asphalt_turn_2', x, y)
            elif level[y][x] == '?':
                Tile('asphalt_turn_3', x, y)
            elif level[y][x] == ',':
                Tile('asphalt_turn_4', x, y)
            elif level[y][x] == '+':
                Tile('asphalt_junction', x, y)
            elif level[y][x] == 'T':
                Tile('asphalt_triple_1', x, y)
            elif level[y][x] == 'E':
                Tile('asphalt_triple_2', x, y)
            elif level[y][x] == 'Y':
                Tile('asphalt_triple_3', x, y)
            elif level[y][x] == 'L':
                Tile('asphalt_triple_4', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
    'wall': load_image('wall.png'),
    'empty': load_image('center.png'),
    'simple_road': load_image('asphalt_black.png'),
    'asphalt_vertical': load_image('asphalt_vertical.png'),
    'asphalt_horizontal': load_image('asphalt_horizontal.png')
}
player_image = load_image('mario.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type: str, pos_x: int, pos_y: int):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type: str, pos_x: int, pos_y: int):
        super().__init__(walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)

    def update(self, py_events):
        speed_x = speed_y = 0

        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            speed_x = -STEP
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            speed_x = STEP
        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            speed_y = -STEP
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            speed_y = STEP

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
file_name = r"map.txt"
player, level_x, level_y = generate_level(load_level(file_name))

running = True
while running:
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            running = False
            terminate()

    player.update(events)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 255))
    all_sprites.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
