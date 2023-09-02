from pytmx.util_pygame import load_pygame
import pygame as pg
import sys
from setts import *
from level import Level
from player import Player
from sprite_objects import SpriteObject, Tile, BgTile, Flower, Roots, Stalactite, Grass, Flycatcher, Spikes, Finish
from random import choice
from menus import MainMenu, LevelsMenu
from menu_manager import MenuManager
from languages import language
from utils import *
import json

class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(language.butterfly_game)
        pg.display.set_icon(load_image("../sprites/interface/icon.png"))
        self.clock = pg.time.Clock()

        self.bg = pg.transform.scale(load_image("../sprites/menus/bg.png"), (SC_WIDTH, SC_HEIGHT))

        self.loading_sc_image = load_image("../sprites/menus/loading_sc_image.png")
        self.loading_sc_image = pg.transform.scale(self.loading_sc_image, (SC_WIDTH, SC_HEIGHT))

        self.menu_manager = None
        self.levels = {}
        for i in range(1, levels_num + 1):
            self.levels[i] = self.setup_level(i, True)

        self.is_in_game = False
        self.menu_manager = MenuManager(self.sc, self.levels, self.set_is_in_game, self.setup_level)

        for level in self.levels.values():
            level.menu_manager = self.menu_manager
    # level
    def setup_level(self, level_num, first_start):
        self.sc.blit(self.loading_sc_image, (0, 0))
        pg.display.flip()
        self.tiles = []
        self.flowers_num = 0
        self.player = None
        self.all_objects = []
        self.finish = None
        if level_num == 1: difficulty = 1
        elif level_num == 2: difficulty = 1
        elif level_num == 3: difficulty = 2
        elif level_num == 4: difficulty = 2
        elif level_num == 5: difficulty = 3
        elif level_num == 6: difficulty = 3
        elif level_num == 7: difficulty = 4
        elif level_num == 8: difficulty = 4
        elif level_num == 9: difficulty = 5
        elif level_num == 10: difficulty = 5
        data = load_pygame(f"../sprites/basic{level_num}.tmx")

        self.level_map = [[[] for j in range(data.height)] for i in range(data.width)]
        self.start_pos = None
        self.air_id = None
        self.create_objects(data)
        self.create_tiles(data, level_num)
        self.create_sprite_objects(data)

        return Level(self.sc, self.player, self.all_objects, self.level_map, self.flowers_num, self.finish, difficulty, level_num, self.menu_manager, self.set_is_in_game, first_start)

    def create_tiles(self, data, level_num):
        layer = data.get_layer_by_name("tiles")
        tiles_ids = [i for i in layer.data]
        if self.start_pos == None:
            raise Exception("Level have no start pos")
        self.air_id = layer.data[round(self.start_pos[1] / 32)][round(self.start_pos[0] / 32)]
        for x, y, surf in layer.tiles():
            if tiles_ids[y][x] == self.air_id:
                continue
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            surf = pg.transform.scale(surf, (surf.get_width() * global_mult, surf.get_height() * global_mult))
            tile = Tile(self.sc, surf, pos, [self.all_objects], self.level_map, (x, y))

        layer = data.get_layer_by_name("bg_tiles")
        for x, y, surf in layer.tiles():
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            surf = pg.transform.scale(surf, (surf.get_width() * global_mult, surf.get_height() * global_mult))
            bg_tile = BgTile(self.sc, surf, pos, [self.all_objects])

    def create_objects(self, data):
        for obj in data.objects:
            x, y = obj.x * global_mult, obj.y * global_mult
            if obj.name == "start_pos":
                self.start_pos = obj.x, obj.y
                player_img = load_image("../sprites/game/player.png").convert_alpha()
                player_img = pg.transform.scale(player_img, (player_img.get_width() / 2 * global_mult, player_img.get_height() / 2 * global_mult))
                player_surf = pg.surface.Surface((TILE_SIZE, TILE_SIZE))
                pos = (player_surf.get_width() // global_mult - player_img.get_width() // global_mult,
                       player_surf.get_height() // global_mult - player_img.get_height() // global_mult)
                player_surf.blit(player_img, pos)
                player_surf.set_colorkey("black")
                self.player = Player(self.sc, player_surf, (x, y))

    def create_sprite_objects(self, data):
        for obj in data.get_layer_by_name("sprite_objects"):
            x, y = obj.x * global_mult, obj.y * global_mult
            if obj.name == "flower":
                self.flowers_num += 1
                flower_img = obj.image
                flower_img = pg.transform.scale(flower_img, (TILE_SIZE, TILE_SIZE))
                flower_imgs = flower_img, pg.transform.flip(flower_img, True, False)
                flower = Flower(self.sc, choice(flower_imgs), (x, y), [self.all_objects])

            elif obj.name == "roots":
                roots_img = obj.image
                roots_img = pg.transform.scale(roots_img, (TILE_SIZE, TILE_SIZE))
                roots_imgs = roots_img, pg.transform.flip(roots_img, True, False)
                roots = Roots(self.sc, choice(roots_imgs), (x, y), [self.all_objects])

            elif obj.name == "stalactite":
                stalactite_img = obj.image
                stalactite_img = pg.transform.scale(stalactite_img, (TILE_SIZE, TILE_SIZE))
                stalactite_imgs = stalactite_img, pg.transform.flip(stalactite_img, True, False)
                stalactite = Stalactite(self.sc, choice(stalactite_imgs), (x, y), [self.all_objects])

            elif obj.name == "grass":
                grass_img = obj.image
                grass_img = pg.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                grass_imgs = grass_img, pg.transform.flip(grass_img, True, False)
                grass = Grass(self.sc, choice(grass_imgs), (x, y), [self.all_objects])

            elif obj.name == "flycatcher":
                flycatcher_imgs = [None, None]
                for i in range(2):
                    flycatcher_imgs[i] = load_image(f"../sprites/flycatcher/{i}.png")
                    flycatcher_imgs[i] = pg.transform.scale(flycatcher_imgs[i], (TILE_SIZE, TILE_SIZE))
                    flycatcher_imgs[i] = [flycatcher_imgs[i], pg.transform.flip(flycatcher_imgs[i], True, False)]
                flycatcher = Flycatcher(self.sc, [choice(flycatcher_imgs[0]), choice(flycatcher_imgs[1])], (x, y), [self.all_objects])

            elif obj.name == "spikes":
                img = obj.image
                img = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                imgs = img, pg.transform.flip(img, True, False)
                new_sprite_obj = Spikes(self.sc, choice(imgs), (x, y), [self.all_objects])

            elif obj.name == "finish":
                img = load_image("../sprites/game/finish.png")
                img = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                new_sprite_obj = Finish(self.sc, img, (x, y), [self.all_objects])
                self.finish = new_sprite_obj

            else:
                print("in main.py. Unknown sprite object. obj name -", obj.name)
                continue
                # new_obj_img = obj.image
                # new_obj_img = pg.transform.scale(new_obj_img, (TILE_SIZE, TILE_SIZE))
                # new_obj_imgs = new_obj_img, pg.transform.flip(new_obj_img, True, False)
                # new_obj = SpriteObject(self.sc, choice(new_obj_imgs), (x, y), [self.all_objects])

    def run(self):
        self.is_game = True
        while self.is_game:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_game = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.is_game = False
                    if event.key == pg.K_q:
                        keys = pg.key.get_pressed()
                        if keys[pg.K_LSHIFT]:
                            self.is_game = False
                        elif self.is_in_game:
                            self.is_in_game = False
                            game_fly_sound.stop()
                            click_sound()
                            level = self.get_active_level()
                            level.fly_timer = level.fly_time
                            self.menu_manager.menus["pause"].set_screenshot(self.sc.copy())
                            self.menu_manager.menus["pause"].level_num = level.num
                            self.menu_manager.menus["pause"].complete_time = level.sky.total_time_hours
                            self.menu_manager.set_menu("pause")
                            self.menu_manager.transition = None
                        else:
                            if self.menu_manager.get_active_menu() != None and self.menu_manager.get_active_menu().type == "main":
                                self.is_game = False
                            else:
                                if self.menu_manager.get_active_menu().type == "levels" or self.menu_manager.get_active_menu().type == "options":
                                    self.menu_manager.set_menu("main")
                                elif self.menu_manager.get_active_menu().type == "pause" or self.menu_manager.get_active_menu().type == "win" or self.menu_manager.get_active_menu().type == "death":
                                    self.menu_manager.set_menu("levels")

            self.last_language = language_str
            self.sc.blit(self.bg, (0, 0))
            if not self.menu_manager.is_game:
                self.is_game = False
            if self.is_in_game:
                c = 0
                for level in self.levels.values():
                    if level.active:
                        c += 1
                        level.run()
                if c > 1:
                    raise Exception("More than 1 levels active simultaneously")
            if not self.is_in_game:
                self.menu_manager.run()
            else:
                self.menu_manager.is_in_game = False

            now_fps = round(self.clock.get_fps())
            if now_fps < FPS - FPS / 20:
                print(now_fps, language.fps)

            pg.display.update()
            self.clock.tick(FPS)


        pg.quit()
        sys.exit()

    def set_is_in_game(self, value):
        self.is_in_game = value

    def get_active_level(self):
        active_levels = []
        for level in self.levels.values():
            if level.active:
                active_levels.append(level)
        if len(active_levels) > 1:
            raise Exception("More than 1 levels active simultaneously")
        return active_levels[0]

if __name__ == "__main__":
    game = Game()
    game.run()


