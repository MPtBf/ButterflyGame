import pygame as pg
from setts import *
from languages import language


class SpriteObject(pg.sprite.Sprite):
    def __init__(self, sc, image, pos, sequences):
        super().__init__()
        self.sequences = sequences
        for sequence in self.sequences:
            try:
                sequence.add(self)
            except:
                sequence.append(self)
        self.sc = sc
        if image == None:
            self.image = pg.surface.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill("blue")
        else:
            self.image = image
        self.first_img = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.copy()
        self.hitbox.center = self.rect.center
        self.z = LAYERS["sprite_objects"]
        self.collideable = True

    def kill(self):
        for sequence in self.sequences:
            sequence.remove(self)
        super().kill()


class Tile(SpriteObject):
    def __init__(self, sc, image, pos, sequences, level_map, level_map_pos):
        super().__init__(sc, image, pos, sequences)
        self.z = LAYERS["tiles"]
        self.level_map = level_map
        self.pos = level_map_pos
        self.level_map[self.pos[0]][self.pos[1]].append("T")

    def update(self):
        self.rect.center = self.hitbox.center

    def kill(self):
        self.level_map[self.pos[0]][self.pos[1]].remove("T")
        super().kill()


class BgTile(SpriteObject):
    def __init__(self, sc, image, pos, sequences):
        super().__init__(sc, image, pos, sequences)
        self.z = LAYERS["bg_tiles"]
        self.collideable = False


class RainTile(SpriteObject):
    def __init__(self, pos, sequences):
        super().__init__(None, None, pos, sequences)
        self.z = LAYERS["debug"]
        self.collideable = False


class Flower(SpriteObject):
    def __init__(self, sc, image, pos, sequences):
        super().__init__(sc, image, pos, sequences)
        self.hitbox = self.rect.copy().inflate(-48, -16)
        self.hitbox.midbottom = self.rect.midbottom
        self.collideable = False


class Roots(SpriteObject):
    def __init__(self, sc, image, pos, sequences):
        super().__init__(sc, image, pos, sequences)
        self.hitbox = self.rect.copy().inflate(-8 * global_mult / 2, -56 * global_mult / 2)
        self.hitbox.midtop = self.rect.midtop
        # self.collideable = True


class Stalactite(SpriteObject):
    def __init__(self, sc, image, pos, sequences):
        super().__init__(sc, image, pos, sequences)
        self.hitbox = self.rect.copy().inflate(-32 * global_mult / 2, -8 * global_mult / 2)
        self.hitbox.midtop = self.rect.midtop


class Grass(SpriteObject):
    def __init__(self, sc, image, pos, sequences):
        super().__init__(sc, image, pos, sequences)
        self.hitbox = self.rect.copy().inflate(-8 * global_mult / 2, -56 * global_mult / 2)
        self.hitbox.midbottom = self.rect.midbottom
        self.collideable = False


class Flycatcher(SpriteObject):
    def __init__(self, sc, images, pos, sequences):
        super().__init__(sc, images[0], pos, sequences)
        self.images = images
        self.is_closed = False
        self.hitbox = self.rect.copy().inflate(-32 * global_mult / 2, -48 * global_mult / 2)
        self.hitbox.midbottom = self.rect.midbottom

        self.open_time = 5 * FPS
        self.open_timer = 0

    def update(self):
        if self.open_timer >= self.open_time and self.is_closed:
            self.open_timer = 0
            self.is_closed = False
            self.open()

        if self.is_closed:
            self.open_timer += 1

    def close(self):
        self.image = self.images[1]
        self.hitbox = self.rect.copy().inflate(-32 * global_mult / 2, -16 * global_mult / 2)
        self.hitbox.midbottom = self.rect.midbottom
        self.is_closed = True
        self.open_timer = 0

    def open(self):
        self.image = self.images[0]
        self.hitbox = self.rect.copy().inflate(-32 * global_mult / 2, -48 * global_mult / 2)
        self.hitbox.midbottom = self.rect.midbottom
        self.is_closed = False
        self.open_timer = 0

class Spikes(SpriteObject):
    def __init__(self, sc, image, pos, sequences):
        super().__init__(sc, image, pos, sequences)
        self.hitbox = self.rect.copy().inflate(-8 * global_mult / 2, -8 * global_mult / 2)
        self.hitbox.center = self.rect.center

class Finish(SpriteObject):
    def __init__(self, sc, image, pos, sequences):
        super().__init__(sc, image, pos, sequences)
        self.z = LAYERS["sprite_objects"]
        self.collideable = False
        self.flowers_num = 0
        self.max_flowers_num = self.flowers_num
        self.font = pg.font.Font(None, 15)
        font_img = self.font.render(language.finish, True, "black")
        font_img2 = self.font.render(language.you_need + ":", True, "black")
        font_img3 = self.font.render(f"{language.flower} {self.max_flowers_num - self.flowers_num}/{self.max_flowers_num}", True, "black")

        self.image.blit(font_img, (0, 0))
        self.image.blit(font_img2, (0, 20))
        self.image.blit(font_img3, (0, 30))

        self.completed = False

    def set_flowers_num(self, flowers_num):
        self.flowers_num = flowers_num
        if self.flowers_num > self.max_flowers_num:
            self.max_flowers_num = self.flowers_num

    def update(self):
        font_img = self.font.render(language.finish, True, "black")
        font_img2 = self.font.render(language.you_need + ":", True, "black")
        font_img3 = self.font.render(f"{language.flower} {self.max_flowers_num}x", True, "black")

        self.image.blit(self.first_img, (0, 0))
        self.image.blit(font_img, (0, 0))
        self.image.blit(font_img2, (0, 20))
        self.image.blit(font_img3, (0, 30))

        self.completed = self.max_flowers_num - self.flowers_num == self.max_flowers_num




