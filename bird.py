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
