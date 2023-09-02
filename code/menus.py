import pygame as pg

from utils import ApplyMethodGroup, remove_from_string, load_image
from setts import *
from button import Button, Label
from transition import Transition
from languages import language


class Menu:
    def __init__(self, sc, type, start_transition_func, redirect_function):
        self.sc = sc
        self.type = type

        self.update_group = ApplyMethodGroup()
        self.start_transition_func = start_transition_func
        self.redirect_function = redirect_function
        self.active = False

        self.objects = {
            "labels": {

            },
            "buttons": {

            },
        }

    def update(self):
        pass

    def run(self):
        # self.sc.fill("gray")
        # self.update_group.apply_method("update")
        for button in self.objects["buttons"].values():
            button.update()

        self.update()

        self.draw()

    def draw(self):
        for label in self.objects["labels"].values():
            self.sc.blit(label.get_total_image(), label.rect)
        for button in self.objects["buttons"].values():
            self.sc.blit(button.get_total_image(), button.rect)

class MainMenu(Menu):
    def __init__(self, sc, type, start_transition_func, redirect_function):
        super().__init__(sc, type, start_transition_func, redirect_function)
        self.is_game = True
        self.active = True
        text_color = (182, 122, 51)

        logo_img = load_image("../sprites/menus/logo.png")
        logo_label = Label(logo_img, (SC_WIDTH * 1/2, SC_HEIGHT * 1/4), (400, 250), "",
                               self.update_group, 40, "logo")
        play_button = Button("default", (SC_WIDTH / 2, SC_HEIGHT * 5/10), (400, 70),
                             language.play_button, self.update_group, 50, "play", text_color=text_color, function=self.on_button_event, icon="play")
        options_button = Button("default", (SC_WIDTH * 1/2, SC_HEIGHT * 6/10), (400, 70),
                             language.options_button, self.update_group, 50, "options", text_color=text_color, function=self.on_button_event, icon="options")
        quit_button = Button("default", (SC_WIDTH * 1/2, SC_HEIGHT * 7/10), (200, 70),
                             language.quit_button, self.update_group, 40, "quit", text_color=text_color, function=self.on_button_event, icon="back")
        self.objects = {
            "labels": {
                "logo": logo_label,
            },
            "buttons": {
                "play": play_button,
                "options": options_button,
                "quit": quit_button,
            },
        }

    def on_button_event(self, button_type, action_type=None):
        if action_type == None:
            return
        if action_type == "release":
            if button_type == "play":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "options":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "quit":
                self.is_game = False

    def on_transition_done(self, args):
        self.active = False

class LevelsMenu(Menu):
    def __init__(self, sc, type, start_transition_func, redirect_function, levels):
        super().__init__(sc, type, start_transition_func, redirect_function)
        self.levels = levels
        self.font2 = pg.font.Font(None, 40)
        self.text_color = (182, 122, 51)

        levels_label = Label("default", (SC_WIDTH * 1/2, SC_HEIGHT * 3/20), (350, 50), language.levels,
                               self.update_group, 40, "levels", icon="levels")
        cancel_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 9/10), (220, 70),
                             language.cancel_button, self.update_group, 40, "cancel", function=self.on_button_event, icon="back")
        self.objects = {
            "labels": {
                "levels": levels_label,
            },
            "buttons": {
                "cancel": cancel_button,
            }
        }
        nado_levels_c = levels_num
        levels_y = [3, 5, 7]
        levels_x = [3, 7, 11, 15, 19]
        i = 0
        for y in range(len(levels_y)):
            for x in range(len(levels_x)):
                if i >= nado_levels_c:
                    break
                play_level_button = Button("d", (SC_WIDTH * levels_x[x]/22, SC_HEIGHT * levels_y[y]/10), (250, 100),
                                           language.play_level + " " + str(i + 1), self.update_group, 30, "level" + str(i + 1),
                                           difficulty_level=list(self.levels.values())[i].difficulty_level,
                                           function=self.on_button_event, level_time=self.levels[i + 1].sky.total_time_hours,
                                           completed=self.levels[i + 1].completed)
                self.objects["buttons"]["level" + str(i + 1)] = play_level_button
                i += 1

    def update(self):
        for i, level in enumerate(self.levels.values()):
            btn = self.objects["buttons"]["level" + str(i + 1)]
            btn.total_time = level.sky.total_time_hours
            btn.completed = level.completed


    def on_button_event(self, button_type, action_type=None):
        if action_type == None:
            return
        if action_type == "release":
            if button_type == "cancel":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif "level" == remove_from_string(button_type, "nums"):
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])

    def on_transition_done(self, args):
        self.active = False

class OptionsMenu(Menu):
    def __init__(self, sc, type, start_transition_func, redirect_function):
        super().__init__(sc, type, start_transition_func, redirect_function)
        self.font = pg.font.Font(None, 30)
        self.font2 = pg.font.Font(None, 40)
        self.text_color = (182, 122, 51)
        self.text_color2 = (144, 172, 57)

        self.language = "Ру" if language_str == "ru" else "En"
        self.last_language = self.language

        settings_label = Label("default", (SC_WIDTH * 1/2, SC_HEIGHT * 3/20), (350, 50), language.options_button,
                               self.update_group, 40, "options", icon="options")

        language_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 4/10), (300, 50),
                               f"{language.language}: {self.language}", self.update_group, 30, "language", function=self.on_button_event, icon="language")
        menu_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 9/10), (220, 70),
                               language.cancel_button, self.update_group, 40, "back", function=self.on_button_event, icon="back")

        info_label = Label("default", (SC_WIDTH * 1/2, SC_HEIGHT * 23/30), (450, 50), language.lang_info_restart,
                               self.update_group, 30, "info", icon="info")

        self.objects = {
            "labels": {
                "settings": settings_label,
                "lang_info": info_label,
            },
            "buttons": {
                "language": language_button,
                "menu_button": menu_button,
            }
        }

    def update(self):
        if self.language != self.last_language:
            self.objects["buttons"]["language"].set_text(f"{language.language}: {self.language}")

        self.last_language = self.language

    def on_button_event(self, button_type, action_type=None):
        if action_type == None:
            return
        if action_type == "release":
            if button_type == "language":
                self.redirect_function([self.type, button_type])
            elif button_type == "back":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])

    def on_transition_done(self, args):
        self.active = False

class PauseMenu(Menu):
    def __init__(self, sc, type, start_transition_func, redirect_function):
        super().__init__(sc, type, start_transition_func, redirect_function)

        self.complete_time = None
        self.last_complete_time = self.complete_time

        self.level_num = 0
        self.last_level_num = self.level_num
        self.max_level_num = levels_num
        self.font = pg.font.Font(None, 30)
        self.font2 = pg.font.Font(None, 40)
        self.text_color = (182, 122, 51)
        self.text_color2 = (144, 172, 57)

        self.bg = pg.surface.Surface((SC_WIDTH, SC_HEIGHT))
        self.bg.fill("white")
        overlay_img = pg.surface.Surface((SC_WIDTH, SC_HEIGHT))
        overlay_img.fill("black")
        overlay_img.set_alpha(50)
        self.bg.blit(overlay_img, (0, 0))

        pause_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 1/6), (350, 50), language.pause,
                               self.update_group, 40, "pause", icon="pause")
        level_num_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 1/4), (350, 50), f"{language.level} {self.level_num}",
                               self.update_group, 40, "level_num", icon="num")
        time_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 3/9 + 0.1), (350, 50), f"{language.time}:  0{language.d}, 0{language.h}",
                               self.update_group, 40, "time", icon="time")

        resume_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 5/10), (300, 50),
                               language.resume, self.update_group, 30, "resume", function=self.on_button_event, icon="play")
        again_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 6/10), (300, 50),
                               language.play_again, self.update_group, 30, "again", function=self.on_button_event, icon="again")
        next_level_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 7/10), (300, 50),
                               language.next_level, self.update_group, 30, "next_level", function=self.on_button_event, icon="next")
        menu_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 8/10), (300, 50),
                               language.quit_button, self.update_group, 30, "back", function=self.on_button_event, icon="back")

        self.objects = {
            "labels": {
                "pause": pause_label,
                "level_num": level_num_label,
                "time": time_label,
            },
            "buttons": {
                "resume": resume_button,
                "again": again_button,
                "next_level": next_level_button,
                "back": menu_button,
            }
        }

    def update(self):
        self.sc.blit(self.bg, (0, 0))

        if self.level_num == self.max_level_num:
            if self.level_num != self.last_level_num:
                self.objects["buttons"]["next_level"].set_text(language.the_end)
        else:
            self.objects["buttons"]["next_level"].set_text(self.objects["buttons"]["next_level"].default_text)

        if self.level_num != self.last_level_num:
            self.objects["labels"]["level_num"].set_text(f"{language.level} {self.level_num}")
        self.last_level_num = self.level_num

        if self.complete_time != self.last_complete_time:
            self.objects["labels"]["time"].set_text(f"{language.time}: {(self.complete_time // 24) if self.complete_time != 0 else 0}{language.d}, {(self.complete_time % 24) if self.complete_time != 0 else 0}{language.h}")
        self.last_complete_time = self.complete_time

    def set_screenshot(self, screenshot):
        self.bg = screenshot
        overlay_img = pg.surface.Surface((SC_WIDTH, SC_HEIGHT))
        overlay_img.fill("black")
        overlay_img.set_alpha(50)
        self.bg.blit(overlay_img, (0, 0))

    def on_button_event(self, button_type, action_type=None):
        if action_type == None:
            return
        if action_type == "release":
            if button_type == "resume":
                self.on_transition_done([])
                self.redirect_function([self.type, button_type])
            elif button_type == "next_level":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "again":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "back":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])

    def on_transition_done(self, args):
        self.active = False

class WinMenu(PauseMenu):
    def __init__(self, sc, type, start_transition_func, redirect_function):
        super().__init__(sc, type, start_transition_func, redirect_function)

        win_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 1/6), (350, 50), f"{language.you_win}!",
                               self.update_group, 40, "win", icon="win")
        level_num_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 1/4), (350, 50), f"{language.level} {self.level_num}",
                               self.update_group, 40, "level_num", icon="num")
        time_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 3/9 + 0.1), (350, 50), f"{language.time}:  0{language.d}, 0{language.h}",
                               self.update_group, 40, "time", icon="time")

        again_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 5/10), (300, 50),
                               language.play_again, self.update_group, 30, "again", function=self.on_button_event, icon="again")
        next_level_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 6/10), (300, 50),
                               language.next_level, self.update_group, 30, "next_level", function=self.on_button_event, icon="next")
        menu_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 7/10), (150, 50),
                               language.quit_button, self.update_group, 30, "back", function=self.on_button_event, icon="back")

        self.objects = {
            "labels": {
                "win": win_label,
                "level_num": level_num_label,
                "time": time_label,
            },
            "buttons": {
                "next_level": next_level_button,
                "again": again_button,
                "back": menu_button,
            }
        }

    def on_button_event(self, button_type, action_type=None):
        if action_type == None:
            return
        if action_type == "release":
            if button_type == "next_level":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "again":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "back":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])

class DeathMenu(PauseMenu):
    def __init__(self, sc, type, start_transition_func, redirect_function):
        super().__init__(sc, type, start_transition_func, redirect_function)

        death_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 1/6), (350, 50), f"{language.you_died}!",
                               self.update_group, 40, "death", icon="death")
        level_num_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 1/4), (350, 50), f"{language.level} {self.level_num}",
                               self.update_group, 40, "level_num", icon="num")
        time_label = Label("d", (SC_WIDTH * 1/2, SC_HEIGHT * 3/9 + 0.1), (350, 50), f"{language.time}:  0{language.d}, 0{language.h}",
                               self.update_group, 40, "time", icon="time")

        again_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 5/10), (300, 50),
                               language.play_again, self.update_group, 30, "again", function=self.on_button_event, icon="again")
        next_level_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 6/10), (300, 50),
                               language.next_level, self.update_group, 30, "next_level", function=self.on_button_event, icon="next")
        menu_button = Button("d", (SC_WIDTH * 1/2, SC_HEIGHT * 7/10), (150, 50),
                               language.quit_button, self.update_group, 30, "back", function=self.on_button_event, icon="back")

        self.objects = {
            "labels": {
                "death": death_label,
                "level_num": level_num_label,
                "time": time_label,
            },
            "buttons": {
                "again": again_button,
                "next_level": next_level_button,
                "back": menu_button,
            }
        }

    def on_button_event(self, button_type, action_type=None):
        if action_type == None:
            return
        if action_type == "release":
            if button_type == "next_level":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "again":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])
            elif button_type == "back":
                self.start_transition_func(0.7, [{"func": self.on_transition_done, "args": []},
                                                 {"func": self.redirect_function, "args": [self.type, button_type]}])