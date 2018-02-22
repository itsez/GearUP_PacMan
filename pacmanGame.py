from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty, StringProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.config import Config


class Pac(Widget):
    speed = 1
    velocity = Vector(0, 0)
    rotation = 0
    start_angle = NumericProperty(-50)  # -90 = closed mouth
    end_angle = NumericProperty(230)    # 270 = closed mouth
    dead = False
    curr_key = ''
    m_right = False
    m_left = False
    m_up = False
    m_down = False
    chomp_down = True

    def setup(self):
        self.pos = self.parent.x_marg + (32 * 9), self.parent.y_marg + (32 * 4)
        self.dead = False
        self.rotation = 0
        self.curr_key = ''
        self.start_angle = -50
        self.end_angle = 230
        self.velocity = Vector(0,0)

    def change_direction(self, grid):
        self.check_moves(grid)

        if self.curr_key == 'right' and self.m_right:
            self.rotate(180)
            self.velocity = Vector(1, 0)
        elif self.curr_key == 'left' and self.m_left:
            self.rotate(0)
            self.velocity = Vector(-1, 0)
        elif self.curr_key == 'up' and self.m_up:
            self.rotate(90)
            self.velocity = Vector(0, 1)
        elif self.curr_key == 'down' and self.m_down:
            self.rotate(-90)
            self.velocity = Vector(0, -1)

    def check_moves(self, grid):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        gx = int((self.x / self.parent.tile) - (self.parent.x_marg / self.parent.tile))
        gy = int((self.y / self.parent.tile) - (self.parent.y_marg / self.parent.tile))
        if self.y % 32 == 0:  # check to make sure we are centered
            if grid[gx][gy] == 'h' or grid[gx][gy] == 'hv':
                if not grid[gx-1][gy] == 'wall':
                    self.m_left = True
                elif self.velocity.x == -1 and self.x % 32 == 0:
                    self.velocity.x = 0

                if not grid[gx+1][gy] == 'wall':
                    self.m_right = True
                elif self.velocity.x == 1:
                    self.velocity.x = 0
        if self.x % 32 == 0:
            if grid[gx][gy] == 'v' or grid[gx][gy] == 'hv' and self.y % 32 == 0:
                if not grid[gx][gy-1] == 'wall':
                    self.m_down = True
                elif self.velocity.y == -1:
                    self.velocity.y = 0
                if not grid[gx][gy+1] == 'wall':
                    self.m_up = True
                elif self.velocity.y == 1:
                    self.velocity.y = 0

    def update_pos(self, grid):
        self.change_direction(grid)
        if self.x < self.parent.x_marg - 10:
            self.pos = 604,self.y
        elif self.x > self.parent.map_l + 10:
            self.pos = self.parent.x_marg, self.y
        self.pos = (self.velocity * self.speed) + self.pos

    def rotate(self, val):
        self.rotation = val
        self.start_angle = -50 + val
        self.end_angle = 230 + val

    def chomp(self):
        if self.start_angle == -90 + self.rotation:
            self.chomp_down = False
        if self.start_angle == -50 + self.rotation:
            self.chomp_down = True
        if self.chomp_down:
            self.start_angle += -1
            self.end_angle += 1
        else:
            self.end_angle += -1
            self.start_angle += 1


class TrackH(Widget):
    length = NumericProperty(608)


class TrackV(Widget):
    length = NumericProperty(672)


class Blinky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(1, 0)
    last_move = "right"
    color = ListProperty([.82,.24,.09])
    state = "normal"

    def setup(self):
        self.pos = self.parent.x_marg + (32 * 9), self.parent.y_marg + (32 * 12)
        self.velocity = Vector(1,0)
        self.state = "normal"

    def move(self, grid, pac_x, pac_y):
        self.check_moves(grid)
        if self.state == "normal":
            self.choose_move(pac_x, pac_y)
        elif self.state == "scared":
            self.scatter(pac_x, pac_y)
        self.pos = self.velocity * self.speed + self.pos
        if self.x >= self.parent.map_l + 10:
            self.x = self.parent.x_marg
        if self.x <= self.parent.x_marg - 10:
            self.x = self.parent.map_l

    def scatter(self, pac_x, pac_y):
        if self.last_move == "up" or self.last_move == "down":
            if pac_x > self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x < self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0,0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1,0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1,0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y > self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y < self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def choose_move(self, pac_x, pac_y):
        if self.last_move == "up" or self.last_move == "down":
            if pac_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x > self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0,0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1,0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1,0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def check_moves(self, grid):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        gx = int((self.x / self.parent.tile) - (self.parent.x_marg / self.parent.tile))
        gy = int((self.y / self.parent.tile) - (self.parent.y_marg / self.parent.tile))
        if self.y % 32 == 0:  # check to make sure we are centered
            if grid[gx][gy] == 'h' or grid[gx][gy] == 'hv':
                if not grid[gx - 1][gy] == 'wall':
                    self.m_left = True
                elif self.velocity.x == -1 and self.x % 32 == 0:
                    self.velocity.x = 0

                if not grid[gx + 1][gy] == 'wall':
                    self.m_right = True
                elif self.velocity.x == 1:
                    self.velocity.x = 0
        if self.x % 32 == 0:
            if grid[gx][gy] == 'v' or grid[gx][gy] == 'hv' and self.y % 32 == 0:
                if not grid[gx][gy - 1] == 'wall':
                    self.m_down = True
                elif self.velocity.y == -1:
                    self.velocity.y = 0
                if not grid[gx][gy + 1] == 'wall':
                    self.m_up = True
                elif self.velocity.y == 1:
                    self.velocity.y = 0

    def scared(self):
        self.color = [0,0,1]
        self.state = "scared"
        self.velocity = -self.velocity

    def reset_color(self):
        self.state = "normal"
        self.color = [.82, .24, .09]


class Pinky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, 1)
    last_move = "up"
    timer = 600
    color = ListProperty([.86,.51,.89])
    state = "spawning"

    def setup(self, ate=0):
        self.pos = self.parent.x_marg + (32 * 9), self.parent.y_marg + (32 * 10)
        self.velocity = Vector(0,1)
        self.last_move = "up"
        if not ate:
            self.timer = 600
        self.state = "spawning"

    def move(self, grid, pac_x, pac_y):
        self.check_moves(grid)
        if self.state == "spawning":
            self.spawning()
        if self.state == "normal":
            self.choose_move(pac_x, pac_y)
        elif self.state == "scared":
            self.scatter(pac_x, pac_y)
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= self.parent.map_l + 10:
            self.x = self.parent.x_marg
        if self.x <= self.parent.x_marg - 10:
            self.x = self.parent.map_l

    def spawning(self):
        self.timer += -1
        if self.top > self.parent.y_marg + (32 * 12):
            self.velocity = Vector(0, -1)
        elif self.y < self.parent.y_marg + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.timer < 120:
            self.velocity = Vector(0, 1)
        if self.y >= self.parent.y_marg + (32 * 12):
            self.velocity = Vector(1, 0)
            self.timer = 0
            self.state = "normal"

    def choose_move(self, pac_x, pac_y):
        if self.last_move == "up" or self.last_move == "down":
            if pac_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x > self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0,0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1,0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1,0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def scatter(self, pac_x, pac_y):
        if self.last_move == "up" or self.last_move == "down":
            if pac_x > self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x < self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0,0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1,0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1,0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y > self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y < self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def check_moves(self, grid):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        gx = int((self.x / self.parent.tile) - (self.parent.x_marg / self.parent.tile))
        gy = int((self.y / self.parent.tile) - (self.parent.y_marg / self.parent.tile))
        if self.y % 32 == 0:  # check to make sure we are centered
            if grid[gx][gy] == 'h' or grid[gx][gy] == 'hv':
                if not grid[gx - 1][gy] == 'wall':
                    self.m_left = True
                elif self.velocity.x == -1 and self.x % 32 == 0:
                    self.velocity.x = 0

                if not grid[gx + 1][gy] == 'wall':
                    self.m_right = True
                elif self.velocity.x == 1:
                    self.velocity.x = 0
        if self.x % 32 == 0:
            if grid[gx][gy] == 'v' or grid[gx][gy] == 'hv' and self.y % 32 == 0:
                if not grid[gx][gy - 1] == 'wall':
                    self.m_down = True
                elif self.velocity.y == -1:
                    self.velocity.y = 0
                if not grid[gx][gy + 1] == 'wall':
                    self.m_up = True
                elif self.velocity.y == 1:
                    self.velocity.y = 0

    def scared(self):
        if not self.state == "spawning":
            self.state = "scared"
            self.velocity = -self.velocity
            self.color = [0, 0, 1]

    def reset_color(self):
        self.color = [.86, .51, .89]
        self.state = "normal"


class Clyde(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, -1)
    last_move = "up"
    timer = 800
    color = ListProperty([.86,.52,.11])
    state = "spawning"

    def setup(self, ate=0):
        self.pos = self.parent.x_marg + (32 * 10), self.parent.y_marg + (32 * 10)
        self.velocity = Vector(0,-1)
        self.last_move = "up"
        if not ate:
            self.timer = 800
        self.state = "spawning"

    def move(self, grid, pac_x, pac_y):
        self.check_moves(grid)
        if self.state == "spawning":
            self.spawning()
        if self.state == "normal":
            self.choose_move(grid, pac_x, pac_y)
        elif self.state == "scared":
            self.scatter(grid, pac_x, pac_y)
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= self.parent.map_l + 10:
            self.x = self.parent.x_marg
        if self.x <= self.parent.x_marg - 10:
            self.x = self.parent.map_l

    def spawning(self):
        self.timer += -1
        if self.top > self.parent.y_marg + (32 * 12):
            self.velocity = Vector(0, -1)
        elif self.y < self.parent.y_marg + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.timer < 120:
            self.velocity = Vector(-1, 0)
        if self.x == self.parent.x_marg + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.y >= self.parent.y_marg + (32 * 12):
            self.velocity = Vector(1, 0)
            self.timer = 0
            self.state = "normal"

    def scatter(self, grid, pac_x, pac_y):
        if self.last_move == "up" or self.last_move == "down":
            if pac_x > self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x < self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0,0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1,0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1,0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y > self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y < self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def choose_move(self, grid, pac_x, pac_y):
        self.check_moves(grid)
        if self.last_move == "up" or self.last_move == "down":
            if pac_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x > self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0, 0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1, 0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1, 0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def check_moves(self, grid):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        gx = int((self.x / self.parent.tile) - (self.parent.x_marg / self.parent.tile))
        gy = int((self.y / self.parent.tile) - (self.parent.y_marg / self.parent.tile))
        if self.y % 32 == 0:  # check to make sure we are centered
            if grid[gx][gy] == 'h' or grid[gx][gy] == 'hv':
                if not grid[gx - 1][gy] == 'wall':
                    self.m_left = True
                elif self.velocity.x == -1 and self.x % 32 == 0:
                    self.velocity.x = 0

                if not grid[gx + 1][gy] == 'wall':
                    self.m_right = True
                elif self.velocity.x == 1:
                    self.velocity.x = 0
        if self.x % 32 == 0:
            if grid[gx][gy] == 'v' or grid[gx][gy] == 'hv' and self.y % 32 == 0:
                if not grid[gx][gy - 1] == 'wall':
                    self.m_down = True
                elif self.velocity.y == -1:
                    self.velocity.y = 0
                if not grid[gx][gy + 1] == 'wall':
                    self.m_up = True
                elif self.velocity.y == 1:
                    self.velocity.y = 0

    def scared(self):
        if not self.state == "spawning":
            self.state = "scared"
            self.velocity = -self.velocity
            self.color = [0, 0, 1]

    def reset_color(self):
        self.color = [.86, .51, .11]
        self.state = "normal"


class Inky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, -1)
    last_move = "up"
    timer = 1000
    color = ListProperty([.27,.74,.93])
    state = "spawning"

    def setup(self, ate=0):
        self.pos = self.parent.x_marg + (32 * 8), self.parent.y_marg + (32 * 10)
        self.velocity = Vector(0,-1)
        self.last_move = "up"
        if not ate:
            self.timer = 1000
        self.state = "spawning"

    def move(self, grid, pac_x, pac_y):
        self.check_moves(grid)
        if self.state == "spawning":
            self.spawning()
        if self.state == "normal":
            self.choose_move(pac_x, pac_y)
        elif self.state == "scared":
            self.scatter(pac_x, pac_y)
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= self.parent.map_l + 10:
            self.x = self.parent.x_marg
        if self.x <= self.parent.x_marg - 10:
            self.x = self.parent.map_l

    def spawning(self):
        self.timer += -1
        if self.top > self.parent.y_marg + (32 * 12):
            self.velocity = Vector(0, -1)
        elif self.y < self.parent.y_marg + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.timer < 120:
            self.velocity = Vector(1, 0)
        if self.x == self.parent.x_marg + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.y >= self.parent.y_marg + (32 * 12):
            self.velocity = Vector(1, 0)
            self.timer = 0
            self.state = "normal"

    def choose_move(self, pac_x, pac_y):
        if self.last_move == "up" or self.last_move == "down":
            if pac_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x > self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0, 0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1, 0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1, 0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def scatter(self, pac_x, pac_y):
        if self.last_move == "up" or self.last_move == "down":
            if pac_x > self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif pac_x < self.center_x and self.m_right:
                self.last_move = "right"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0,0):
                if self.m_right:
                    self.last_move = "right"
                    self.velocity = Vector(1,0)
                elif self.m_left:
                    self.last_move = "left"
                    self.velocity = Vector(-1,0)

        elif self.last_move == "left" or self.last_move == "right":
            if pac_y > self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif pac_y < self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def check_moves(self, grid):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        gx = int((self.x / self.parent.tile) - (self.parent.x_marg / self.parent.tile))
        gy = int((self.y / self.parent.tile) - (self.parent.y_marg / self.parent.tile))
        if self.y % 32 == 0:  # check to make sure we are centered
            if grid[gx][gy] == 'h' or grid[gx][gy] == 'hv':
                if not grid[gx - 1][gy] == 'wall':
                    self.m_left = True
                elif self.velocity.x == -1 and self.x % 32 == 0:
                    self.velocity.x = 0

                if not grid[gx + 1][gy] == 'wall':
                    self.m_right = True
                elif self.velocity.x == 1:
                    self.velocity.x = 0
        if self.x % 32 == 0:
            if grid[gx][gy] == 'v' or grid[gx][gy] == 'hv' and self.y % 32 == 0:
                if not grid[gx][gy - 1] == 'wall':
                    self.m_down = True
                elif self.velocity.y == -1:
                    self.velocity.y = 0
                if not grid[gx][gy + 1] == 'wall':
                    self.m_up = True
                elif self.velocity.y == 1:
                    self.velocity.y = 0

    def scared(self):
        if not self.state == "spawning":
            self.color = [0, 0, 1]
            self.state = "scared"
            self.velocity = -self.velocity

    def reset_color(self):
        self.color = [.27, .74, .93]
        self.state = "normal"


class PacGame(Widget):
    pac = ObjectProperty(None)
    blinky = ObjectProperty(None)
    pinky = ObjectProperty(None)
    inky = ObjectProperty(None)
    clyde = ObjectProperty(None)
    h_tracks = ListProperty()
    v_tracks = ListProperty()
    dots = ListProperty()
    score = NumericProperty(0)
    lives = NumericProperty(3)
    status = ObjectProperty()
    status2 = ObjectProperty()
    ready_check = True
    tile = 32  # size of tile
    map_l = (19 * tile)  # length of map
    map_h = (20 * tile)  # height of map
    x_marg = tile  # margin size for sides of window
    y_marg = tile  # margin size for top and bottom
    grid = [["wall" for i in range(21)]for j in range(22)]
    super_dots = []
    powerup = False

    def __init__(self, **kwargs):
        super(PacGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.build_level()
        self.status.text = "Ready?"
        self.redraw(self.status)
        self.redraw()
        self.draw_grid()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.pac.curr_key = keycode[1]
        if self.ready_check:
            self.ready_check = False

    def update(self, dt):
        if not self.ready_check:
            if self.pac.dead:
                self.status.text = "You Died"
                self.redraw(self.status)
                self.death()
            elif not self.pac.dead:
                self.pac.update_pos(self.grid)
                if not self.status == '':
                    self.status.text = ''
                    self.redraw(self.status)
                self.move_ghosts()
                self.check_ghost_collision()
                self.check_dot_collision()
                if not self.dots:
                    self.win()

    def redraw(self, widget=None):
        if widget:
            self.remove_widget(widget)
            self.add_widget(widget)
        else:
            self.redraw(self.pac)
            self.redraw(self.blinky)
            self.redraw(self.pinky)
            self.redraw(self.inky)
            self.redraw(self.clyde)

    def powered(self):
        self.blinky.scared()
        self.inky.scared()
        self.pinky.scared()
        self.clyde.scared()
        self.powerup = True
        Clock.schedule_once(self.unpower, 5)

    def unpower(self, dt):
        self.blinky.reset_color()
        if self.inky.state == "scared":
            self.inky.reset_color()
        if self.clyde.state == "scared":
            self.clyde.reset_color()
        if self.pinky.state == "scared":
            self.pinky.reset_color()
        self.powerup = False

    def death(self):
        if self.pac.end_angle > 90 + self.pac.rotation:
            self.pac.start_angle += 1
            self.pac.end_angle -= 1
        elif self.lives > 0:
            self.respawn_player()
        else:
            self.status.text = "You Lose"
            self.status2.text = "Press Enter to Restart"
            if self.pac.curr_key == "enter":
                self.pac.dead = False
                self.respawn_player(0)
            self.redraw(self.status)
            self.redraw(self.status2)

    def draw_grid(self):
        h_positions = [(0, 0, 19), (0, 2, 5), (6, 2, 3), (10, 2, 3), (14, 2, 5), (0, 4, 3), (4, 4, 11), (16, 4, 3),
                       (0, 6, 9), (10, 6, 9), (6, 8, 7), (-1, 10, 8), (12, 10, 8), (6, 12, 7), (0, 14, 5), (6, 14, 3),
                       (10, 14, 3), (14, 14, 5), (0, 16, 19), (0, 19, 9), (10, 19, 9)]
        v_positions = [(0, 0, 3), (8, 0, 3), (10, 0, 3), (18, 0, 3), (2, 2, 3), (4, 2, 18), (6, 2, 3), (12, 2, 3),
                       (14, 2, 18), (16, 2, 3), (0, 4, 3), (8, 4, 3), (10, 4, 3), (18, 4, 3), (6, 6, 7), (12, 6, 7),
                       (8, 12, 3), (10, 12, 3), (0, 14, 6), (6, 14, 3), (12, 14, 3), (18, 14, 6), (8, 16, 4), (10, 16, 4)]

        for i in h_positions:
            for j in range(i[2]):
                self.grid[i[0] + j][i[1]] = "h"

        for i in v_positions:
            for j in range(i[2]):
                if self.grid[i[0]][i[1]+j] == "h":
                    self.grid[i[0]][i[1]+j] = "hv"
                else:
                    self.grid[i[0]][i[1]+j] = "v"

    def move_ghosts(self):
        self.blinky.move(self.grid, self.pac.center_x, self.pac.center_y)
        self.pinky.move(self.grid, self.pac.center_x, self.pac.center_y)
        self.inky.move(self.grid, self.pac.center_x, self.pac.center_y)
        self.clyde.move(self.grid, self.pac.center_x, self.pac.center_y)

    def check_ghost_collision(self):
        if self.pac.collide_point(self.blinky.center_x, self.blinky.center_y):
            if self.blinky.state == "scared":
                self.blinky.setup()
            else:
                self.lives += -1
                self.pac.dead = True
        if self.pac.collide_point(self.pinky.center_x, self.pinky.center_y):
            if self.pinky.state == "scared":
                self.pinky.setup(1)
            else:
                self.lives += -1
                self.pac.dead = True
        if self.pac.collide_point(self.clyde.center_x, self.clyde.center_y):
            if self.clyde.state == "scared":
                self.clyde.setup(1)
            else:
                self.lives += -1
                self.pac.dead = True
        if self.pac.collide_point(self.inky.center_x, self.inky.center_y):
            if self.inky.state == "scared":
                self.inky.setup(1)
            else:
                self.lives += -1
                self.pac.dead = True

    def check_dot_collision(self):
        for i in self.super_dots:
            if self.pac.collide_point(i[0], i[1]):
                self.powered()
                with self.canvas:
                    Color(0, 0, 0)
                    Ellipse(pos=(i[0] + 8, i[1] + 8), size=(16, 16))
                self.score += 1
                self.super_dots.remove(i)
                self.redraw()
                break
        for i in self.dots:
            if self.pac.collide_point(i[0] + 8, i[1] + 8):
                self.score += 1
                self.dots.remove(i)
                with self.canvas:
                    Color(0, 0, 0)
                    Ellipse(pos=(i[0], i[1]), size=(8, 8))
                self.redraw()
                break

    def respawn_player(self, arg=1):
        self.inky.setup()
        self.pinky.setup()
        self.clyde.setup()
        self.pac.setup()
        self.blinky.setup()
        if arg == 0:
            self.lives = 3
            self.draw_dots()
            self.score = 0
            self.dots = []
            self.draw_dots()
            self.status2.text = ''
            self.redraw(self.status2)
        self.redraw(self.status)
        self.redraw()
        self.status.text = "Ready?"
        self.ready_check = True

    def win(self):

        self.status.text = "You Win"
        self.status2.text = "Press Enter to Restart"
        self.ready_check = True
        self.redraw(self.status)
        self.redraw(self.status2)
        if self.pac.curr_key == "enter":
            self.pac.dead = False
            self.respawn_player(0)

    def build_level(self):
        # h_positions = (#tiles x, #tiles y, #tiles length)
        h_positions = [(0,0,19), (0,2,5), (6,2,3), (10,2,3), (14,2,5), (0,4,3), (4,4,11), (16,4,3), (0,6,9), (10,6,9),
                       (6,8,7), (-1,10,8), (12,10,8), (6,12,7), (0,14,5), (6,14,3), (10,14,3), (14,14,5), (0,16,19),
                       (0,19,9), (10,19,9)]
        v_positions = [(0,0,3),(8,0,3),(10,0,3),(18,0,3),(2,2,3),(4,2,18),(6,2,3),(12,2,3),(14,2,18),(16,2,3), (0,4,3),
                      (8,4,3),(10,4,3),(18,4,3),(6,6,7), (12,6,7), (8,12,3),(10,12,3),(0,14,6),(6,14,3),(12,14,3),
                                                          (18,14,6), (8,16,4), (10,16,4)]

        for i in h_positions:
            track = TrackH(Color=(1,1,1,1),pos=(self.x_marg + (self.tile * i[0]), self.y_marg + (self.tile * i[1])))
            track.length = i[2] * self.tile
            self.h_tracks.append(track)
            self.add_widget(track)

        for i in v_positions:
            track = TrackV(Color=(1, 1, 1, 1), pos=(self.x_marg + (self.tile * i[0]), self.y_marg + (self.tile * i[1])))
            track.length = i[2] * self.tile
            self.v_tracks.append(track)
            self.add_widget(track)
        self.draw_dots()

        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(self.x_marg + (self.tile * 7) + 4, self.y_marg + (self.tile * 8) + 80 /2), size=(152, 80))
            Color(1, 1, 1)
            Rectangle(pos=(self.x_marg + (self.tile * 9)- 4, self.y_marg + (self.tile * 12) - 8), size=(40, 8))

    def draw_dots(self):
        super = [(self.tile, 64), (self.tile * 19, 64), (self.tile, self.tile * 19), (self.tile * 19, self.tile * 19)]
        for t in self.h_tracks:
            y_dot = t.center_y - 4
            x_dot = t.x + (self.tile / 2) - 4
            if x_dot < self.x_marg:                                          # makes sure left portal doesn't have dots
                x_dot += self.x_marg
            for i in range(t.width / self.tile):
                # check to not draw dots around spawn area or portal tracks
                if t.y == self.y_marg + (self.tile * 10):
                    break
                if x_dot < (self.tile * 5) + self.x_marg or x_dot > (self.tile * 14) + self.x_marg or\
                                y_dot < (self.tile * 8) + self.y_marg or y_dot > (self.tile * 14) + self.y_marg:
                        with self.canvas:
                            Color(244, 244, 230)
                            Ellipse(pos=(x_dot, y_dot), size=(8, 8))
                            self.dots.append((x_dot, y_dot))
                            x_dot += self.tile
                            if x_dot > 640 or x_dot > t.right:          # keeps the portals from misplacing dots
                                break
                else:
                    x_dot += self.tile

        for t in self.v_tracks:
            y_dot = t.y + (self.tile/2) - 4
            x_dot = t.center_x - 4
            for i in range(t.height / self.tile):
                # check to not draw dots around spawn
                if (x_dot, y_dot) not in self.dots and y_dot < (self.tile * 7) + self.y_marg or\
                                y_dot > (self.tile * 14) + self.y_marg or x_dot < (self.tile * 5) + self.x_marg or\
                                x_dot > (self.tile * 14) + self.x_marg:
                        with self.canvas:
                            Color(244, 244, 230)
                            Ellipse(pos=(x_dot, y_dot), size=(8, 8))
                            self.dots.append((x_dot, y_dot))
                            y_dot += self.tile
                else:
                    y_dot += self.tile
        # draw super dots
        self.super_dots = [(self.tile, 64), (self.tile * 19, self.tile * 2), (self.tile, self.tile * 19),
                           (self.tile * 19, self.tile * 19)]
        for i in self.super_dots:
            self.dots.remove((i[0] + 12, i[1] + 12))
            with self.canvas:
                Color(244, 244, 230)
                Ellipse(pos=(i[0] + 8, i[1] + 8), size=(16, 16))


class PacmanApp(App):
    def build(self):
        # ordering for game initialization
        Config.set('modules', 'monitor','')
        game = PacGame()
        Window.size = (672, 704)
        Window.top = 100
        Clock.schedule_interval(game.update, 20/60)
        return game


if __name__ == '__main__':
    PacmanApp().run()
