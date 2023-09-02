import pygame as pg
from setts import *
from player import Player, Hitbox
from sprite_objects import Flycatcher, Flower, Spikes, Finish
from sky import Sky
from utils import *
from menu import StaminaBar, FlowersBar, HealthBar


class Level:
    def __init__(self, sc, player, all_objects, level_map, flowers_num, finish, difficulty_level, num, menu_manager, set_is_in_game, first_start):
        self.sc = sc

        self.num = num
        self.sky = Sky(self.sc, level_map)
        if first_start:
            self.completed = get_level_completed(self.num)
            self.sky.total_time_hours = get_level_total_time(self.num)
        else:
            self.completed = False
        self.active = False
        self.dead = False
        self.difficulty_level = difficulty_level
        self.menu_manager = menu_manager
        self.set_is_in_game = set_is_in_game
        self.flowers_num = flowers_num
        self.max_flower_num = self.flowers_num

        self.all_objects = all_objects
        self.player = player
        self.menu_objects = ApplyMethodGroup()
        self.stamina_bar = StaminaBar(self.sc, [self.menu_objects])
        self.flowers_bar = FlowersBar(self.sc, [self.menu_objects])
        self.flowers_bar.max_score = self.max_flower_num
        self.health_bar = HealthBar(self.sc, [self.menu_objects])

        self.finish = finish

        self.setup()

        self.fly_time = 4 * FPS - 5
        self.fly_timer = self.fly_time

    def setup(self):
        self.all_sprites = CameraGroup(self.player.hitbox.get_center())
        self.bg = pg.transform.scale(load_image("../sprites/menus/bg.png"), (SC_WIDTH, SC_HEIGHT))
        for obj in self.all_objects:
            self.all_sprites.add(obj)
        self.all_sprites.add(self.player)

    def run(self):
        self.sky.update()
        self.sky.bg()
        if self.health_bar.score < self.health_bar.max_score and self.stamina_bar.score >= 0.1:
            self.stamina_bar.add_score(-0.075)
            self.health_bar.add_score(0.02)
        if self.player.sprint and self.player.can_sprint:
            self.stamina_bar.add_score(-0.1)
        elif not self.player.sprint and not 7 > self.sky.stage > 2:
            self.stamina_bar.add_score(0.05)
        self.player.set_can_sprint(self.stamina_bar.get_active())
        self.flowers_bar.set_score(self.max_flower_num - self.flowers_num)
        self.finish.set_flowers_num(self.flowers_num)
        self.all_sprites.update()
        self.collide()
        self.all_sprites.custom_draw(self.player)
        self.menu_objects.apply_method("update")
        self.sky.overlay()

        # fly sound
        self.fly_timer += 1
        if self.fly_timer >= self.fly_time:
            self.fly_timer = 0
            fly_sound()
            # if self.last_fly_channel == 0:
            # self.last_fly_channel = 1
            # fly_sound(volume=(self.player.direction.length() - 4) / 8 * 0.8)
            # elif self.last_fly_channel == 1:
            #     self.last_fly_channel = 0
            #     fly_sound2(volume=(self.player.direction.length() - 4) / 8 * 0.8)
        volume = 0
        volume2 = 0
        if module(self.player.direction.x) > player_max_h_speed * 3/5:
            volume = (module(self.player.direction.x) - player_max_h_speed * 3/5) / module(player_max_h_speed * 2) * 2/10
        if module(self.player.direction.y) > player_max_v_speed * 3/5:
            volume2 = (module(self.player.direction.y) - player_max_v_speed * 3/5) / module(player_max_v_speed * 2) * 2/10
        else:
            game_fly_sound.set_volume(0)
        game_fly_sound.set_volume(max(volume, volume2))

        if self.completed:
            game_fly_sound.stop()
            win_sound(volume=0.2)
            already_completed = get_level_completed(self.num)
            if not already_completed:
                set_level_completed(self.num)
            self.set_is_in_game(False)
            self.menu_manager.menus["win"].set_screenshot(self.sc.copy())
            self.menu_manager.menus["win"].level_num = self.num
            self.menu_manager.set_menu("win")
            self.menu_manager.transition = None
            self.menu_manager.menus["levels"].objects["buttons"][f"level{self.num}"].level_time = self.sky.total_time_hours
            self.menu_manager.menus["levels"].objects["buttons"][f"level{self.num}"].completed = True
            self.menu_manager.menus["win"].complete_time = self.sky.total_time_hours
            last_total_time = get_level_total_time(self.num)
            if last_total_time == 0 or self.sky.total_time_hours < last_total_time:
                set_level_total_time(self.num, self.sky.total_time_hours)
        elif self.dead:
            game_fly_sound.stop()
            death_sound()
            self.set_is_in_game(False)
            self.menu_manager.menus["death"].set_screenshot(self.sc.copy())
            self.menu_manager.menus["death"].level_num = self.num
            self.menu_manager.set_menu("death")
            self.menu_manager.transition = None
            self.menu_manager.menus["death"].complete_time = self.sky.total_time_hours

    def collide(self):
        # all collide objects
        objects_hitboxes_list = [self.all_objects[i].hitbox for i in range(len(self.all_objects))]
        collides = self.player.hitbox.get_rect().collidelistall(objects_hitboxes_list)
        if collides:
            for collide_index, collide in enumerate(collides):
                obj = self.all_objects[collide]

                if isinstance(obj, Finish):
                    if self.finish.completed:
                        self.completed = True

                elif isinstance(obj, Spikes):
                    # hit_sound()
                    spikes_sound(volume=1)
                    # self.player.direction.xy = (0, 0)
                    # self.player.move_to_start_pos()
                    # self.stamina_bar.score = self.stamina_bar.max_score
                    self.health_bar.add_score(-10)
                    if self.health_bar.score + self.health_bar.added_score <= -5:
                        self.dead = True

                    delta_x = obj.hitbox.centerx - self.player.hitbox.get_center_x()
                    delta_y = obj.hitbox.centery - self.player.hitbox.get_center_y()
                    # here was bug with deltas of not square objects and player
                    delta_x += ((self.player.rect.width - self.player.hitbox.get_width()) / 2) * normalize(delta_x)
                    delta_y += ((self.player.rect.height - self.player.hitbox.get_height()) / 2) * normalize(delta_y)
                    delta_x += ((obj.image.get_width() - obj.hitbox.width / 2) * normalize(delta_x))
                    delta_y += ((obj.image.get_height() - obj.hitbox.height / 2) * normalize(delta_y))
                    if module(delta_x) > module(delta_y):
                        self.player.direction.x = round(3 * 2 * (1 if delta_x < 0 else -1))
                    elif module(delta_x) < module(delta_y):
                        self.player.direction.y = round(3 * 2 * (1 if delta_y < 0 else -1))
                    continue

                elif isinstance(obj, Flycatcher):
                    if not obj.is_closed:
                        # hit_sound()
                        spikes_sound()
                        self.health_bar.add_score(-15)
                        if self.health_bar.score + self.health_bar.added_score <= -7.5:
                            self.dead = True

                        obj.close()
                        self.player.direction.xy = (0, 0)
                        # self.player.move_to_start_pos()
                        # self.stamina_bar.score = self.stamina_bar.max_score
                        delta_x = obj.hitbox.centerx - self.player.hitbox.get_center_x()
                        delta_y = obj.hitbox.centery - self.player.hitbox.get_center_y()
                        # here was bug with deltas of not square objects and player
                        delta_x += ((self.player.rect.width - self.player.hitbox.get_width()) / 2) * normalize(delta_x)
                        delta_y += ((self.player.rect.height - self.player.hitbox.get_height()) / 2) * normalize(delta_y)
                        delta_x += ((obj.image.get_width() - obj.hitbox.width / 2) * normalize(delta_x))
                        delta_y += ((obj.image.get_height() - obj.hitbox.height / 2) * normalize(delta_y))

                        if module(delta_x) > module(delta_y):
                            self.player.direction.y = 0
                            self.player.direction.x = round(3 * 2 * (1 if delta_x < 0 else -1))
                        elif module(delta_x) < module(delta_y):
                            self.player.direction.x = 0
                            self.player.direction.y = round(3 * 2 * (1 if delta_y < 0 else -1))
                    continue

                elif isinstance(obj, Flower):
                    eat_sound(volume=0.5)
                    obj.kill()
                    self.stamina_bar.add_score(self.stamina_bar.max_score)

                if not obj.collideable:
                    continue
                delta_x = obj.hitbox.centerx - self.player.hitbox.get_center_x()
                delta_y = obj.hitbox.centery - self.player.hitbox.get_center_y()
                # here was bug with deltas of not square objects and player
                delta_x += ((self.player.rect.width - self.player.hitbox.get_width()) / 2) * normalize(delta_x)
                delta_y += ((self.player.rect.height - self.player.hitbox.get_height()) / 2) * normalize(delta_y)
                delta_x += ((obj.image.get_width() - obj.hitbox.width / 2) * normalize(delta_x))
                delta_y += ((obj.image.get_height() - obj.hitbox.height / 2) * normalize(delta_y))


                # horizontal
                if module(delta_x) > module(delta_y):
                    if module(self.player.direction.x) > 0.5 * global_mult: # max 4.9, 9.9
                        hit_sound(volume=(module(self.player.direction.x) / 10) * 0.5)
                        if module(self.player.direction.x) > 4.5 * global_mult:
                            self.health_bar.add_score(-1)
                    if delta_x >= 0:
                        self.player.hitbox.set_x(obj.hitbox.topleft[0] - self.player.hitbox.get_width())
                    elif delta_x < 0:
                        self.player.hitbox.set_x(obj.hitbox.topright[0])
                    # braking and bouncing to opposite direction
                    self.player.direction.x = round(module(self.player.direction.x) / 2 * (1 if delta_x < 0 else -1))
                    # friction
                    if module(self.player.direction.y) > self.player.max_v_speed / 2:
                        if self.player.direction.y >= 0:
                            self.player.direction.y = self.player.max_v_speed / 2
                        else:
                            self.player.direction.y = -self.player.max_v_speed / 2
                # verticals
                elif module(delta_x) < module(delta_y):
                    if module(self.player.direction.y) > 0.3 * global_mult: # max 2.9, 5.9
                        hit_sound(volume=(module(self.player.direction.y) / 6) * 0.5)
                        if module(self.player.direction.y) > 2.75 * global_mult:
                            self.health_bar.add_score(-1)
                    if delta_y >= 0:
                        self.player.hitbox.set_bottom_left((self.player.hitbox.get_x(), obj.hitbox.topleft[1]))
                    elif delta_y < 0:
                        self.player.hitbox.set_top_left((self.player.hitbox.get_x(), obj.hitbox.bottomleft[1]))
                    # braking and bouncing to opposite direction
                    self.player.direction.y = round(module(self.player.direction.y) / 2 * (1 if delta_y < 0 else -1))
                    # friction
                    if module(self.player.direction.x) > self.player.max_h_speed / 2:
                        if self.player.direction.x >= 0:
                            self.player.direction.x = self.player.max_h_speed / 2
                        else:
                            self.player.direction.x = -self.player.max_h_speed / 2


        # defining flowers num
        flowers_num = 0
        for obj in self.all_sprites:
            if isinstance(obj, Flower):
                flowers_num += 1
        self.flowers_num = flowers_num



class CameraGroup(pg.sprite.Group):
    def __init__(self, start_pos):
        super().__init__()
        self.sc = pg.display.get_surface()
        self.offset = pg.math.Vector2(0, 0)

        rect = self.sc.get_rect()
        self.sc_rect = pg.surface.Surface((rect.width + player_max_h_speed * 2, rect.height + player_max_v_speed * 2)).get_rect()
        self.dead_target = None

        self.center = list(start_pos)
        self.moving = pg.math.Vector2(0, 0)

    def box_target_camera(self, target):
        if not self.dead_target:
            self.moving[0] = round(target.hitbox.get_center_x() - self.center[0], 1)
            self.moving[1] = round(target.hitbox.get_center_y() - self.center[1], 1)
        else:
            self.moving[0] = round(self.dead_target.rect.centerx - self.center[0], 1)
            self.moving[1] = round(self.dead_target.rect.centery - self.center[1], 1)
        if self.moving.xy != (0, 0):
            self.moving.normalize()


        if target.hitbox.get_center_x() < self.center[0]:
            self.center[0] += self.moving.x * 0.02 * global_mult / 2
        if target.hitbox.get_center_x() > self.center[0]:
            self.center[0] += self.moving.x * 0.02 * global_mult / 2

        if target.hitbox.get_center_y() < self.center[1]:
            self.center[1] += self.moving.y * 0.02 * global_mult / 2
        if target.hitbox.get_center_y() > self.center[1]:
            self.center[1] += self.moving.y * 0.02 * global_mult / 2

        self.offset.x = self.center[0] - SC_WIDTH / 2
        self.offset.y = self.center[1] - SC_HEIGHT / 2

    def custom_draw(self, player):
        # print(self.center, (self.offset.x, self.offset.y))
        # self.offset.x = player.hitbox.get_center_x() - SC_WIDTH / 2
        # self.offset.y = player.hitbox.get_center_y() - SC_HEIGHT / 2


        self.box_target_camera(player)
        self.sc_rect.topleft = add_all(self.center, (-player_max_h_speed - SC_WIDTH / 2, -player_max_v_speed - SC_HEIGHT / 2))

        for layer in sorted(LAYERS.values()):
            # # if sprite not on the screen it's not drawing
            # collides = self.sc_rect.collidelistall(self.sprites())
            # # print(len(collides))
            # for collide in collides:
            #     sprite = self.sprites()[collide]
            for sprite in self.sprites():
                if sprite.z != layer:
                    continue
                if isinstance(sprite.rect, FloatRect):
                    offset_rect = sprite.rect.get_rect()
                else:
                    offset_rect = sprite.rect.copy()
                offset_rect.center -= self.offset
                self.sc.blit(sprite.image, offset_rect)

        rect = pg.surface.Surface((SC_WIDTH - 800, SC_HEIGHT - 500)).get_rect()
        rect.topleft = (400, 250)

