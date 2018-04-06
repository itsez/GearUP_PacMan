from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle


class Pac(Widget):
    speed = 2                           # must be even number
    velocity = Vector(0, 0)
    rotation = 0
    start_angle = NumericProperty(-50)  # -90 = closed mouth
    end_angle = NumericProperty(230)    # 270 = closed mouth
    dead = False                        # keeps track of current state
    curr_key = ''                       # user input buffer
    m_right = False                     # these tell the possible directions to move
    m_left = False
    m_up = False
    m_down = False

    def setup(self):
        # Reset Pac to his default states and start positions.
        self.pos = self.parent.x_marg + (32 * 9), self.parent.y_marg + (32 * 4)
        self.dead = False
        self.rotation = 0
        self.curr_key = ''
        self.start_angle = -50
        self.end_angle = 230
        self.velocity = Vector(0, 0)

    def change_direction(self, grid):
        # Change direction based on the last input received if it is a possible move.
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
        # Check to see which moves are valid and stop us if we've hit a wall.
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
        # Try to change direction then update position based on the velocity.
        self.change_direction(grid)
        if self.x >= self.parent.map_l + 10:
            self.x = self.parent.x_marg
        if self.x <= self.parent.x_marg - 10:
            self.x = self.parent.map_l
        if self.y >= self.parent.map_h + 10:
            self.y = self.parent.y_marg
        if self.y <= self.parent.y_marg - 10:
            self.y = self.parent.map_h
        self.pos = (self.velocity * self.speed) + self.pos

    def rotate(self, val):
        # Rotate pac by val.
        self.rotation = val
        self.start_angle = -50 + val
        self.end_angle = 230 + val


class Blinky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = 1
    velocity = Vector(1, 0)
    last_move = "right"
    color = ListProperty([.82, .24, .09])
    scatter_timer = 100
    chase_timer = 0
    state = "scatter"
    step = 0

    def setup(self, ate=0):
        # Set blinky back to default settings and position.
        self.pos = self.parent.x_marg + (32 * 9), self.parent.y_marg + (32 * 12)
        self.velocity = Vector(1, 0)
        self.scatter_timer = 100
        self.speed = 1
        self.last_move = "right"
        if not ate:             # If this is a restart not a respawn.
            self.step = 0
            self.state = "scatter"
            self.scatter_timer = 300
        self.color = [.82, .24, .09]
        self.state = "normal"

    def move(self, grid, pac_x, pac_y):
        # Decide what movement state we are in then call that method.
        self.check_moves(grid)
        if self.state == "normal":
            self.chase(pac_x, pac_y)
        elif self.state == "scared":
            self.run(pac_x, pac_y)
        elif self.state == "scatter":
            self.scatter()
        # Portal teleport code.
        self.pos = self.velocity * self.speed + self.pos
        if self.x >= self.parent.map_l + 10:
            self.x = self.parent.x_marg
        if self.x <= self.parent.x_marg - 10:
            self.x = self.parent.map_l

    def scatter(self):
        # Paths blinky towards his respective corner.
        target_x = self.parent.map_l + self.parent.x_marg
        target_y = self.parent.map_h + self.parent.y_marg
        self.scatter_timer += -1
        if not self.scatter_timer:
            self.velocity = -self.velocity
            self.state = "normal"
            self.chase_timer = 500

        if self.last_move == "up" or self.last_move == "down":
            if target_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif target_x > self.center_x and self.m_right:
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
            if target_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif target_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def run(self, pac_x, pac_y):
        # Runs away from pac.
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

    def chase(self, pac_x, pac_y):
        # Chase pac's direct position.
        if not self.step == 3:
            self.chase_timer += -1
            if not self.chase_timer:
                self.step += 1
                self.state = "scatter"
                self.scatter_timer = 100
                self.velocity = -self.velocity
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
        # Check valid moves and stop if at wall.
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
                    self.x = self.x + self.x % 32
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

    def scared(self):
        # State change when pac is powered
        self.color = [0,0,1]
        self.state = "scared"
        self.velocity = -self.velocity

    def reset_color(self):
        # Resets state.
        self.state = "normal"
        self.color = [.82, .24, .09]
        self.velocity = -self.velocity
        if not self.scatter_timer:
            self.state = "normal"
        else:
            self.state = "scatter"


class Pinky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, 1)
    last_move = "right"
    timer = 600
    chase_timer = 0
    color = ListProperty([.86, .51, .89])
    state = "spawning"
    step = 0

    def setup(self, ate=0):
        self.pos = self.parent.x_marg + (32 * 9), self.parent.y_marg + (32 * 10)
        self.velocity = Vector(0,1)
        self.last_move = "right"
        if not ate:
            self.timer = 600
            self.step = 0
            self.state = "spawning"
        self.color = [.86, .51, .89]
        self.state = "spawning"

    def move(self, grid, pac_x, pac_y, pac_velocity):
        self.check_moves(grid)
        if self.state == "spawning":
            self.spawning()
        if self.state == "normal":
            self.chase(pac_x, pac_y, pac_velocity)
        elif self.state == "scared":
            self.run(pac_x, pac_y)
        elif self.state == "scatter":
            self.scatter()
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
            self.timer = 300
            self.state = "scatter"

    def scatter(self):
        target_x = self.parent.x_marg
        target_y = self.parent.map_h + self.parent.tile * 2
        self.timer += -1
        if not self.timer:
            self.velocity = -self.velocity
            self.chase_timer = 800
            self.state = "normal"

        if self.last_move == "up" or self.last_move == "down":
            if target_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif target_x > self.center_x and self.m_right:
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
            if target_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif target_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def chase(self, pac_x, pac_y, pac_velocity):
        if not self.step == 3:
            self.chase_timer += -1
            if not self.chase_timer:
                self.velocity = -self.velocity
                self.step += 1
                self.state = "scatter"
                self.timer = 300
        predict_x = pac_x + (self.parent.tile * pac_velocity.x * 4)
        predict_y = pac_y + (self.parent.tile * pac_velocity.y * 4)
        if self.last_move == "up" or self.last_move == "down":
            if predict_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif predict_x > self.center_x and self.m_right:
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
            if predict_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif predict_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def run(self, pac_x, pac_y):
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

    def scared(self):
        if not self.state == "spawning":
            self.state = "scared"
            self.velocity = -self.velocity
            self.color = [0, 0, 1]

    def reset_color(self):
        self.color = [.86, .51, .89]
        self.velocity = -self.velocity
        if not self.timer:
            self.state = "normal"
        else:
            self.state = "scatter"


class Clyde(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, -1)
    last_move = "horizontal"
    timer = 1400
    color = ListProperty([.86, .52, .11])
    state = "spawning"
    step = 0

    def setup(self, ate=0):
        self.pos = self.parent.x_marg + (32 * 10), self.parent.y_marg + (32 * 10)
        self.velocity = Vector(0,-1)
        self.last_move = "horizontal"
        if not ate:
            self.step = 0
            self.timer = 1400
        self.color = [.86, .51, .11]
        self.state = "spawning"

    def move(self, grid, pac_x, pac_y):
        self.check_moves(grid)
        if self.state == "scared":
            self.run(pac_x, pac_y)
        elif self.state == "spawning":
            self.spawning()
        elif abs(self.center_x - pac_x) + abs(self.center_y - pac_y) <= 8 * self.parent.tile:
            if not self.state == "scatter":
                self.velocity = -self.velocity
            self.state = "scatter"
            self.scatter()
        else:
            self.state = "normal"
            self.chase(pac_x, pac_y)

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
            self.timer = 300
            self.state = "scatter"

    def scatter(self):
        target_x = self.parent.x_marg + self.parent.tile * 2
        target_y = 0
        if self.last_move == "vertical":
            if target_x < self.center_x and self.m_left:
                self.velocity = Vector(-1, 0)
            elif target_x > self.center_x and self.m_right:
                self.last_move = "horizontal"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0, 0):
                if self.m_right:
                    self.last_move = "horizontal"
                    self.velocity = Vector(1, 0)
                elif self.m_left:
                    self.last_move = "horizontal"
                    self.velocity = Vector(-1, 0)

        elif self.last_move == "horizontal":
            if target_y < self.center_y and self.m_down:
                self.last_move = "vertical"
                self.velocity = Vector(0, -1)
            elif target_y > self.center_y and self.m_up:
                self.last_move = "vertical"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "vertical"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "vertical"
                    self.velocity = Vector(0, -1)

    def run(self, pac_x, pac_y):
        if self.last_move == "vertical":
            if pac_x > self.center_x and self.m_left:
                self.last_move = "horizontal"
                self.velocity = Vector(-1, 0)
            elif pac_x < self.center_x and self.m_right:
                self.last_move = "horizontal"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0, 0):
                if self.m_right:
                    self.last_move = "horizontal"
                    self.velocity = Vector(1, 0)
                elif self.m_left:
                    self.last_move = "horizontal"
                    self.velocity = Vector(-1, 0)

        elif self.last_move == "horizontal":
            if pac_y > self.center_y and self.m_down:
                self.last_move = "vertical"
                self.velocity = Vector(0, -1)
            elif pac_y < self.center_y and self.m_up:
                self.last_move = "vertical"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "vertical"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "vertical"
                    self.velocity = Vector(0, -1)

    def chase(self, pac_x, pac_y):
        if self.last_move == "vertical":
            if pac_x < self.center_x and self.m_left:
                self.last_move = "horizontal"
                self.velocity = Vector(-1, 0)
            elif pac_x > self.center_x and self.m_right:
                self.last_move = "horizontal"
                self.velocity = Vector(1, 0)
            elif self.velocity == Vector(0, 0):
                if self.m_right:
                    self.last_move = "horizontal"
                    self.velocity = Vector(1, 0)
                elif self.m_left:
                    self.last_move = "horizontal"
                    self.velocity = Vector(-1, 0)

        elif self.last_move == "horizontal":
            if pac_y < self.center_y and self.m_down:
                self.last_move = "vertical"
                self.velocity = Vector(0, -1)
            elif pac_y > self.center_y and self.m_up:
                self.last_move = "vertical"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "vertical"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "vertical"
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
        self.velocity = -self.velocity
        self.color = [.86, .51, .11]
        self.state = "normal"


class Inky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, -1)
    last_move = "right"
    timer = 1000
    chase_timer = 0
    color = ListProperty([.27, .74, .93])
    state = "spawning"
    step = 0

    def setup(self, ate=0):
        self.pos = self.parent.x_marg + (32 * 8), self.parent.y_marg + (32 * 10)
        self.velocity = Vector(0,-1)
        self.last_move = "right"
        if not ate:
            self.timer = 1000
            self.state = "spawning"
            self.step = 0
        self.state = "spawning"
        self.color = [.27, .74, .93]

    def move(self, grid, pac_x, pac_y):
        self.check_moves(grid)
        if self.state == "spawning":
            self.spawning()
        if self.state == "normal":
            self.chase(pac_x, pac_y)
        elif self.state == "scared":
            self.run(pac_x, pac_y)
        elif self.state == "scatter":
            self.scatter()
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= self.parent.map_l + 10:
            self.x = self.parent.x_marg
        if self.x <= self.parent.x_marg - 10:
            self.x = self.parent.map_l
        if self.y >= self.parent.map_h + 10:
            self.y = self.parent.y_marg
        if self.y <= self.parent.y_marg - 10:
            self.y = self.parent.map_h

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
            self.timer = 300
            self.state = "scatter"

    def scatter(self):
        target_x = self.parent.map_l + self.parent.tile * 2
        target_y = 0
        self.timer += -1
        if not self.timer:
            self.velocity = -self.velocity
            self.chase_timer = 800
            self.state = "normal"

        if self.last_move == "up" or self.last_move == "down":
            if target_x < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif target_x > self.center_x and self.m_right:
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
            if target_y < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif target_y > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def chase(self, pac_x, pac_y):
        if not self.step == 3:
            self.chase_timer += -1
            if not self.chase_timer:
                self.velocity = -self.velocity
                self.step += 1
                self.state = "scatter"
                self.timer = 300
        x_target = pac_x + abs(self.parent.blinky.center_x - pac_x) * 2
        y_target = pac_y + abs(self.parent.blinky.center_y - pac_y) * 2
        if self.last_move == "up" or self.last_move == "down":
            if x_target < self.center_x and self.m_left:
                self.last_move = "left"
                self.velocity = Vector(-1, 0)
            elif x_target> self.center_x and self.m_right:
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
            if y_target < self.center_y and self.m_down:
                self.last_move = "down"
                self.velocity = Vector(0, -1)
            elif y_target > self.center_y and self.m_up:
                self.last_move = "up"
                self.velocity = Vector(0, 1)
            elif self.velocity == Vector(0, 0):
                if self.m_up:
                    self.last_move = "up"
                    self.velocity = Vector(0, 1)
                elif self.m_down:
                    self.last_move = "down"
                    self.velocity = Vector(0, -1)

    def run(self, pac_x, pac_y):
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
        self.velocity = -self.velocity
        if not self.timer:
            self.state = "normal"
        else:
            self.state = "scatter"


class PacGame(Widget):
    pac = ObjectProperty(None)
    blinky = ObjectProperty(None)
    pinky = ObjectProperty(None)
    inky = ObjectProperty(None)
    clyde = ObjectProperty(None)
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
    power_timer = 0
    h_positions = []
    v_positions = []
    h_exclude_dots = []
    v_exclude_dots = []

    def __init__(self, **kwargs):
        # Initialize keyboards, build the level, populate grid then draw ready status.
        super(PacGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.build_level()
        self.status.text = "Ready?"
        self.redraw(self.status)
        self.redraw()
        self.fill_grid()
        Window.size = (self.map_l + self.x_marg * 2, self.map_h + self.y_marg * 2)

    def _keyboard_closed(self):
        # Unbind keyboard upon closing.
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # When a key is pressed we update pac's curr_key.
        self.pac.curr_key = keycode[1]
        if self.ready_check:        # If we are in ready check take us out when a key is pressed.
            self.ready_check = False

    def update(self, dt):
        # Main update loop of program.
        if not self.ready_check:    # If we aren't in ready check continue with normal game loop.
            if self.pac.dead:       # If pac is dead reset ghosts and pac.
                self.status.text = "You Died"
                self.redraw(self.status)
                self.death()
            elif not self.pac.dead: # If not dead update positions, clear status then check collisions.
                self.pac.update_pos(self.grid)
                if not self.status == '':
                    self.status.text = ''
                    self.redraw(self.status)
                self.move_ghosts()
                self.check_ghost_collision()
                self.check_dot_collision()
                if not self.dots and not self.super_dots:   # If no more dots then end the game.
                    self.win()

    def redraw(self, widget=None):
        # Method to redraw widgets to put them on top of the visual stack.
        # If we specify a widget only redraw it else redraw all main widgets.
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
        # Changes ghost states and sets powerup timer.
        # If we already are powered reset the timer.
        if self.powerup:
            Clock.unschedule(self.power_timer)
        self.blinky.scared()
        self.inky.scared()
        self.pinky.scared()
        self.clyde.scared()
        self.powerup = True
        self.power_timer = Clock.schedule_once(self.unpower, 5)

    def unpower(self, dt):
        # When timer runs out we reset any scared ghosts.
        self.blinky.reset_color()
        if self.inky.state == "scared":
            self.inky.reset_color()
        if self.clyde.state == "scared":
            self.clyde.reset_color()
        if self.pinky.state == "scared":
            self.pinky.reset_color()
        self.powerup = False

    def death(self):
        # Perform respawning unless player is out of lives.
        if self.pac.end_angle > 90 + self.pac.rotation:  # Death animation.
            self.pac.start_angle += 1
            self.pac.end_angle -= 1
        elif self.lives > 0:
            self.respawn_player()
        else:
            # Display game over status and wait for restart.
            self.status.text = "You Lose"
            self.status2.text = "Press Enter to Restart"
            if self.pac.curr_key == "enter":
                self.pac.dead = False
                self.respawn_player(True)
            self.redraw(self.status)
            self.redraw(self.status2)

    def move_ghosts(self):
        # Call all the movement methods for ghosts.
        if self.blinky.step == 3:   # When blinky finishes wave steps everyone else finishes.
            self.pinky.step = 3
            self.inky.step = 3
            self.clyde.step = 3
        self.blinky.move(self.grid, self.pac.center_x, self.pac.center_y)
        self.pinky.move(self.grid, self.pac.center_x, self.pac.center_y, self.pac.velocity)
        self.inky.move(self.grid, self.pac.center_x, self.pac.center_y)
        self.clyde.move(self.grid, self.pac.center_x, self.pac.center_y)

    def check_ghost_collision(self):
        # Determine if pac collides witha  ghost and decide what to do depending on their state.
        # If a ghost is scared we respawn it else we set pac's death state to true.
        if self.pac.collide_point(self.blinky.center_x, self.blinky.center_y):
            if self.blinky.state == "scared":
                self.blinky.setup(1)
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
        # Check for any dots we are eating and remove/cover them up with a black dot to hide them.
        # Then we redraw the widgets over the black dot and increment the score.
        for i in self.super_dots:
            if self.pac.collide_point(i[0] * self.tile + 8 + self.x_marg, i[1] * self.tile + 8 + self.y_marg):
                self.powered()
                with self.canvas:
                    Color(0, 0, 0)
                    Ellipse(pos=(i[0] * self.tile + 8 + self.x_marg, i[1] * self.tile + 8 + self.y_marg), size=(16, 16))
                self.score += 9
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
        if self.dots.__len__() < 60:    # If they're close to winning speedup blinky.
            self.blinky.step = 3
            self.blinky.speed = 2

    def respawn_player(self, restart=False):
        # Respawns the player and ghosts then perfroms ready check.
        # If restart is true perform all the resetting needed to start the game over again.
        # Setup each player, reset all counters, redraw dots, and set status and perform ready check.
        self.inky.setup()
        self.pinky.setup()
        self.clyde.setup()
        self.pac.setup()
        self.blinky.setup()
        if restart:
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
        # Display win status and wait for input to reset game.
        self.status.text = "You Win"
        self.status2.text = "Press Enter to Restart"
        self.ready_check = True
        self.redraw(self.status)
        self.redraw(self.status2)
        if self.pac.curr_key == "enter":
            self.pac.dead = False
            self.respawn_player(True)

    def get_positions(self):
        # Used later to pull in positions from files or other sources.
        # tracks that go outside of margins are treated as portals.
        # tracks must be placed according to standard pacman track placement
        # all tracks of same type must have a wall between them.
        self.h_positions = [(0, 0, 19), (0, 2, 5), (6, 2, 3), (10, 2, 3), (14, 2, 5), (0, 4, 3), (4, 4, 11), (16, 4, 3),
                            (0, 6, 9), (10, 6, 9), (6, 8, 7), (-1, 10, 8), (12, 10, 8), (6, 12, 7), (0, 14, 5),
                            (6, 14, 3), (10, 14, 3), (14, 14, 5), (0, 16, 19), (0, 19, 9), (10, 19, 9)]
        self.v_positions = [(0, 0, 3), (8, 0, 3), (10, 0, 3), (18, 0, 3), (2, 2, 3), (4, 2, 18), (6, 2, 3), (12, 2, 3),
                            (14, 2, 18), (16, 2, 3), (0, 4, 3), (8, 4, 3), (10, 4, 3), (18, 4, 3), (6, 6, 7),
                            (12, 6, 7), (8, 12, 3), (10, 12, 3), (0, 14, 6), (6, 14, 3), (12, 14, 3), (18, 14, 6),
                            (8, 16, 4), (10, 16, 4)]
        self.h_exclude_dots = [(-1, 10), (12, 10)]      # x,y position of h_track that shouldn't have dots
        self.v_exclude_dots = []                        # x,y position of v_track that shouldn't have dots
        self.super_dots = [(0, 1), (18, 1), (0, 18),
                           (18, 18)]    # positions of super dots

    def fill_grid(self):
        # Draw out the grid based on h_positions and v_positions.

        for i in self.h_positions:
            for j in range(i[2]):
                self.grid[i[0] + j][i[1]] = "h"

        for i in self.v_positions:
            for j in range(i[2]):
                if self.grid[i[0]][i[1]+j] == "h":
                    self.grid[i[0]][i[1]+j] = "hv"
                else:
                    self.grid[i[0]][i[1]+j] = "v"

    def build_level(self):
        # Draw the tracks then place dots on them as well as draw the ghost house.
        self.get_positions()
        for i in self.h_positions:
            with self.canvas:
                Color(0,0,0)
                Rectangle(pos=(self.x_marg + (self.tile * i[0]), self.y_marg + (self.tile * i[1])),
                          size=(i[2] * self.tile,self.tile))

        for i in self.v_positions:
            with self.canvas:
                Color(0,0,0)
                Rectangle(pos=(self.x_marg + (self.tile * i[0]), self.y_marg + (self.tile * i[1])),
                          size=(self.tile,self.tile * i[2]))

        self.draw_dots()
        with self.canvas:   # Draw ghost house / spawn room.
            Color(0, 0, 0)
            Rectangle(pos=(self.x_marg + (self.tile * 7) + 4, self.y_marg + (self.tile * 8) + 80 /2), size=(152, 80))
            Color(1, 1, 1)
            Rectangle(pos=(self.x_marg + (self.tile * 9)- 4, self.y_marg + (self.tile * 12) - 8), size=(40, 8))

    def draw_dots(self):
        # Draw the dots in each tile along valid tracks.
        for p in self.h_positions:
            y_dot = (p[1] * self.tile) + (self.tile / 2) - 4 + self.y_marg
            x_dot = (p[0] * self.tile) + (self.tile / 2) - 4 + self.x_marg
            for e in self.h_exclude_dots:
                ey_dot = (e[1] * self.tile) + (self.tile / 2) - 4 + self.y_marg
                ex_dot = (e[0] * self.tile) + (self.tile / 2) - 4 + self.x_marg
                if x_dot == ex_dot and y_dot == ey_dot:
                    x_dot += self.tile * p[2]
                    break

            for i in range(p[2]):
                # check to not draw dots around spawn area or excluded positions
                if x_dot <= self.x_marg or x_dot >= self.map_l + self.x_marg:  # makes sure no dots are drawn outside of the map
                    x_dot += self.x_marg

                elif x_dot < (self.tile * 5) + self.x_marg or x_dot > (self.tile * 14) + self.x_marg or\
                        y_dot < (self.tile * 7) + self.y_marg or y_dot > (self.tile * 14) + self.y_marg:

                        with self.canvas:
                            Color(244, 244, 230)
                            Ellipse(pos=(x_dot, y_dot), size=(8, 8))
                            self.dots.append((x_dot, y_dot))
                            x_dot += self.tile
                else:
                    x_dot += self.tile

        for p in self.v_positions:
            y_dot = (p[1] * self.tile) + (self.tile / 2) - 4 + self.y_marg
            x_dot = (p[0] * self.tile) + (self.tile / 2) - 4 + self.x_marg

            for e in self.v_exclude_dots:
                ey_dot = (e[1] * self.tile) + (self.tile / 2) - 4 + self.y_marg
                ex_dot = (e[0] * self.tile) + (self.tile / 2) - 4 + self.x_marg
                if x_dot == ex_dot and y_dot == ey_dot:
                    x_dot += self.tile * p[2]
                    break

            for i in range(p[2]):
                if y_dot <= self.y_marg or y_dot >= self.y_marg + self.map_h:  # check to not draw outside of map
                    y_dot += self.tile

                # check to not draw dots around spawn
                elif (x_dot, y_dot) not in self.dots and x_dot < (self.tile * 5) + self.x_marg or\
                        x_dot > (self.tile * 14) + self.x_marg or y_dot < (self.tile * 7) + self.y_marg or\
                        y_dot > (self.tile * 14) + self.y_marg:
                        with self.canvas:
                            Color(244, 244, 230)
                            Ellipse(pos=(x_dot, y_dot), size=(8, 8))
                            self.dots.append((x_dot, y_dot))
                            y_dot += self.tile
                else:
                    y_dot += self.tile

        # draw super dots
        for i in self.super_dots:
            if (i[0] * self.tile + (self.tile / 2) - 4 + self.x_marg, i[1] * self.tile + (self.tile / 2) - 4 + self.y_marg) not in self.dots:
                print('Super Dot position ' + str((i[0], i[1])) + ' is not allowed.')
            else:
                self.dots.remove((i[0] * self.tile + (self.tile / 2) - 4 + self.x_marg, i[1] * self.tile + (self.tile / 2) - 4 + self.y_marg))
                with self.canvas:
                    Color(244, 244, 230)
                    Ellipse(pos=(i[0] * self.tile + 8 + self.x_marg, i[1] * self.tile + 8 + self.y_marg), size=(16, 16))


class PacmanApp(App):
    def build(self):
        # ordering for game initialization
        game = PacGame()
        Window.top = 100  # Set top position of window.
        Clock.schedule_interval(game.update, 1/60)  # Update speed for game loop.
        return game


if __name__ == '__main__':
    PacmanApp().run()
