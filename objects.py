from funktionen import *


# Vom haupt Guide, aber einiges ist korrigiert
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None, surf=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        if surf:
            self.image.blit(surf, (0, 0))
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


# Vom haupt Guide, aber einiges ist korrigiert
class Block(Object):
    def __init__(self, x, y, size, xy=(96, 0), surface=None):
        super().__init__(x, y, size, size)
        if surface:
            self.image.blit(surface, (0, 0))
        else:
            block = get_block(size, xy)
            self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


# Vom haupt Guide
class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("traps", "fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Spike(Object):
    def __init__(self, x, y, surface):
        super().__init__(x, y, surface.get_width(), surface.get_height(), name="spike", surf=surface)
        self.image.blit(surface, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class BgTile:
    def __init__(self, x, y, size, surface, opacity):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.set_alpha(opacity)

        self.image.blit(surface, (0, 0))
        self.image = image_darken(self.image)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Text:
    def __init__(self, x, y, width, height, text, size=48):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        draw_text(self.image, text=text, size=size)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Trophy(Object):
    def __init__(self, x, y, surface=None):
        super().__init__(x, y, 64, 64, 'trophy')
        if surface:
            self.image.blit(surface, (0, 0))
        else:
            image = pygame.image.load('assets/items/Checkpoints/End/End (Idle).png')
            self.image.blit(image, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


# Button class (guide: https://www.youtube.com/watch?v=G8MYGDf_9ho&t=340s&ab_channel=CodingWithRuss)
# funktion und args parameter addiert
class Button:
    def __init__(self, x, y, image, surface, screens, function=None, *args):
        self.screens = screens
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.function = function
        self.func_args = args
        self.clicked = False
        self.surface = surface

    # zeichnen der Button an display
    def draw(self):
        # global current_screen
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.function in self.screens:
                        gv.current_screen = self.function
                    if self.func_args:
                        self.function(*self.func_args)
                    else:
                        self.function()
                    self.clicked = True
                else:
                    self.clicked = False
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

