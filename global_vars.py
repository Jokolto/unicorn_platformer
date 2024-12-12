from konstanten import CANVAS_WIDTH, CANVAS_HEIGHT
# nicht sehr schön ich weiss

# flags
FULL_SCREEN = False
pause_is_activated = False

# andere
current_screen = None
current_level = None
levels = []
canvas_width, canvas_height = CANVAS_WIDTH, CANVAS_HEIGHT
screen_width, screen_height = 0, 0
display = None
center_x, center_y = int(canvas_width / 2), int(canvas_height / 2)  # Center von screen
score = []
music = None
