from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')


# fill here
running = True
x = 800 // 2
dir = 0
isLeft = False

def handle_events():
    # fill here
    global running, x, isLeft, dir
    events = get_events() # list
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                isLeft = False
                dir += 1
            elif event.key == SDLK_LEFT:
                isLeft = True
                dir -= 1        
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:  
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1

frame = 0
while running:
    clear_canvas()
    grass.draw(400, 30)
    if isLeft: character.clip_composite_draw(frame * 100, 100, 100, 100, 0, 'h', x, 90, 100, 100)
    else: character.clip_draw(frame * 100, 100, 100, 100, x, 90)
    update_canvas()

    handle_events()

    frame = (frame + 1) % 8
    x += dir * 5
    delay(0.05)


close_canvas()
