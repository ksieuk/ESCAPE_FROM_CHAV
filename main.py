import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))
clock = pygame.time.Clock()

FPS = 50
STEP = 5

# основной персонаж
# player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# словарь для карты
map_symbols = {
        '.': 'simple_road',
        '-': 'asphalt_horizontal',
        'I': 'asphalt_vertical',
        '#': 'wall',
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
    }


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image ", name)
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
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
            if level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            else:
                Tile(map_symbols[level[y][x]], x, y)

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

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x, self.pos_y = tile_width * pos_x, tile_height * pos_y
        self.rect = self.image.get_rect().move(
            self.pos_x + 15, self.pos_y + 5)
        self.is_moving_right = self.is_moving_left = self.is_moving_up = self.is_moving_down = False

    def update(self, py_events):
        speed_x = speed_y = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            speed_x = -STEP
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            speed_x = STEP
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            speed_y = -STEP
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            speed_y = STEP

        if self.is_moving_left:
            speed_x = -STEP
        if self.is_moving_right:
            speed_x = STEP
        if self.is_moving_up:
            speed_y = -STEP
        if self.is_moving_down:
            speed_y = STEP

        if WIDTH >= self.pos_x + speed_x >= 0:
            self.pos_x += speed_x
            self.rect.x += speed_x

        if HEIGHT >= self.pos_y + speed_y >= 0:
            self.pos_y += speed_y
            self.rect.y += speed_y


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

    player.update(events)
    camera.update(player)  # TODO all spirites
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)