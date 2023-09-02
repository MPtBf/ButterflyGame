import pygame as pg

from setts import *


pg.font.init()

class Transition:
    def __init__(self, sc, update_group, duration, functions=[], color="black"):
        self.update_group = update_group
        self.update_group.add(self)
        self.sc = sc

        self.functions = functions
        self.notified = False

        self.duration = duration
        self.current_time = 0
        self.color = color
        self.current_opacity = 0
        self.opacity_add = 2 / self.duration / FPS * 255

        self.image = pg.surface.Surface((SC_WIDTH, SC_HEIGHT))
        self.image.fill(self.color)
        self.image.set_alpha(255 - self.current_opacity)

        self.ended = False
        self.done = False

    def update(self):
        if not self.ended:
            if not self.done:
                self.current_opacity += self.opacity_add
            elif self.done:
                self.current_opacity -= self.opacity_add
            if self.current_opacity >= 255:
                self.current_opacity = 255
                self.done = True

            if self.done and self.current_opacity <= 0:
                self.current_opacity = 0
                self.ended = True

            self.image.set_alpha(self.current_opacity)

            if not self.notified and self.done:
                if self.functions != []:
                    for function in self.functions:
                        function["func"](function["args"])
                self.notified = True

    def add_function(self, new_function):
        self.functions.append(new_function)

    def get_surf(self):
        return self.image

    def kill(self):
        self.update_group.remove(self)
