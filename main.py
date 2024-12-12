import os  # import Paket Betriebssystem
import random
import pygame.mask

import global_vars
from objects import *
from pytmx.util_pygame import load_pygame
from entities import *


# Breite und Höhe vom Gerät
info = pygame.display.Info()
gv.screen_width, gv.screen_height = info.current_w, info.current_h
resolutions = []

# Verschiebe das Fenster an die gewünschten Koordinaten
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialisierung Pygame (eigentlich nicht, es ist in funktionen.py)
pygame.init()
pygame.mixer.init()


# Pygame display und FPS
gv.display = pygame.display.set_mode((gv.canvas_width, gv.canvas_height))  # erstelle eine Anzeige
FPSCLOCK = pygame.time.Clock()  # Initialisierung des Framerateclocks
pygame_icon = pygame.image.load('assets/characters/unicorn/idle.png')
pygame.display.set_icon(pygame_icon)

''' Screen funktionen (guide quelle: https://www.youtube.com/watch?v=GMBqjxcKogA&ab_channel=baraltech) '''


# Haupt menu Leinwand
def main_menu():
    # buttons
    abstand = 40  # y abstand zwischen den Tasten
    butt_width = 225  # Breite der Tasten
    butt_height = 120  # Höhe der Tasten
    butt_x, butt_y = 100, int(gv.center_y - butt_height / 2)

    # Bildintegration
    bg_img = pygame.image.load('assets/background/bg menu.jpg')
    play_butt_img = get_butt_image('play.png', (butt_width, butt_height))
    options_butt_img = get_butt_image('options.png', (butt_width, butt_height))
    exit_butt_img = get_butt_image('exit.png', (butt_width, butt_height))

    # Tasten init
    play_butt = Button(butt_x, (butt_height + abstand), play_butt_img, gv.display, screens, lvl_selection_screen)
    option_butt = Button(butt_x, 2 * (butt_height + abstand), options_butt_img, gv.display, screens, options)
    exit_butt = Button(butt_x, 3 * (butt_height + abstand), exit_butt_img, gv.display, screens, quit_game)

    main_menu_buttons = [option_butt, play_butt, exit_butt]

    # Caption Text
    caption_text = 'Unicorn Platformer'
    size = 60
    gv.pause_is_activated = False

    # music test
    if gv.music != 'audio/music/test.mp3':
        gv.music = 'audio/music/test.mp3'
        pygame.mixer.music.load(gv.music)
        pygame.mixer.music.play()

    while gv.current_screen == main_menu:
        draw_screen(gv.display, FPSCLOCK, main_menu_buttons, caption_text, size, bg_img=bg_img)


# Einstellung Leinwand
def options():
    # buttons configuration
    abstand = 20  # y abstand zwischen den Tasten
    butt_width = 225  # Breite der Tasten
    butt_height = 120  # Höhe der Tasten
    butt_x, butt_y = int(gv.center_x - butt_width / 2), int(gv.center_y - butt_height / 2)

    # Bildintegration
    bg_img = pygame.image.load('assets/background/hs_bg.png')
    back_butt_img = get_butt_image('back.png', (butt_width, butt_height))
    full_screen_butt_img = get_butt_image('fullscreen.png', (butt_width, butt_height))

    # options buttons
    back_butt = Button(butt_x, (butt_height + abstand) + 40, back_butt_img, gv.display, screens, main_menu)
    full_screen_butt = Button(butt_x, 2 * (butt_height + abstand) + 40, full_screen_butt_img, gv.display,
                              screens, toggle_full_screen)

    options_buttons = [back_butt, full_screen_butt]

    # Caption Text
    size = 60
    caption_text = 'Options'

    while gv.current_screen == options:
        draw_screen(gv.display, FPSCLOCK, options_buttons, caption_text, size, bg_img)


# high score screen
def high_score():
    # buttons configuration
    abstand = 0  # y abstand zwischen den Tasten
    butt_width = 225  # Breite der Tasten
    butt_height = 120  # Höhe der Tasten
    butt_x, butt_y = int(gv.center_x - butt_width / 2), int(gv.center_y - butt_height / 2)

    bg_img = pygame.image.load('assets/background/hs_bg.png')
    back_butt_img = get_butt_image('back.png', (butt_width, butt_height))
    back_butt = Button(butt_x, 4 * (butt_height + abstand) + 40, back_butt_img, gv.display, screens, main_menu)

    caption_text = 'High score'
    size = 60
    buttons = [back_butt]
    while gv.current_screen == high_score:
        draw_screen(gv.display, FPSCLOCK, buttons, caption_text, size, bg_img, hs_score_show=True)


# Game Over Leinwand
def end_screen():
    # buttons configuration
    abstand = 20  # y abstand zwischen den Tasten
    butt_width = 225  # Breite der Tasten
    butt_height = 120  # Höhe der Tasten
    butt_x, butt_y = int(gv.center_x - butt_height / 2), int(gv.center_y - butt_height / 2)

    # Soundintegration
    pygame.mixer.music.pause()
    lose_sound = pygame.mixer.Sound("audio/sounds/lose sound.mp3")
    pygame.mixer.Sound.play(lose_sound)

    # Bildintegration
    restart_butt_img = get_butt_image('replay.png', (butt_height, butt_height))
    main_menu_butt_img = get_butt_image('menu.png', (butt_height, butt_height))

    # buttons
    abstand_x = 100
    restart_butt = Button(butt_x-abstand_x, butt_y, restart_butt_img, gv.display, screens, restart)
    menu_butt = Button(butt_x+abstand_x, butt_y, main_menu_butt_img, gv.display, screens, main_menu)
    buttons = [restart_butt, menu_butt]

    # Caption Text
    size = 60
    caption_text = 'Game Over'
    while gv.current_screen == end_screen:
        draw_screen(gv.display, FPSCLOCK, buttons, caption_text, size, score_show=True)


# Ziel erreicht Leinwand
def wining_screen():
    # buttons configuration
    abstand = 0  # y abstand zwischen den Tasten
    butt_width = 225  # Breite der Tasten
    butt_height = 120  # Höhe der Tasten
    butt_x, butt_y = int(gv.center_x - butt_height / 2), gv.canvas_height-butt_height-40

    # Soundintegration
    win_sound = pygame.mixer.Sound("audio/sounds/won sound.mp3")
    pygame.mixer.Sound.play(win_sound)

    # Bildintegration
    bg_img = pygame.image.load('assets/background/win_screen_bg.png')
    restart_butt_img = get_butt_image('replay.png', (butt_height, butt_height))
    main_menu_butt_img = get_butt_image('menu.png', (butt_height, butt_height))
    next_level_butt_img = get_butt_image('next.png', (butt_width, butt_height))

    # buttons
    abstand_x = 220
    restart_butt = Button(butt_x-abstand_x, butt_y, restart_butt_img, gv.display, screens, restart)
    menu_butt = Button(butt_x, butt_y, main_menu_butt_img, gv.display, screens, main_menu)
    next_level_butt = Button(butt_x+abstand_x, butt_y, next_level_butt_img, gv.display, screens, next_level)

    buttons = [restart_butt, menu_butt]
    if gv.current_level in gv.levels[0:-1]:
        buttons.append(next_level_butt)

    # size = 60
    # caption_text = 'Du hast gewonnen!'

    while gv.current_screen == wining_screen:
        draw_screen(gv.display, FPSCLOCK, buttons, bg_img=bg_img, score_show=True)


# Level Wähl Leinwand
def lvl_selection_screen():
    # center, buttons configuration
    x_abstand = 180  # x_abstand
    y_abstand = 40  # y_abstand zwischen den Tasten
    butt_width = 225  # Breite der Tasten
    butt_height = 120  # Höhe der Tasten
    butt_x, butt_y = int(gv.center_x - butt_width / 2), int(gv.center_y - butt_height / 2)

    # Bildintegration
    bg_img = pygame.image.load('assets/background/hs_bg.png')
    back_butt_img = get_butt_image('back.png', (butt_width, butt_height))
    hs_butt_img = get_butt_image('high_score.png', (butt_width, butt_height))
    level1_img = get_butt_image('level1.png', (butt_height, butt_height))
    level2_img = get_butt_image('level2.png', (butt_height, butt_height))
    level3_img = get_butt_image('level3.png', (butt_height, butt_height))
    endless_img = get_butt_image('endless.png', (butt_height, butt_height))

    # options buttons
    hs_butt = Button(gv.canvas_width // 4 - butt_height, 2 * (butt_height + y_abstand) + 40, hs_butt_img,
                     gv.display, screens, high_score)
    back_butt = Button(gv.canvas_width // 4 - butt_height, (butt_height + y_abstand) + 40, back_butt_img,
                       gv.display, screens, main_menu)
    level1_butt = Button(gv.canvas_width // 4 - butt_height + x_abstand * 2, (butt_height + y_abstand) + 40, level1_img,
                        gv.display, screens, play, "level1")
    level2_butt = Button(gv.canvas_width // 4 - butt_height + x_abstand * 3, (butt_height + y_abstand) + 40, level2_img,
                         gv.display, screens, play, "level2")
    level3_butt = Button(gv.canvas_width // 4 - butt_height + x_abstand * 4, (butt_height + y_abstand) + 40, level3_img,
                         gv.display, screens, play, "level3")
    endless_butt = Button(gv.canvas_width // 4 - butt_height + x_abstand * 3, (butt_height + y_abstand)*2 + 40,
                          endless_img, gv.display, screens, play, "endless")
    buttons = [level1_butt, level2_butt, level3_butt, endless_butt, back_butt, hs_butt]

    # Caption Text
    size = 60
    caption_text = 'Wählen Sie einen Level'

    while gv.current_screen == lvl_selection_screen:
        draw_screen(gv.display, FPSCLOCK, buttons, caption_text, size, bg_img)


# Haupt Spiel Leinwand
def play(level=gv.current_level):
    # center, buttons configuration
    abstand = 100  # x abstand zwischen den Tasten
    butt_width = 225  # Breite der Tasten
    butt_height = 120  # Höhe der Tasten
    butt_x, butt_y = int(gv.center_x - butt_height / 2), int(gv.center_y - butt_height / 2)

    gv.current_level = level
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

    # Bildintegration
    background, bg_image = get_background("gray.png")
    try_again_butt_img = get_butt_image('replay.png', (butt_height, butt_height))
    pause_butt_img = get_butt_image('pause.png', (50, 50))
    pause_butt_img.set_colorkey((255, 255, 255))
    main_menu_butt_img = get_butt_image('menu.png', (butt_height, butt_height))
    bg_test = pygame.image.load("assets/background/gif.gif")

    # Pause und Win Screen Tasten
    pause_butt = Button(10, 10, pause_butt_img, gv.display, screens, toggle_pause)
    try_again_butt = Button(butt_x - abstand, butt_y, try_again_butt_img, gv.display, screens, restart)
    menu_butt = Button(butt_x + abstand, butt_y, main_menu_butt_img, gv.display, screens, main_menu)

    play_buttons = [pause_butt, try_again_butt, menu_butt]

    # Einstellungen
    block_size = 48  # 48 - default (bad idea to change)

    # Player
    player = Player(300, 100, 52, 60, end_screen, wining_screen)
    enemy = Enemy(500, 9*block_size, 50, 50, 5*block_size)

    # Level import
    tmx_data = load_pygame(f"levels/{level}.tmx")
    blocks_layer = tmx_data.get_layer_by_name("blocks")
    objects_layer = tmx_data.get_layer_by_name("Objekts")

    # background_layer = tmx_data.get_layer_by_name("background")

    non_col_objects = []
    level = []

    # tiles layer zum level addieren
    for x, y, surf in blocks_layer.tiles():
        if block_size != 48:
            surf = pygame.transform.scale(surf, (block_size, block_size))
        level.append(Block(x*block_size, y*block_size, block_size, surface=surf))

    """
    for x, y, surf in background_layer.tiles():
        non_col_objects.append(BgTile(x*block_size, y*block_size, block_size, surf, background_layer.opacity*255))
    """

    # Objekte Layer zum Level addieren
    # noinspection PyTypeChecker
    for obj in objects_layer:
        if obj.type == "Trophy":
            level.append(Trophy(obj.x, obj.y, obj.image))

        if obj.type == "Text":
            non_col_objects.append(Text(obj.x, obj.y, obj.width, obj.height, obj.properties['text'], size=22))

    # Endless mode
    if gv.current_level == "endless":
        gv.music = 'audio/music/test_2.mp3'
        pygame.mixer.music.load(gv.music)
        pygame.mixer.music.play()
        pattern_num = 30
        pattern_width = 13*block_size
        rand_level = []

        # tiled map import
        patterns_maps = dict()
        for num, pattern in enumerate(os.listdir("levels/patterns")):
            if not (pattern == 'win_pattern.tmx'):
                patterns_maps[f'pattern {num+1}'] = load_pygame(f"levels/patterns/{pattern}")
        win_map = load_pygame(f"levels/patterns/win_pattern.tmx")

        # patterns layout import
        patterns = []
        for pattern_map in patterns_maps.values():
            patterns.append([pattern_map.get_layer_by_name("blocks"), pattern_map.get_layer_by_name("Objekts")])
        win_pattern = [win_map.get_layer_by_name("blocks"), win_map.get_layer_by_name("Objekts")]

        # level creation
        for i in range(1, pattern_num+1):
            choice = random.choice(patterns)
            if i == pattern_num:
                choice = win_pattern
            blocks_layer, objects_layer = choice[0], choice[1]

            for x, y, surf in blocks_layer.tiles():
                rand_level.append(Block(x * block_size + pattern_width*i, y * block_size, block_size, surface=surf))

            for obj in objects_layer:
                if obj.type == "Trophy":
                    rand_level.append(Trophy(obj.x + pattern_width*i, obj.y, obj.image))
                if obj.type == "Spike":
                    rand_level.append(Spike(obj.x + pattern_width*i, obj.y, obj.image))

        level.extend(rand_level)

    objects = [*level]
    all_obj = objects + non_col_objects
    entities = [player, enemy]

    offset_x = 0
    scroll_area_width = 400
    while gv.current_screen == play:
        FPSCLOCK.tick(FPS)
        pygame.display.set_caption(f'{PROJECT_NAME} | fps: {FPSCLOCK.get_fps():.1f}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    toggle_pause()
                if event.key == pygame.K_UP and player.jump_count < 2 and not gv.pause_is_activated:
                    player.jump()

        if not gv.pause_is_activated:
            for entity in entities:
                entity.loop(FPS)
                handle_move(entity, objects)

        draw_play(gv.display, background, bg_test, entities, all_obj, offset_x, play_buttons)

        if ((player.rect.right - offset_x >= CANVAS_WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel


# Spiel Restart
def restart():
    gv.pause_is_activated = False
    gv.current_screen = play
    play(gv.current_level)


# Funktion für next level button
def next_level():
    # Level Zahl + 1 (wird nur klappen, solange es weniger als 10 level gibt, aber so viel planen wir nicht machen)
    gv.current_level = f"level{int(gv.current_level[-1]) + 1}"
    gv.current_screen = play
    play(gv.current_level)


# Globale Variablen config
gv.current_screen = main_menu
gv.current_level = "level1"
gv.levels = ["level1", "level2", "level3"]
screens = [main_menu, play, options, high_score, end_screen, wining_screen, lvl_selection_screen]


# Program Start, wenn nicht importiert (hier, ist eigentlich egal)
if __name__ == "__main__":
    gv.current_screen()
