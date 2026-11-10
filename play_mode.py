from pico2d import *
import game_world
import game_framework
from bird import Bird
from boy import Boy
from grass import Grass

boy = None
birds = []
BIRD_COUNT = 10


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy, birds

    boy = Boy()
    game_world.add_oject(boy)

    canvas_width = get_canvas_width()
    canvas_height = get_canvas_height()
    birds = []
    for index in range(BIRD_COUNT):
        x = canvas_width * (index + 0.5) / BIRD_COUNT
        y = canvas_height * (0.55 + 0.035 * index)
        direction = 1 if index % 2 == 0 else -1
        bird = Bird(x, y, direction)
        birds.append(bird)
        game_world.add_oject(bird)

    grass = Grass()
    game_world.add_oject(grass, 0)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()








