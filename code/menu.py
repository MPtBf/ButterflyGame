import pygame as pg

from setts import *
from utils import normalize, module, add_all, mult_all, FloatRect, load_image


class MenuElement:
    def __init__(self, sc, image, pos, groups):
        self.groups = groups
        for group in self.groups:
            try:
                group.add(self)
            except:
                group.append(self)
        self.z = LAYERS["menu"]

        self.sc = sc
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos if pos else (0, 0)

    def draw(self):
        self.sc.blit(self.image, self.rect)

    def kill(self):
        for group in self.groups:
            group.remove(self)


class StaminaBar(MenuElement):
    def __init__(self, sc, groups):
        image = pg.surface.Surface((30, 100))
        image.fill("white")
        bg = pg.surface.Surface((20, 90))
        bg.fill("gray80")
        image.blit(bg, (5, 5))
        self.progress_image = pg.surface.Surface((20, 90))
        super().__init__(sc, image, None, groups)
        self.rect.bottomleft = stamina_bar_pos

        self.icon_image = load_image("../sprites/interface/stamina_icon.png")
        self.icon_image = pg.transform.scale(self.icon_image, (40, 60))
        self.icon_rect = self.icon_image.get_rect()
        self.icon_rect.center = self.rect.center
        self.icon_rect.centery -= 85

        self.max_score = 50
        self.score = self.max_score
        self.last_score = None

        self.added_score = 0

    def update(self):
        self.score += self.added_score
        self.added_score = 0
        if self.score < 0:
            self.score = 0
        elif self.score > self.max_score:
            self.score = self.max_score

        if self.score != self.last_score:
            # print(self.score)
            size = (20, round(90 * (self.score / self.max_score)))
            self.progress_image = pg.surface.Surface(size)
            self.progress_image.fill("orange")
        self.draw()
        self.last_score = self.score

    def add_score(self, count):
        self.added_score += count

    def draw(self):
        self.sc.blit(self.image, self.rect)
        self.sc.blit(self.progress_image, add_all(self.rect.topleft, (5, 5)))
        self.sc.blit(self.icon_image, self.icon_rect)

    def get_active(self):
        return not self.score < 1


class FlowersBar(MenuElement):
    def __init__(self, sc, groups):
        image = pg.surface.Surface((30, 100))
        image.fill("white")
        bg = pg.surface.Surface((20, 90))
        bg.fill("gray80")
        image.blit(bg, (5, 5))
        self.progress_image = pg.surface.Surface((20, 90))
        super().__init__(sc, image, None, groups)
        self.rect.bottomleft = flowers_bar_pos

        self.icon_image = load_image("../sprites/interface/flower_icon.png")
        self.icon_image = pg.transform.scale(self.icon_image, (40, 60))
        self.icon_rect = self.icon_image.get_rect()
        self.icon_rect.center = self.rect.center
        self.icon_rect.centery -= 85

        self.max_score = 1
        self.score = self.max_score
        self.last_score = None

        self.added_score = 0

    def update(self):
        self.score = self.new_score if self.new_score != -1 else self.score
        self.added_score = 0
        if self.score < 0:
            self.score = 0
        elif self.score > self.max_score:
            self.score = self.max_score

        if self.score != self.last_score:
            # print(self.score)
            size = (20, round(90 * (self.score / self.max_score)))
            self.progress_image = pg.surface.Surface(size)
            self.progress_image.fill("yellow")
        self.draw()
        self.last_score = self.score

    def set_score(self, count):
        self.new_score = count

    def draw(self):
        self.sc.blit(self.image, self.rect)
        self.sc.blit(self.progress_image, add_all(self.rect.topleft, (5, 5)))
        self.sc.blit(self.icon_image, self.icon_rect)

    def get_active(self):
        return not self.score < 1


class HealthBar(MenuElement):
    def __init__(self, sc, groups):
        image = pg.surface.Surface((30, 100))
        image.fill("white")
        bg = pg.surface.Surface((20, 90))
        bg.fill("gray80")
        image.blit(bg, (5, 5))
        self.progress_image = pg.surface.Surface((20, 90))
        super().__init__(sc, image, None, groups)
        self.rect.bottomleft = health_bar_pos

        self.icon_image = load_image("../sprites/interface/health_icon.png")
        self.icon_image = pg.transform.scale(self.icon_image, (40, 40))
        self.icon_rect = self.icon_image.get_rect()
        self.icon_rect.center = self.rect.center
        self.icon_rect.centery -= 75

        self.max_score = 50
        self.score = self.max_score
        self.last_score = None

        self.added_score = 0

        self.hurt_delay_time = 30
        self.hurt_delay_timer = 0

    def update(self):
        self.score += self.added_score
        self.added_score = 0
        if self.score < 0:
            self.score = 0
        elif self.score > self.max_score:
            self.score = self.max_score

        if self.score != self.last_score:
            # print(self.score)
            size = (20, round(90 * (self.score / self.max_score)))
            self.progress_image = pg.surface.Surface(size)
            self.progress_image.fill("red")
        self.draw()
        self.last_score = self.score

        self.hurt_delay_timer += 1

    def add_score(self, count):
        if count > 0:
            self.added_score += count
        elif self.hurt_delay_timer >= self.hurt_delay_time:
            self.added_score += count
            self.hurt_delay_timer = 0

    def draw(self):
        self.sc.blit(self.image, self.rect)
        self.sc.blit(self.progress_image, add_all(self.rect.topleft, (5, 5)))
        self.sc.blit(self.icon_image, self.icon_rect)

    def get_active(self):
        return not self.score < 1







