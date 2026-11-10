import game_framework
from pico2d import *
import game_world


def init():
    pass


def finish():
    pass


def update():
    pass


def render():
    clear_canvas()
    game_world.render()
    update_canvas()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_mode()
            return
