import pygame
from os import listdir
from os.path import isfile, join
from konstanten import *
import sys  # import Paket System
import global_vars as gv

pygame.init()


def get_block(size, xy):
    x, y = xy
    path = join("assets", "terrain", "terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(x, y, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_butt_image(name, rescale=tuple()):
    path = join("assets", "menu", "buttons", name)
    butt_image = pygame.image.load(path)
    if rescale:
        butt_image = pygame.transform.scale(butt_image, size=rescale)
    return butt_image


# Vom haupt Guide
def get_background(name):
    path = join("assets", "background", name)
    image = pygame.image.load(path)
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(gv.canvas_width // width + 1):
        for j in range(gv.canvas_height // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


# Vom haupt Guide
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


# Vom haupt Guide
def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


# Vom haupt Guide ursprünglich, aber viel korrigiert
def draw_play(window, background, bg_image, entities, objects, offset_x, play_buttons):
    # Hintergrund ein Image
    bg_image = pygame.transform.scale(bg_image, (gv.canvas_width, gv.canvas_height))
    window.blit(bg_image, (0, 0))

    # Tiled Bg
    # for tile in background:
    #   window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)
    for entity in entities:
        entity.draw(window, offset_x)
    pause_butt, try_again_butt, menu_butt = play_buttons[0], play_buttons[1], play_buttons[2]

    pause_butt.draw()

    if gv.pause_is_activated:
        menu_text = 'Pause'
        size = 100
        draw_text(window, (gv.center_x - ((len(menu_text) * size) / 4), 0), menu_text, colour=BLACK, size=size)
        try_again_butt.draw()
        menu_butt.draw()

    pygame.display.update()


def draw_screen(window, fps_clock, buttons, caption_text="", size=0, bg_img=None, hs_score_show=False, score_show=False):
    # viel ifs - nicht ideal
    fps_clock.tick(FPS)
    pygame.display.set_caption(f'{PROJECT_NAME} | fps: {fps_clock.get_fps():.1f}')
    if bg_img:
        bg_img = pygame.transform.scale(bg_img, (gv.canvas_width, gv.canvas_height))
        window.blit(bg_img, (0, 0))
    else:
        window.fill(BG)
    if caption_text:
        for text in [caption_text]:
            draw_text(window, (gv.center_x - ((len(text) * size) / 4), 0), caption_text, colour=TEXT_COLOR, size=size)

    if hs_score_show:
        with open("saves.txt", "r") as file:
            data = file.read()
            existing_score = [int(score) for score in data.split(',')[1:]]

        existing_score.extend([int(score) for score in gv.score])
        hs_list = sorted(existing_score, reverse=True)[0:3]
        for i, score in enumerate(hs_list):
            draw_text(gv.display, (gv.center_x, 130*i + 100), str(score), colour=TEXT_COLOR, size=60)

    if score_show and gv.current_level == 'endless':
        text = f'Your Score: {gv.score[-1]}'
        draw_text(gv.display, (gv.center_x - ((len(text) * size) / 4), 500), text,
                  colour=WHITE, size=45)

    for button in buttons:
        button.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            quit_game()
    pygame.display.update()


def draw_text(display, xy=(0, 0), text='', colour=(0, 0, 0), size=48, name="arial"):
    """Funktion für das Zeichnen von Text auf die Pygame Leinwand."""
    font = pygame.font.SysFont(name=name, size=size, bold=1)
    render_text = font.render(text, True, colour)
    display.blit(render_text, xy)


# Vom haupt Guide
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


# Vom haupt Guide
def load_sprite_sheets(dir1, dir2, width, height, direction=False, rescale=(52, 60)):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image))

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(surface, rescale))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def quit_game():
    with open("saves.txt", "r+") as file:
        data = file.read()
        print(data)
        for score in gv.score:
            file.write(f',{str(score)}')

    print('quit')
    pygame.quit()
    sys.exit()


def toggle_pause():
    gv.pause_is_activated = not gv.pause_is_activated


def toggle_full_screen():
    if not gv.FULL_SCREEN:
        gv.FULL_SCREEN = True
        flag = pygame.FULLSCREEN
        gv.canvas_width, gv.canvas_height = gv.screen_width, gv.screen_height
        # gv.canvas_width, gv.canvas_height = CANVAS_WIDTH, CANVAS_HEIGHT
    else:
        gv.canvas_width, gv.canvas_height = CANVAS_WIDTH, CANVAS_HEIGHT
        gv.FULL_SCREEN = False
        flag = pygame.RESIZABLE

    depth = pygame.display.mode_ok((gv.canvas_width, gv.canvas_height), flag)
    gv.display = pygame.display.set_mode((gv.canvas_width, gv.canvas_height), flag, depth)
    # center, buttons reconfiguration
    gv.center_x, gv.center_y = int(gv.canvas_width / 2), int(gv.canvas_height / 2)


# Vom haupt Guide, aber viel korrigiert
def handle_move(entity, objects):
    collide_left = collide(entity, objects, -PLAYER_VEL * 2)
    collide_right = collide(entity, objects, PLAYER_VEL * 2)
    if str(entity) == "Player":
        keys = pygame.key.get_pressed()
        entity.x_vel = 0
        if keys[pygame.K_LEFT] and not collide_left:
            entity.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT] and not collide_right:
            entity.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(entity, objects, entity.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            entity.make_hit()
        if obj and obj.name == 'trophy':
            # if gv.current_level != 'endless':
            entity.win()

        if obj and obj.name == "spike":
            entity.die()


def image_darken(image):
    # will subtract 50 from the RGB values of the surface called image.
    new_image = image
    dark = pygame.Surface((image.get_width(), image.get_height()), flags=pygame.SRCALPHA)
    dark.fill((25, 25, 25, 0))
    new_image.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return new_image
