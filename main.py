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
                Tile('wall', x, y)
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