from pico2d import *
import math

SCREEN_W = 800
SCREEN_H = 600

MOVE_CIRCLE = 1
MOVE_RECTANGLE = 2
MOVE_TRIANGLE = 3


class Character:
    def __init__(self):
        self.image = load_image('character.png')
        self.image_w = self.image.w
        self.image_h = self.image.h

        self.center_x = SCREEN_W / 2
        self.center_y = SCREEN_H / 2
        self.margin = max(self.image_w / 2, self.image_h / 2) + 20
        self.radius = min((SCREEN_W - 2 * self.margin) / 2, (SCREEN_H - 2 * self.margin) / 2)

        self.mode = MOVE_CIRCLE
        self.angle = math.pi / 2
        self.travel = 0.0
        self.speed = 2.0
        self.x, self.y = self.circle_point(self.angle)

    def circle_point(self, angle):
        return (self.center_x + self.radius * math.cos(angle),
                self.center_y + self.radius * math.sin(angle))

    def rectangle_points(self):
        return [
            (self.center_x, self.center_y + self.radius),
            (self.center_x + self.radius, self.center_y + self.radius),
            (self.center_x + self.radius, self.center_y - self.radius),
            (self.center_x - self.radius, self.center_y - self.radius),
            (self.center_x - self.radius, self.center_y + self.radius),
            (self.center_x, self.center_y + self.radius),
        ]

    def triangle_points(self):
        h = self.radius * math.sqrt(3) / 2
        return [
            (self.center_x, self.center_y + self.radius),
            (self.center_x + self.radius, self.center_y - h),
            (self.center_x - self.radius, self.center_y - h),
            (self.center_x, self.center_y + self.radius),
        ]

    def set_mode(self, new_mode):
        self.mode = new_mode
        self.travel = 0.0
        if new_mode == MOVE_CIRCLE:
            self.angle = math.pi / 2
            self.x, self.y = self.circle_point(self.angle)
        elif new_mode == MOVE_RECTANGLE:
            self.x, self.y = self.rectangle_points()[0]
        elif new_mode == MOVE_TRIANGLE:
            self.x, self.y = self.triangle_points()[0]

    def draw(self):
        self.image.draw(self.x, self.y)

    def point_on_path(self, points):
        total = 0.0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            total += math.hypot(x2 - x1, y2 - y1)

        current = self.travel
        if current >= total:
            current = total

        length = 0.0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            seg_len = math.hypot(x2 - x1, y2 - y1)
            if current <= length + seg_len:
                if seg_len == 0:
                    self.x, self.y = x1, y1
                else:
                    t = (current - length) / seg_len
                    self.x = x1 + (x2 - x1) * t
                    self.y = y1 + (y2 - y1) * t
                return
            length += seg_len

        self.x, self.y = points[-1]

    def update(self):
        if self.mode == MOVE_CIRCLE:
            self.update_circle()
        elif self.mode == MOVE_RECTANGLE:
            self.update_rectangle()
        elif self.mode == MOVE_TRIANGLE:
            self.update_triangle()

    def update_circle(self):
        circle_length = 2 * math.pi * self.radius
        self.travel += self.speed

        if self.travel >= circle_length:
            self.set_mode(MOVE_RECTANGLE)
            return

        self.angle = math.pi / 2 - self.travel / self.radius
        self.x, self.y = self.circle_point(self.angle)

    def update_rectangle(self):
        points = self.rectangle_points()
        total = 0.0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            total += math.hypot(x2 - x1, y2 - y1)

        self.travel += self.speed
        if self.travel >= total:
            self.set_mode(MOVE_TRIANGLE)
            return

        self.point_on_path(points)

    def update_triangle(self):
        points = self.triangle_points()
        total = 0.0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            total += math.hypot(x2 - x1, y2 - y1)

        self.travel += self.speed
        if self.travel >= total:
            self.set_mode(MOVE_CIRCLE)
            return

        self.point_on_path(points)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


open_canvas(SCREEN_W, SCREEN_H)
character = Character()

running = True
while running:
    clear_canvas()
    character.draw()
    update_canvas()

    running = handle_events()
    character.update()
    delay(0.01)

close_canvas()