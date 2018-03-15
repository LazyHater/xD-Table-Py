import colorsys
from random import random, randint
from display import Color


class Ball(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.x = randint(0, ctx.width)
        self.y = randint(0, ctx.height)
        self.dx = random()
        self.dy = random()
        self.max_dist = Ball.dist(0, 0, ctx.width, ctx.height)
        self.c = Color(*colorsys.hsv_to_rgb(random(), 1, 255))

    def handle_collisions_with_borders(self, dt):
        # left border
        if self.x + self.dx * dt < 0:
            self.x = 0
            self.dx *= -1

        # right border
        if self.x + self.dx * dt > self.ctx.width - 1:
            self.x = self.ctx.width - 1
            self.dx *= -1

        # up border
        if self.y + self.dy * dt < 0:
            self.y = 0
            self.dy *= -1

        # down border
        if self.y + self.dy * dt > self.ctx.height - 1:
            self.y = self.ctx.height - 1
            self.dy *= -1

    def update(self, dt):
        self.handle_collisions_with_borders(dt)
        self.x += self.dx
        self.y += self.dy

    @staticmethod
    def dist(x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def get_val(self, x, y):
        return ((1.0 - (Ball.dist(self.x, self.y, x, y) / self.max_dist)) ** 8)

    def render(self, display):
        for x in xrange(display.width):
            for y in xrange(display.height):
                display.set(x, y, Color(*colorsys.hsv_to_rgb(self.get_val(x, y), 1, 255)))

        display.set(int(self.x), int(self.y), Color(255, 255, 255))


class Metaballs(object):
    def __init__(self, bor):
        self.set_defaults()
        self.bor = bor
        self.width = bor.width
        self.height = bor.height
        self.balls = [Ball(self), Ball(self)]

    def step(self, dt):

        for b in self.balls:
            b.update(dt)

    def render(self, display):
        display.fill(Color(0, 0, 0))
        for x in xrange(display.width):
            for y in xrange(display.height):
                r, g, b = 0, 0, 0
                for ball in self.balls:
                    val = ball.get_val(x, y)
                    r += ball.c.r * val
                    g += ball.c.g * val
                    b += ball.c.b * val

                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255
                display.set(x, y, Color(r, g, b))

        # for b in self.balls:
        #    display.set(int(b.x), int(b.y), Color(255, 255, 255))

    def set_defaults(self):
        self.hue = 0
        self.dhue = 0.3
        self.ddhue = 0.1
        self.dshift = 0.005
        self.sat = 1
        self.dsat = 0.1
        self.val = 255
        self.dval = 3

    def on_press(self, key):
        if key == 'w':
            # incrase value
            self.val += self.dval
            if self.val > 255:
                self.val = 255

        if key == 's':
            # decrase value
            self.val -= self.dval
            if self.val < 0:
                self.val = 0

        if key == 'd':
            # incrase saturation
            self.sat += self.dsat
            if self.sat > 1:
                self.sat = 1

        if key == 'a':
            # decrase saturation
            self.sat -= self.dsat
            if self.sat < 0:
                self.sat = 0

        if key == 'f':
            # incrase hue change speed
            self.dhue += self.ddhue

        if key == 'g':
            # decrase hue change speed
            self.dhue -= self.ddhue

        if key == 'r':
            # reset to default
            self.set_defaults()