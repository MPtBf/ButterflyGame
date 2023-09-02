import pygame as pg

from setts import *
from languages import language
from utils import remove_from_string, load_image


pg.font.init()

class Button:
    def __init__(self, image, center_pos, size, text, update_group, font_size, type,
                 difficulty_level=0, text_color=(182, 122, 51), allowed=True, function=None, icon=None, level_time=1, completed=False):
        self.update_group = update_group
        self.function = function
        self.update_group.add(self)
        self.icon = icon
        self.level_time = level_time
        if self.icon != None:
            self.icon = load_image(f"../sprites/menus/button_icons/{icon}.png")

        if image == "default" or image == "d":
            image = load_image("../sprites/menus/button.png")
        default_image = pg.transform.scale(image, size)
        self.image_without_text = default_image.copy()
        self.rect = default_image.get_rect()
        self.rect.center = center_pos
        self.image = default_image.copy()
        self.type = type
        self.default_text = text

        self.pressed = False
        self.pressed_timer = 0
        self.selected = False
        self.allowed = allowed

        self.font_size = font_size
        self.text_color = text_color
        self.text_color2 = (144, 172, 57)
        self.text = text
        font1 = pg.font.Font(None, self.font_size)
        self.font = font1
        if "level" == remove_from_string(self.type, [str(i) for i in range(10)]):
            self.completed = completed
            self.last_completed = self.completed
            self.completed_before = self.completed
            self.last_level_time = self.level_time
            self.min_level_time = self.level_time

            text_img = font1.render(self.text, True, self.text_color2)
            text_rect = text_img.get_rect()
            text_rect.center = (default_image.get_width() / 2, default_image.get_height() * 4/30)
            default_image.blit(text_img, text_rect)

            text_img3 = font1.render(f"{language.difficulty}: {difficulty_level}", True, self.text_color)
            text_rect3 = text_img3.get_rect()
            text_rect3.center = (default_image.get_width() / 2, default_image.get_height() * 32/40)
            default_image.blit(text_img3, text_rect3)

            self.image_without_completed = default_image.copy()


            text_img = font1.render(f"{language.pass_time}: {(self.min_level_time // 24) if self.min_level_time != 0 else '_'}{language.d}, {(self.min_level_time % 24) if self.min_level_time != 0 else '_'}{language.h}", True, self.text_color)
            text_rect = text_img.get_rect()
            text_rect.center = (default_image.get_width() / 2, default_image.get_height() * 24/40)
            default_image.blit(text_img, text_rect)

            selected_image = default_image.copy()
            default_image_mask = pg.mask.from_surface(default_image)
            image = default_image_mask.to_surface()
            overlay_image = image.copy()
            overlay_image.set_colorkey("black")
            overlay_image.set_alpha(70)
            selected_image.blit(overlay_image, (0, 0))

            text_img2 = font1.render(f"{language.completed}" if self.completed else f"{language.not_} {language.completed}", True, self.text_color)
            text_rect2 = text_img2.get_rect()
            text_rect2.center = (default_image.get_width() / 2, default_image.get_height() * 16/40)
            default_image.blit(text_img2, text_rect2)


            selected_image = default_image.copy()
            default_image_mask = pg.mask.from_surface(default_image)
            image = default_image_mask.to_surface()
            overlay_image = image.copy()
            overlay_image.set_colorkey("black")
            overlay_image.set_alpha(70)
            selected_image.blit(overlay_image, (0, 0))

            self.images = {
                "default": default_image,
                "selected": selected_image
            }
        else:
            font1 = pg.font.Font(None, self.font_size)
            self.font1 = font1
            text_img = font1.render(self.text, True, self.text_color)
            text_rect = text_img.get_rect()
            text_rect.center = (default_image.get_width() / 2, default_image.get_height() * 6/10)
            if self.icon != None:
                text_rect.centerx += self.rect.height / 4
                self.icon = pg.transform.scale(self.icon, (self.rect.height, self.rect.height))
                default_image.blit(self.icon, (0, 0))
            default_image.blit(text_img, text_rect)

            selected_image = default_image.copy()
            default_image_mask = pg.mask.from_surface(default_image)
            image = default_image_mask.to_surface()
            overlay_image = image.copy()
            overlay_image.set_colorkey("black")
            overlay_image.set_alpha(70)
            selected_image.blit(overlay_image, (0, 0))

            self.images = {
                "default": default_image,
                "selected": selected_image
            }

        self.last_is_pressed = False
        self.is_pressed = False

    def update(self):
        if "level" == remove_from_string(self.type, [str(i) for i in range(10)]):
            if self.completed:
                self.completed_before = True
            self.min_level_time = self.level_time if self.level_time < self.min_level_time or self.min_level_time == 0 else self.min_level_time
            if self.completed != self.last_completed or self.level_time != self.last_level_time:
                new_image = self.image_without_completed.copy()
                text_img = self.font.render(f"{language.completed}" if self.completed_before else f"{language.not_} {language.completed}", True, self.text_color)
                text_rect = text_img.get_rect()
                text_rect.center = (new_image.get_width() / 2, new_image.get_height() * 16/40)
                new_image.blit(text_img, text_rect)
                text_img = self.font.render(f"{language.pass_time}: {(self.min_level_time // 24) if self.min_level_time != 0 else '_'}{language.d}, {(self.min_level_time % 24) if self.min_level_time != 0 else '_'}{language.h}", True, self.text_color)
                text_rect = text_img.get_rect()
                text_rect.center = (new_image.get_width() / 2, new_image.get_height() * 24/40)
                new_image.blit(text_img, text_rect)
                self.images["default"] = new_image
                selected_image = new_image.copy()
                default_image_mask = pg.mask.from_surface(selected_image)
                image = default_image_mask.to_surface()
                overlay_image = image.copy()
                overlay_image.set_colorkey("black")
                overlay_image.set_alpha(70)
                selected_image.blit(overlay_image, (0, 0))
                self.images["selected"] = selected_image
            self.last_completed = self.completed
            self.last_level_time = self.level_time

        self.input()
        if self.selected:
            self.image = self.images["selected"]
        else:
            self.image = self.images["default"]


        if self.pressed and self.selected:
            self.image = self.images["default"]

        self.last_is_pressed = self.is_pressed

    def input(self):
        mouse = pg.mouse
        mouse_pos = mouse.get_pos()
        is_mouse_pressed = mouse.get_pressed()[0]

        self.selected = self.rect.collidepoint(mouse_pos)

        if is_mouse_pressed and self.selected:
            self.is_pressed = True
            self.image = self.images["default"]
        else:
            self.is_pressed = False

        if self.last_is_pressed != self.is_pressed:
            if self.is_pressed:
                self.on_button_press()
            elif is_mouse_pressed and not self.selected:
                self.on_button_press_cancel()
            elif not is_mouse_pressed and self.selected:
                self.on_button_release()

    def set_text(self, new_text):
        self.text = new_text

        default_image = self.image_without_text.copy()
        font1 = self.font1
        text_img = font1.render(self.text, True, self.text_color)
        text_rect = text_img.get_rect()
        text_rect.center = (default_image.get_width() / 2, default_image.get_height() * 6 / 10)
        if self.icon != None:
            text_rect.centerx += self.rect.height / 4
            self.icon = pg.transform.scale(self.icon, (self.rect.height, self.rect.height))
            default_image.blit(self.icon, (0, 0))
        default_image.blit(text_img, text_rect)

        selected_image = default_image.copy()
        default_image_mask = pg.mask.from_surface(default_image)
        image = default_image_mask.to_surface()
        overlay_image = image.copy()
        overlay_image.set_colorkey("black")
        overlay_image.set_alpha(70)
        selected_image.blit(overlay_image, (0, 0))

        self.images = {
            "default": default_image,
            "selected": selected_image
        }

    def on_button_press(self):
        click_sound()
        if self.function:
            self.function(self.type, action_type="press")
        self.pressed = True

    def on_button_release(self):
        if self.function:
            self.function(self.type, action_type="release")
        self.pressed = False

    def on_button_press_cancel(self):
        if self.function:
            self.function(self.type, action_type="cancel")
        self.pressed = False

    def get_total_image(self):
        return self.image

    def kill(self):
        self.update_group.remove(self)


class Label:
    def __init__(self, image, center_pos, size, text, update_group, font_size, type, text_color=(182, 122, 51), icon=None):
        self.update_group = update_group
        self.update_group.add(self)
        self.icon = icon
        if self.icon != None:
            self.icon = load_image(f"../sprites/menus/button_icons/{icon}.png")

        if image == "default" or image == "d":
            image = load_image("../sprites/menus/label.png")
        default_image = pg.transform.scale(image, size)
        self.image_without_text = default_image.copy()
        self.rect = default_image.get_rect()
        self.rect.center = center_pos
        self.image = default_image.copy()
        self.type = type
        self.default_text = text

        self.font_size = font_size
        self.text_color = text_color
        self.text_color2 = (144, 172, 57)
        self.text = text
        font1 = pg.font.Font(None, self.font_size)
        self.font1 = font1
        text_img = font1.render(self.text, True, self.text_color)
        text_rect = text_img.get_rect()
        text_rect.center = (default_image.get_width() / 2, default_image.get_height() * 6/10)
        if self.icon != None:
            text_rect.centerx += self.rect.height / 4
            self.icon = pg.transform.scale(self.icon, (self.rect.height, self.rect.height))
            default_image.blit(self.icon, (0, 0))
        default_image.blit(text_img, text_rect)

        self.image = default_image

    def update(self):
        pass

    def set_text(self, new_text):
        self.text = new_text

        default_image = self.image_without_text.copy()
        font1 = self.font1
        text_img = font1.render(self.text, True, self.text_color)
        text_rect = text_img.get_rect()
        text_rect.center = (default_image.get_width() / 2, default_image.get_height() * 6 / 10)
        if self.icon != None:
            text_rect.centerx += self.rect.height / 4
            self.icon = pg.transform.scale(self.icon, (self.rect.height, self.rect.height))
            default_image.blit(self.icon, (0, 0))
        default_image.blit(text_img, text_rect)

        self.image = default_image

    def get_total_image(self):
        return self.image

    def kill(self):
        self.update_group.remove(self)


