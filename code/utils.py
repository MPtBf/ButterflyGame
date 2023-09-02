import pygame as pg


def load_image(path:str):
    return pg.image.load(path).convert_alpha()

def dir(tile_pos, dir, size):
    """
    :param size: width and height of
    :param tile_pos: tile pos
    :param dir: up; right; down; left and combinations for diagonals (upright, downright... upleft) or 0, 1, 2, 3, 4... 7

    :return: returns pos of tile in specified direction
    """

    width, height = size

    # straight
    if dir == "up" or dir == 0:
        return [tile_pos[0],
                tile_pos[1] - 1 if tile_pos[1] - 1 >= 0 else height - 1]
    elif dir == "right" or dir == 1:
        return [tile_pos[0] + 1 if tile_pos[0] + 1 <= width - 1 else 0,
                tile_pos[1]]
    elif dir == "down" or dir == 2:
        return [tile_pos[0],
                tile_pos[1] + 1 if tile_pos[1] + 1 <= height - 1 else 0]
    elif dir == "left" or dir == 3:
        return [tile_pos[0] - 1 if tile_pos[0] - 1 >= 0 else width - 1,
                tile_pos[1]]

    # diagonals
    elif dir == "upright" or dir == 4:
        return [tile_pos[0] + 1 if tile_pos[0] + 1 <= width - 1 else 0,
                tile_pos[1] - 1 if tile_pos[1] - 1 >= 0 else height - 1]
    elif dir == "downright" or dir == 5:
        return [tile_pos[0] + 1 if tile_pos[0] + 1 <= width - 1 else 0,
                tile_pos[1] + 1 if tile_pos[1] + 1 <= height - 1 else 0]
    elif dir == "downleft" or dir == 6:
        return [tile_pos[0] - 1 if tile_pos[0] - 1 >= 0 else width - 1,
                tile_pos[1] + 1 if tile_pos[1] + 1 <= height - 1 else 0]
    elif dir == "upleft" or dir == 7:
        return [tile_pos[0] - 1 if tile_pos[0] - 1 >= 0 else width - 1,
                tile_pos[1] - 1 if tile_pos[1] - 1 >= 0 else height - 1]

    else:
        print("error in dir(): указано несуществующее направление")

def module(x):
    return x if x >= 0 else -x
def normalize(x):
    if x == 0:
        return 0
        # raise ValueError("Нельзя нормализовать нулевой вектор")
    return 1 if x > 0 else -1

def add_all(sequence, other, subtract = False):
    # print(sequence, "AND", other)
    sequence = list(sequence).copy()
    if isinstance(other, (int, float)):
        for i in range(len(sequence)):
            sequence[i] += other * (-1 if subtract else 1)
    elif isinstance(other, (list, tuple)):
        for i in range(len(sequence)):
            sequence[i] += other[i] * (-1 if subtract else 1)
    # print(sequence, "sequence")
    return sequence
def mult_all(sequence, other, divide = False):
    # print(sequence, "AND", other)
    sequence = list(sequence).copy()
    if isinstance(other, (int, float)):
        for i in range(len(sequence)):
            if divide:
                sequence[i] /= other
            else:
                sequence[i] *= other
    elif isinstance(other, (list, tuple)):
        for i in range(len(sequence)):
            if divide:
                sequence[i] /= other[i]
            else:
                sequence[i] *= other[i]
    return sequence

def remove_from_string(string, list):
    if list == "nums":
        list = [str(i) for i in range(10)]
    elif list == "letters":
        list = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")
    new_string = ""
    for char in string:
        if char not in list:
            new_string += char
    return new_string

class FloatRect:
    def __init__(self, surf):
        if isinstance(surf, pg.surface.Surface):
            self.image = surf
        elif isinstance(surf, pg.Rect):
            self.image = pg.surface.Surface((surf.width, surf.height))
        else:
            raise TypeError("что")
        self.x = 0
        self.y = 0

    def get_rect(self):
        rect = self.image.get_rect()
        rect.topleft = round(self.x), round(self.y)
        return rect

    def __add__(self, other):
        if (type(other) == tuple or type(other) == list) and len(other) == 2:
            self.x += other[0]
            self.y += other[1]
        else:
            raise TypeError("что")
    def __sub__(self, other):
        if (type(other) == tuple or type(other) == list) and len(other) == 2:
            self.x -= other[0]
            self.y -= other[1]
        else:
            raise TypeError("что")

    def get_top_left(self):
        return (round(self.x), round(self.y))
    def set_top_left(self, list):
        self.x = list[0]
        self.y = list[1]

    def get_bottom_left(self):
        return (round(self.x), round(self.y + self.image.get_height()))
    def set_bottom_left(self, list):
        self.x = list[0]
        self.y = list[1] - self.image.get_height()

    def get_top_right(self):
        return (round(self.x + self.image.get_width()), round(self.y))
    def set_top_right(self, list):
        self.x = list[0] - self.image.get_width()
        self.y = list[1]

    def get_bottom_right(self):
        return (round(self.x + self.image.get_width()), round(self.y + self.image.get_height()))
    def set_bottom_right(self, list):
        self.x = list[0] - self.image.get_width()
        self.y = list[1] - self.image.get_height()


    def get_center(self):
        # return (round(self.x + self.image.get_width() / 2), round(self.y + self.image.get_height() / 2))  # default
        return (int(self.x + self.image.get_width() / 2), int(self.y + self.image.get_height() / 2))  # experimental - butterfly image not shaking
    def set_center(self, list):
        self.x = list[0] - self.image.get_width() // 2
        self.y = list[1] - self.image.get_height() // 2


    def get_center_x(self):
        return round(self.x + self.image.get_width() / 2)
    def set_center_x(self, x):
        self.x = x - self.image.get_width()

    def get_center_y(self):
        return round(self.y + self.image.get_height() / 2)
    def set_center_y(self, y):
        self.y = y - self.image.get_height()

    def get_x(self):
        return round(self.x)
    def set_x(self, x):
        self.x = x

    def get_y(self):
        return round(self.y)
    def set_y(self, y):
        self.y = y


    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

class ApplyMethodGroup:
    def __init__(self, sequence=[]):
        self.sequence = list(sequence)

    def apply_method(self, method):
        for element in self.sequence:
            eval(f"element.{method}()")

    def add(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            for element in other:
                self.sequence.append(other)
        else:
            self.sequence.append(other)

    def remove(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            for element in other:
                self.sequence.remove(other)
        else:
            self.sequence.remove(other)



