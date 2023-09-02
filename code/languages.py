import pygame

from setts import *


class English:
    butterfly_game = "Butterfly Game"
    fps = "FPS"

    yes = "Yes"
    no = "No"

    play_button = "Play"
    options_button = "Options"
    quit_button = "Quit"
    cancel_button = "Cancel"
    play_level = "Level"
    level = "Level"
    completed = "Completed"
    not_ = "Not"
    difficulty = "Difficulty"
    resume = "Resume"
    pause = "Pause"
    the_end = "The End"
    play_again = "Play Again"
    you_win = "Level Complete"
    you_died = "You Died"
    levels = "Levels"
    show_overlay = "Show Overlay"
    time = "Time"

    language = "Language"

    finish = "Finish"
    you_need = "You need"
    flower = "Flower"
    next_level = "Next Level"

    pass_time = "Pass Time"
    d = "d"
    h = "h"

    lang_info_restart = "Restart The Game For The Result"

en = English()


class Russian:
    butterfly_game = "Игра про Бабочек"
    fps = en.fps
    
    yes = "Да"
    no = "Нет"
    
    play_button = "Играть"
    options_button = "Настройки"
    quit_button = "Выйти"
    cancel_button = "Отмена"
    play_level = "Уровень"
    level = "Уровень"
    completed = "Пройден"
    not_ = "Не"
    difficulty = "Сложность"
    resume = "Продолжить"
    next_level = "Следующий Уровень"
    pause = "Пауза"
    the_end = "Конец"
    play_again = "Начать Заново"
    you_win = "Уровень Пройден"
    language = "Язык"
    you_died = "Вы Проиграли"
    levels = "Уровни"
    show_overlay = "Показывать Наложение"
    time = "Время"

    finish = "Финиш"
    you_need = "Нужно"
    flower = "Цветок"

    pass_time = "За Время"
    d = "д"
    h = "ч"

    lang_info_restart = "Для Результата Перезапустите Игру"

ru = Russian()

language = en if language_str == "en" else ru
