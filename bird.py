from pico2d import get_canvas_height, get_canvas_width, load_image

import game_framework
import game_world
from game_constants import PIXEL_PER_METER


BIRD_SPEED_KMPH = 10.0
BIRD_SPEED_PPS = BIRD_SPEED_KMPH * 1000.0 / 3600.0 * PIXEL_PER_METER

SPRITE_WIDTH = 918
SPRITE_HEIGHT = 506
SPRITE_COLUMNS = 5
SPRITE_ROWS = 3
FRAME_COUNTS_PER_ROW = (5, 5, 4)

WINGTIP_TRAVEL_SOURCE_PX = 166.0
WINGTIP_TRANSITION_FRAMES = 5


def _build_frame_rectangles():
    rectangles = []
    for row, frame_count in enumerate(FRAME_COUNTS_PER_ROW):
        top = row * SPRITE_HEIGHT // SPRITE_ROWS
        bottom = (row + 1) * SPRITE_HEIGHT // SPRITE_ROWS
        for column in range(frame_count):
            left = column * SPRITE_WIDTH // SPRITE_COLUMNS
            right = (column + 1) * SPRITE_WIDTH // SPRITE_COLUMNS
            rectangles.append(
                (left, SPRITE_HEIGHT - bottom, right - left, bottom - top)
            )
    return tuple(rectangles)


FRAME_RECTS = _build_frame_rectangles()

BOY_DISPLAY_HEIGHT_PX = 100.0
BOY_HEIGHT_M = 2.0
PIGEON_WINGSPAN_M = 0.6
BIRD_SCALE = (
    BOY_DISPLAY_HEIGHT_PX * PIGEON_WINGSPAN_M
    / (BOY_HEIGHT_M * WINGTIP_TRAVEL_SOURCE_PX)
)
BIRD_DRAW_WIDTH = SPRITE_WIDTH / SPRITE_COLUMNS * BIRD_SCALE
BIRD_DRAW_HEIGHT = SPRITE_HEIGHT / SPRITE_ROWS * BIRD_SCALE

WINGTIP_SPEED_RATIO = 4.5
WINGTIP_TRAVEL_SCREEN_PX = WINGTIP_TRAVEL_SOURCE_PX * BIRD_SCALE
WINGTIP_DISTANCE_PER_FRAME = (
    WINGTIP_TRAVEL_SCREEN_PX / WINGTIP_TRANSITION_FRAMES
)
BIRD_FRAME_RATE = (
    BIRD_SPEED_PPS * WINGTIP_SPEED_RATIO / WINGTIP_DISTANCE_PER_FRAME
)


class Bird:
    image = None

    def __init__(self, x, y, direction=1):
        if direction not in (-1, 1):
            raise ValueError('direction must be -1 or 1')

        self.image = self._load_image()
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.frame = 0.0

    def update(self):
        elapsed = max(0.0, game_framework.frame_time)
        self.frame = (
            self.frame + BIRD_FRAME_RATE * elapsed
        ) % len(FRAME_RECTS)

    @classmethod
    def _load_image(cls):
        if cls.image is None:
            cls.image = load_image('bird_animation.png')
        return cls.image
