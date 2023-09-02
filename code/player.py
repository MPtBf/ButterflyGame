import pygame as pg
from time import sleep

from setts import *
from utils import FloatRect, add_all, module, normalize, load_image


class Player(pg.sprite.Sprite):
    def __init__(self, sc, image, pos):
        super().__init__()
        self.sc = sc
        self.image = image
        self.rect = self.image.get_rect()
        self.start_pos = list(pos).copy()
        self.rect.topleft = (add_all(pos, 0)[0], pos[1] + 24 * global_mult / 2)
        self.hitbox = FloatRect(self.rect.inflate(-32 * global_mult / 2, -48 * global_mult / 2))
        self.hitbox.set_center(self.rect.center)
        self.z = LAYERS["player"]

        # animation
        self.default_image = self.image.copy()
        up = load_image("../sprites/game/player_animation/up.png").convert_alpha()
        player_img = pg.transform.scale(up, (up.get_width() / 2 * global_mult, up.get_height() / 2 * global_mult))
        player_surf = pg.surface.Surface((TILE_SIZE, TILE_SIZE))
        pos = (player_surf.get_width() // global_mult - player_img.get_width() // global_mult,
               player_surf.get_height() // global_mult - player_img.get_height() // global_mult)
        player_surf.blit(player_img, pos)
        player_surf.set_colorkey("black")
        between = load_image("../sprites/game/player_animation/between.png").convert_alpha()
        player_img = pg.transform.scale(between, (between.get_width() / 2 * global_mult, between.get_height() / 2 * global_mult))
        player_surf = pg.surface.Surface((TILE_SIZE, TILE_SIZE))
        pos = (player_surf.get_width() // global_mult - player_img.get_width() // global_mult,
               player_surf.get_height() // global_mult - player_img.get_height() // global_mult)
        player_surf.blit(player_img, pos)
        player_surf.set_colorkey("black")
        down = load_image("../sprites/game/player_animation/down.png").convert_alpha()
        player_img = pg.transform.scale(down, (down.get_width() / 2 * global_mult, down.get_height() / 2 * global_mult))
        player_surf = pg.surface.Surface((TILE_SIZE, TILE_SIZE))
        pos = (player_surf.get_width() // global_mult - player_img.get_width() // global_mult,
               player_surf.get_height() // global_mult - player_img.get_height() // global_mult)
        player_surf.blit(player_img, pos)
        player_surf.set_colorkey("black")
        self.animation = {
            "up": up,
            "between": between,
            "down": down,
        }
        self.rotation_angle = 0

        self.animation_time = 4
        self.animation_timer = 0
        self.animation_state = 0

        # movement
        self.direction = pg.math.Vector2(0, 0)
        self.h_speed = 0.05 * global_mult / 2
        self.v_speed = 0.03 * global_mult / 2
        self.max_h_speed = player_max_h_speed
        self.max_v_speed = player_max_v_speed
        self.gravitation = 0.1 * global_mult / 2
        self.max_fall_speed = 1.5 * global_mult / 2
        self.sprint = False
        self.can_sprint = True

        self.show_overlay = show_overlay

    def input(self):
        keys = pg.key.get_pressed()

        # movement
        # sprint
        if keys[pg.K_LCTRL] and self.sprint and self.can_sprint:
            self.max_h_speed = player_max_h_speed * 2
            self.max_v_speed = player_max_v_speed * 2
        else:
            self.max_h_speed = player_max_h_speed
            self.max_v_speed = player_max_v_speed
            self.sprint = False
        if keys[pg.K_LCTRL]:
            self.sprint = True

        # horizontal
        if keys[pg.K_d] and keys[pg.K_a]:
            if self.direction.x - self.h_speed < 0:
                self.direction.x += self.h_speed
            elif self.direction.x + self.h_speed > 0:
                self.direction.x += -self.h_speed
            else:
                self.direction.x = 0
        elif keys[pg.K_d]:
            if self.direction.x + self.h_speed < 0:
                self.direction.x += self.h_speed * 2
            else:
                self.direction.x += self.h_speed
        elif keys[pg.K_a]:
            if self.direction.x - self.h_speed > 0:
                self.direction.x += -self.h_speed * 2
            else:
                self.direction.x += -self.h_speed
        else:
            if self.direction.x - self.h_speed > 0:
                self.direction.x += -self.h_speed
            elif self.direction.x + self.h_speed < 0:
                self.direction.x += self.h_speed
            else:
                self.direction.x = 0
        # lead to max speed if speed better than it
        if module(self.direction.x) > self.max_h_speed:
            if self.direction.x > 0:
                self.direction.x -= self.h_speed * 2
            elif self.direction.x < 0:
                self.direction.x -= -self.h_speed * 2


        # vertical
        if keys[pg.K_s] and keys[pg.K_w]:
            if self.direction.y - self.v_speed < 0:
                self.direction.y += self.v_speed
            elif self.direction.y + self.v_speed > 0:
                self.direction.y += -self.v_speed
            else:
                self.direction.y = 0
        elif keys[pg.K_s]:
            if self.direction.y + self.v_speed < 0:
                self.direction.y += self.v_speed * 2
            else:
                self.direction.y += self.v_speed
        elif keys[pg.K_w]:
            if self.direction.y - self.v_speed > 0:
                self.direction.y += -self.v_speed * 2
            else:
                self.direction.y += -self.v_speed
        else:
            if self.direction.y - self.v_speed > 0:
                self.direction.y += -self.v_speed
            elif self.direction.y + self.v_speed < 0:
                self.direction.y += self.v_speed
            else:
                self.direction.y = 0
        # lead to max speed if speed better than it
        if module(self.direction.y) > self.max_v_speed:
            if self.direction.y > 0:
                self.direction.y -= self.v_speed * 2 + self.gravitation
            elif self.direction.y < 0:
                self.direction.y -= -(self.v_speed * 2 + self.gravitation)

        if not keys[pg.K_w] and self.direction.y < self.max_fall_speed:
            self.direction.y += self.gravitation
        elif not keys[pg.K_s]:
            self.direction.y -= self.gravitation

    def update(self):
        self.input()
        self.hitbox.x += self.direction.x
        self.hitbox.y += self.direction.y

        self.rect.center = self.hitbox.get_center()

        # animation
        keys = pg.key.get_pressed()
        if keys[pg.K_LCTRL] and self.sprint and self.can_sprint:
            self.animation_time = 3
        else:
            self.animation_time = 4

        is_w = keys[pg.K_w]
        self.image = self.default_image.copy()
        if self.animation_timer >= self.animation_time and is_w:
            self.animation_timer = 0
            self.animation_state += 1
            if self.animation_state >= 4:
                self.animation_state = 0
        if is_w:
            self.animation_timer += 1
            if self.animation_state == 0:
                self.image = self.animation["up"].copy()
            elif self.animation_state == 2:
                self.image = self.default_image.copy()
            elif self.animation_state == 2:
                self.image = self.animation["between"].copy()
            elif self.animation_state == 3:
                self.image = self.animation["down"].copy()
        self.set_image(pg.transform.rotate(self.image, -self.direction.x / (player_max_h_speed * 2) * max_player_animation_rotation_angle))
        if self.direction.y >= -0.5:
            self.set_image(pg.transform.scale(self.image, (self.image.get_width(),
                    self.image.get_height() * 3/10 + self.image.get_height() * 7/10 * module((self.direction.y - 6) / (player_max_v_speed * 2)))))
        # if self.direction.y >= -0.5:
        #     self.set_image(pg.transform.scale(self.image, (self.image.get_width(), self.image.get_height() * ((-self.direction.y + 12) / 15))))
        if not is_w:
            self.animation_timer = 0

    def move_to_start_pos(self):
        self.rect.topleft = (add_all(self.start_pos, 0)[0], self.start_pos[1] + 24 * global_mult / 2)
        self.hitbox.set_center(self.rect.center)

    def set_can_sprint(self, can_sprint):
        self.can_sprint = can_sprint

    def set_image(self, new_image):
        self.image = pg.surface.Surface(self.default_image.get_size())
        self.image.set_colorkey("black")
        self.image.blit(new_image, ((self.image.get_width() - new_image.get_width()) / 2, (self.image.get_height() - new_image.get_height()) / 2))



class Hitbox(pg.sprite.Sprite):
    def __init__(self, target, color):
        super().__init__()
        if isinstance(target, pg.surface.Surface):
            self.rect = target.get_rect()
        else:
            self.rect = target.hitbox
        if isinstance(self.rect, FloatRect):
            self.image = pg.surface.Surface((self.rect.get_width(), self.rect.get_height()))
        else:
            self.image = pg.surface.Surface((self.rect.width, self.rect.height))
        self.image.fill(color)
        self.z = LAYERS["debug"]


