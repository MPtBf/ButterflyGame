import pygame as pg
from random import randint

from setts import *
from utils import add_all, mult_all
from sprite_objects import RainTile


class Sky:
    def __init__(self, sc, level_map):
        self.sc = sc

        # day stages
        self.stage = 0
        self.last_stage = (self.stage + 1) % stages_num

        # colors
        self.bg_color = bg_color_levels[self.stage]
        self.overlay_color = overlay_color_levels[self.stage]

        # colors moving
        self.bg_col_moving = [0, 0, 0]
        self.overlay_col_moving = [0, 0, 0]

        # time
        self.time = get_time_from_stage(self.stage)

        # stars
        self.stars_poses = [[0, 0] for i in range(25)]
        for star_pos in self.stars_poses:
            star_pos[0] = randint(0, SC_WIDTH)
            star_pos[1] = randint(0, SC_HEIGHT)

        # total level time
        self.total_time_hours = 0
        self.hour_time = 0

        # # rain tiles
        # # defining rain positions
        # self.rain_tiles = [[[] for j in range(len(level_map))] for i in range(len(level_map[0]))]
        # self.rain_poses = []
        # self.rain_objects = []
        # # which of this two causes fewer lags
        # for x in range(len(level_map[0])):
        #     for y in range(len(level_map)):
        #         if "T" not in level_map[y][x]:
        #             self.rain_tiles[y][x].append("f")
        #             self.rain_poses.append((x * TILE_SIZE, y * TILE_SIZE))
        #             if randint(1, 100) < 101:
        #                 self.rain_objects.append(RainTile((x * TILE_SIZE, y * TILE_SIZE), []))
        #         else:
        #             break
        #
        # self.rain_poses = tuple(self.rain_poses)

        # for y in self.rain_tiles:
        #     print(y)

    def update(self):
        # increasing time
        self.time += 1
        self.hour_time += 1
        if self.hour_time >= day_length / 24:
            self.hour_time = 0
            self.total_time_hours += 1
        if self.time > day_length:
            self.time = 0

        # switching stages and colors moving
        day_stage = get_day_stage(self.time)
        self.stage = day_stage
        if day_stage % stages_num == (self.last_stage - 1) % stages_num:
            self.last_stage += 1
            self.last_stage %= stages_num
            self.bg_col_moving = self.get_col_moving(day_stage, bg_color_levels)
            self.overlay_col_moving = self.get_col_moving(day_stage, overlay_color_levels)
            self.bg_color = bg_color_levels[self.stage]
            self.overlay_color = overlay_color_levels[self.stage]
        self.bg_color = add_all(self.bg_color, self.bg_col_moving)
        self.overlay_color = add_all(self.overlay_color, self.overlay_col_moving)

        # printing time
        # print(str(round(self.time // 60 // 2.5)) + ":" + str(round((self.time // 2.5) % 60)))  # time - h:m
        # print(self.stage)

    def get_col_moving(self, day_stage, color_levels):
        col_moving = add_all(
            color_levels[(day_stage + 1) % stages_num],
            color_levels[day_stage],
            subtract=True)
        moving = mult_all(col_moving, stage_length, divide=True)
        return moving

    def bg(self):
        self.sc.fill(self.bg_color)
        # self.sc.fill(bg_color_levels[3])

    def stars(self):
        if self.stage < 2:
            return
        for star_pos in self.stars_poses:
            pg.draw.circle(self.sc, "white", star_pos, 1)

    def overlay(self):
        if not show_overlay[0]:
            return

        surf = pg.surface.Surface((SC_WIDTH, SC_HEIGHT))
        surf.fill(self.overlay_color[:3])
        surf.set_alpha(self.overlay_color[3])

        # self.sc.blit(surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.sc.blit(surf, (0, 0))

    def rain(self):
        return self.rain_objects



