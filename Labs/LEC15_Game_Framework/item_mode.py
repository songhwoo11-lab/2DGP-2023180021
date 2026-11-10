import game_framework
from pico2d import *
import game_world
from ball import Ball

update_underlying = True
image = None


def init():
    global image
    image = load_image('item_select.png')


def finish():
    global image
    image = None


def update():
    pass


def render():
    clear_canvas()
    game_world.render()
    image.draw(400, 300)
    update_canvas()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            for layer in game_world.world:
                for obj in layer[:]:
                    if isinstance(obj, Ball):
                        game_world.remove_object(obj)
            game_framework.pop_mode()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.pop_mode()
            return
