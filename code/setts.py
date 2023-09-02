import pygame as pg
from pytmx.util_pygame import load_pygame

TILE_SIZE = 64
global_mult = TILE_SIZE / 32
tiles_x = 20
tiles_y = 20

SC_WIDTH = 1542
SC_HEIGHT = 810
fullscreen = False

FPS = 60

levels_num = 10

with open("../data/game_data.txt", "r") as file:
    for line in file.read().split("\n"):
        if line.split(": ")[0] == "language":
            lang = line.split(": ")[1]
language_str = lang
def change_language(lang):
    if lang not in ["ru", "en"]:
        raise Exception()
    with open("../data/game_data.txt", "r") as file:
        file_content = file.read()
    with open("../data/game_data.txt", "w") as file:
        new_file_content = ""
        for line in file_content.split("\n"):
            if line.split(": ")[0] == "language":
                edited_line = line.split(": ")[0] + ": " + lang
                new_file_content += edited_line
            else:
                new_file_content += line
            if line != "":
                new_file_content += "\n"
        file.write(new_file_content)
def set_level_completed(level_num):
    if level_num not in [i + 1 for i in range(levels_num)]:
        raise Exception()
    with open("../data/temporary/levels_data.txt", "r") as file:
        file_content = file.read()
    with open("../data/temporary/levels_data.txt", "w") as file:
        new_file_content = ""
        for line in file_content.split("\n"):
            if line.split(": ")[0] == str(level_num):
                edited_line = line.split(": ")[0] + ": " + str(True)
                new_file_content += edited_line
            else:
                new_file_content += line
            if line != "":
                new_file_content += "\n"
        file.write(new_file_content)
def get_level_completed(level_num):
    level_num = int(level_num)
    if level_num not in [i + 1 for i in range(levels_num)]:
        raise Exception()
    with open("../data/temporary/levels_data.txt", "r") as file:
        file_content = file.read()
        for line in file_content.split("\n"):
            if line.split(": ")[0] == str(level_num):
                return True if "True" in line.split(": ")[1] else False
def set_level_total_time(level_num, total_time):
    if level_num not in [i + 1 for i in range(levels_num)]:
        raise Exception()
    with open("../data/temporary/levels_data.txt", "r") as file:
        file_content = file.read()
    with open("../data/temporary/levels_data.txt", "w") as file:
        new_file_content = ""
        for line in file_content.split("\n"):
            if line.split(": ")[0] == str(level_num) + "t":
                edited_line = line.split(": ")[0] + ": " + str(total_time)
                new_file_content += edited_line
            else:
                new_file_content += line
            if line != "":
                new_file_content += "\n"
        file.write(new_file_content)
def get_level_total_time(level_num):
    level_num = int(level_num)
    if level_num not in [i + 1 for i in range(levels_num)]:
        raise Exception()
    with open("../data/temporary/levels_data.txt", "r") as file:
        file_content = file.read()
        for line in file_content.split("\n"):
            if line.split(": ")[0] == str(level_num) + "t":
                return int(line.split(": ")[1])




health_bar_pos = (30, SC_HEIGHT - 30)
stamina_bar_pos = (90, SC_HEIGHT - 30)
flowers_bar_pos = (150, SC_HEIGHT - 30)

# default player speed  # !without sprint! sprint = v * 2
player_max_h_speed = 5 * global_mult / 2
player_max_v_speed = 3 * global_mult / 2

max_player_animation_rotation_angle = 70  # !without sprint! sprint = v * 2

LAYERS = {
    "bg": 1,
    "stars": 2,
    "bg_tiles": 3,
    "tiles": 4,
    "sprite_objects": 5,
    "player": 6,
    "front_decor": 7,
    "overlay": 8,
    "menu": 9,
    "debug": 10
}

stages_num = 8
day_length = 60 * FPS * 2

day_stages = [day_length / stages_num * (i + 1) for i in range(stages_num)]
stage_length = day_length / stages_num
def get_day_stage(time):
    if time > day_length or time < 0:
        raise ValueError("Время вышло за рамки длительности дня")
    for i, stage_time in enumerate(day_stages):
        if time <= stage_time:
            return i
def get_time_from_stage(stage):
    return stage * stage_length


bg_color_levels = (  # None
    (250, 240, 150),  # morning -     light yellow
    (200, 250, 230),  # noon -        light blue-green
    (250, 250, 210),  # afternoon -   light yellow-green
    (250, 140, 100),  # evening -           scarlet
    (80, 50, 100),    # early night - dark  blue-violet
    (40, 40, 80),     # midnight -    dark  blue
    (20, 40, 90),     # night -       dark  blue
    (210, 130, 150)   # early morning -     pale pink
)
overlay_color_levels = (  # None # no lags :)
    (250, 240, 150, 50),  # morning -     light yellow
    (200, 250, 230, 30),  # noon -        light blue-green
    (250, 250, 210, 30),  # afternoon -   light yellow-green
    (250, 140, 100, 100),  # evening -           scarlet
    (80, 50, 100, 140),    # early night - dark  blue-violet
    (40, 40, 80, 170),     # midnight -    dark  blue
    (20, 40, 90, 170),     # night -       dark  blue
    (40, 60, 100, 130)   # early morning -     pale pink
)
# overlay_color_levels = (  # BLEND_RGBA_MULT # LAGS :(
#     (80, 60, 100),    # morning -
#     (255, 250, 215),  # noon -
#     (100, 60, 90),    # afternoon -
#     (70, 70, 130),    # evening -
#     (50, 50, 100),    # early night -
#     (50, 50, 100),    # midnight -
#     (50, 50, 100),    # night -
#     (50, 50, 100)     # early morning -
# )

show_overlay = [True]

# sounds
pg.mixer.init()

channel1 = pg.mixer.Channel(0)  # click, hit
channel2 = pg.mixer.Channel(1)  # win
channel3 = pg.mixer.Channel(2)  # fly
channel4 = pg.mixer.Channel(3)  # eat
channel5 = pg.mixer.Channel(4)  # spikes

button_click_sound = pg.mixer.Sound("../sounds/button.mp3")
def click_sound(volume=1):
    global channel1, button_click_sound
    button_click_sound.set_volume(volume)
    channel1.play(button_click_sound, 0)
game_hit_sound = pg.mixer.Sound("../sounds/hit.mp3")
def hit_sound(volume=1):
    global channel1, game_hit_sound
    game_hit_sound.set_volume(volume)
    channel1.play(game_hit_sound, 0)
game_eat_sound = pg.mixer.Sound("../sounds/eat.mp3")
def eat_sound(volume=1):
    global channel4, game_eat_sound
    game_eat_sound.set_volume(volume)
    channel4.play(game_eat_sound, 0)
game_win_sound = pg.mixer.Sound("../sounds/win.mp3")
def win_sound(volume=1):
    global channel2, game_win_sound
    game_win_sound.set_volume(volume)
    channel2.play(game_win_sound, 0)
game_death_sound = pg.mixer.Sound("../sounds/death.mp3")
def death_sound(volume=1):
    global channel2, game_death_sound
    game_death_sound.set_volume(volume)
    channel2.play(game_death_sound, 0)
game_fly_sound = pg.mixer.Sound("../sounds/fly.mp3")
def fly_sound(volume=1):
    global channel3, game_fly_sound
    game_fly_sound.set_volume(volume)
    channel3.play(game_fly_sound, 0)
game_spikes_sound = pg.mixer.Sound("../sounds/spikes.mp3")
def spikes_sound(volume=1):
    global channel5, game_spikes_sound
    game_spikes_sound.set_volume(volume)
    channel5.play(game_spikes_sound, 0)

if __name__ == "__main__":
    pass
