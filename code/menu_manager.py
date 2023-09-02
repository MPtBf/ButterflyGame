import pygame as pg

from setts import *
from menus import MainMenu, LevelsMenu, PauseMenu, WinMenu, OptionsMenu, DeathMenu
from transition import Transition
from utils import ApplyMethodGroup, remove_from_string
from languages import language


class MenuManager:
    def __init__(self, sc, levels, set_is_in_game_func, setup_level_func):
        self.sc = sc
        self.is_game = True
        self.is_in_game = False
        self.levels = levels
        self.set_is_in_game_func = set_is_in_game_func
        self.setup_level_func = setup_level_func

        self.menus = {
            "main": MainMenu(self.sc, "main", self.start_transition, self.redirect),
            "levels": LevelsMenu(self.sc, "levels", self.start_transition, self.redirect, self.levels),
            "options": OptionsMenu(self.sc, "options", self.start_transition, self.redirect),
            "pause": PauseMenu(self.sc, "pause", self.start_transition, self.redirect),
            "death": DeathMenu(self.sc, "death", self.start_transition, self.redirect),
            "win": WinMenu(self.sc, "win", self.start_transition, self.redirect),
        }

        self.transition = None
        self.update_group = ApplyMethodGroup()

    def run(self):
        for menu in self.menus.values():
            if menu.active:
                menu.run()
                if menu.type == "main" and not menu.is_game:
                    self.is_game = False

        self.update_group.apply_method("update")
        if self.transition != None:
            overlay_surf = self.transition.get_surf()
            self.sc.blit(overlay_surf, (0, 0))
        if self.transition != None and self.transition.ended:
            self.transition = None

    def start_transition(self, duration, functions):
        if self.transition == None:
            self.transition = Transition(self.sc, self.update_group, duration, functions=functions)

    def set_menu(self, menu_type):
        self.set_is_in_game_func(False)
        for level in self.levels.values():
            self.set_is_in_game_func(False)
        for menu in self.menus.values():
            if menu.type == menu_type:
                menu.active = True
            else:
                menu.active = False

    def redirect(self, args):
        menu_type, button_type = args
        # if menu_type == self.menus["main"].type:
        #     if button_type == self.menus["main"].objects["buttons"]["play"].type:
        #         self.menus["main"].active = True
        #         self.is_in_game = True

        if menu_type == self.menus["main"].type:
            if button_type == self.menus["main"].objects["buttons"]["play"].type:
                self.menus["main"].active = False
                self.menus["levels"].active = True
            elif button_type == self.menus["main"].objects["buttons"]["options"].type:
                self.menus["main"].active = False
                self.menus["options"].active = True
        elif menu_type == self.menus["levels"].type:
            if button_type == self.menus["levels"].objects["buttons"]["cancel"].type:
                self.menus["main"].active = True
                self.menus["levels"].active = False
            elif remove_from_string(self.menus["levels"].objects["buttons"]["level1"].type, "nums") == remove_from_string(button_type, "nums"):
                level_num = remove_from_string(button_type, "letters")
                for level in self.levels.values():
                    level.active = False
                self.levels[int(level_num)].active = True
                self.set_is_in_game_func(True)
        elif menu_type == self.menus["pause"].type:
            if button_type == self.menus["pause"].objects["buttons"]["resume"].type:
                if self.levels[self.menus["pause"].level_num].completed:
                    return
                self.menus["pause"].active = False
                self.levels[self.menus["pause"].level_num].active = True
                self.set_is_in_game_func(True)
            elif button_type == self.menus["pause"].objects["buttons"]["next_level"].type:
                for level in self.levels.values():
                    level.active = False
                if self.menus["pause"].level_num == max(self.levels.keys()):
                    self.set_is_in_game_func(False)
                    self.menus["pause"].active = False
                    self.menus["levels"].active = True
                    return
                self.levels[self.menus["pause"].level_num + 1].active = True
                self.set_is_in_game_func(True)
            elif button_type == self.menus["pause"].objects["buttons"]["again"].type:
                self.levels[self.menus["pause"].level_num] = self.setup_level_func(self.menus["pause"].level_num, False)
                self.levels[self.menus["pause"].level_num].active = True
                self.set_is_in_game_func(True)
            elif button_type == self.menus["pause"].objects["buttons"]["back"].type:
                self.menus["levels"].active = True
                self.menus["pause"].active = False
        elif menu_type == self.menus["win"].type:
            if button_type == self.menus["win"].objects["buttons"]["next_level"].type:
                for level in self.levels.values():
                    level.active = False
                if self.menus["win"].level_num == max(self.levels.keys()):
                    self.set_is_in_game_func(False)
                    self.menus["win"].active = False
                    self.menus["levels"].active = True
                    return
                self.levels[self.menus["win"].level_num + 1].active = True
                self.set_is_in_game_func(True)
            elif button_type == self.menus["win"].objects["buttons"]["again"].type:
                self.levels[self.menus["win"].level_num] = self.setup_level_func(self.menus["win"].level_num, False)
                self.levels[self.menus["win"].level_num].active = True
                self.set_is_in_game_func(True)
            elif button_type == self.menus["win"].objects["buttons"]["back"].type:
                self.menus["levels"].active = True
                self.menus["win"].active = False
                self.set_is_in_game_func(False)
        elif menu_type == self.menus["death"].type:
            if button_type == self.menus["death"].objects["buttons"]["next_level"].type:
                for level in self.levels.values():
                    level.active = False
                if self.menus["death"].level_num == max(self.levels.keys()):
                    self.set_is_in_game_func(False)
                    self.menus["death"].active = False
                    self.menus["levels"].active = True
                    return
                self.levels[self.menus["death"].level_num + 1].active = True
                self.set_is_in_game_func(True)
            elif button_type == self.menus["death"].objects["buttons"]["again"].type:
                self.levels[self.menus["death"].level_num] = self.setup_level_func(self.menus["death"].level_num, False)
                self.levels[self.menus["death"].level_num].active = True
                self.set_is_in_game_func(True)
            elif button_type == self.menus["death"].objects["buttons"]["back"].type:
                self.menus["levels"].active = True
                self.menus["death"].active = False
                self.set_is_in_game_func(False)
        elif menu_type == self.menus["options"].type:
            if button_type == self.menus["options"].objects["buttons"]["language"].type:
                if self.menus["options"].language == "En":
                    self.menus["options"].language = "Ру"
                    change_language("ru")
                elif self.menus["options"].language == "Ру":
                    self.menus["options"].language = "En"
                    change_language("en")
            elif button_type == self.menus["options"].objects["buttons"]["menu_button"].type:
                self.menus["main"].active = True
                self.menus["options"].active = False

    def get_active_menu(self):
        active_menus = []
        for menu in self.menus.values():
            if menu.active:
                active_menus.append(menu)
        if len(active_menus) > 1:
            raise Exception("More than 1 menus active simultaneously")
        return active_menus[0] if active_menus != [] else None


