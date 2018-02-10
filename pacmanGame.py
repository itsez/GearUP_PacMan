from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle


class Pac(Widget):
    speed = 2
    velocity = Vector(0, 0)
    start_angle = NumericProperty(-50)  # -90 = closed mouth
    end_angle = NumericProperty(230)    # 270 = closed mouth
    bite_down = 1
    bite_speed = 1.5
    rotation = 0
    dead = False
    curr_key = ''
    horizontal = False
    vertical = False
    m_right = False
    m_left = False
    m_up = False
    m_down = False

    def change_direction(self, h_tracks, v_tracks):

        self.check_moves(h_tracks, v_tracks)
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

    def check_moves(self, h_tracks, v_tracks):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        for t in h_tracks:
            if t.y == self.y:
                if t.y == self.y and t.right >= self.x >= t.x:
                    self.m_right = True
                    self.m_left = True
                    if self.x == t.x:
                        self.m_left = False
                    if self.right == t.right:
                        self.m_right = False
                    if t.center_x + (self.velocity.x * t.width/2) == self.center_x + (self.velocity.x * 16):
                        self.velocity.x = 0
                    break

        for t in v_tracks:
            if t.x == self.x:
                if t.x == self.x and t.top >= self.y >= t.y:
                    self.m_down = True
                    self.m_up = True
                    if t.top == self.top:
                        self.m_up = False
                    if self.y == t.y:
                        self.m_down = False
                    if t.center_y + (self.velocity.y * t.height/2) == self.center_y + (self.velocity.y * 16):
                        self.velocity.y = 0
                    break

    def update_pos(self, h_tracks, v_tracks):
        self.change_direction(h_tracks, v_tracks)
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= 640:
            self.x = 40
            self.rotate(180)
            self.velocity.x = -self.velocity.x

        if self.x <= 8:
            self.x = 608
            self.rotate(180)
            self.velocity.x = -self.velocity.x

    def chomp(self):
        # TODO
        pass

    def rotate(self, val):
        self.rotation = val
        self.start_angle = -50 + val
        self.end_angle = 230 + val

    def death(self):
        if self.end_angle > 90 + self.rotation:
            self.start_angle += 1
            self.end_angle -= 1


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
    make_move = False

    def move(self, h_tracks, v_tracks, pac_x, pac_y):
        self.choose_move(h_tracks, v_tracks, pac_x, pac_y)
        self.pos = self.velocity * self.speed + self.pos
        if self.x >= 640:
            self.x = 40
        if self.x <= 8:
            self.x = 608

    def choose_move(self, h_tracks, v_tracks, pac_x, pac_y):
        self.check_moves(h_tracks, v_tracks)

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

    def check_moves(self, h_tracks, v_tracks):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        for t in h_tracks:
            if t.y == self.y:
                if t.y == self.y and t.right >= self.x >= t.x:
                    self.m_right = True
                    self.m_left = True
                    if self.x == t.x:
                        self.m_left = False
                    if self.right == t.right:
                        self.m_right = False
                    if t.center_x + (self.velocity.x * t.width/2) == self.center_x + (self.velocity.x * 16):
                        self.velocity.x = 0
                    break
        for t in v_tracks:
            if t.x == self.x:
                if t.x == self.x and t.top >= self.y >= t.y:
                    self.m_down = True
                    self.m_up = True
                    if t.top == self.top:
                        self.m_up = False
                    if self.y == t.y:
                        self.m_down = False
                    if t.center_y + (self.velocity.y * t.height/2) == self.center_y + (self.velocity.y * 16):
                        self.velocity.y = 0
                    break


class Pinky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, 1)
    last_move = "up"
    make_move = False
    timer = 400

    def move(self, h_tracks, v_tracks, pac_x, pac_y):
        if self.timer > 0:
            self.spawning()
        else:
            self.choose_move(h_tracks, v_tracks, pac_x, pac_y)
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= 640:
            self.x = 40
        if self.x <= 8:
            self.x = 608

    def spawning(self):
        self.timer += -1
        if self.top > 60 + (32 * 12):
            self.velocity = Vector(0, -1)
        elif self.y < 60 + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.timer < 120:
            self.velocity = Vector(0,1)
        if self.y >= 60 + (32 * 12):
            self.velocity = Vector(1, 0)
            self.timer = 0

    def choose_move(self, h_tracks, v_tracks, pac_x, pac_y):
        self.check_moves(h_tracks, v_tracks)

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

    def check_moves(self, h_tracks, v_tracks):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        for t in h_tracks:
            if t.y == self.y:
                if t.y == self.y and t.right >= self.x >= t.x:
                    self.m_right = True
                    self.m_left = True
                    if self.x == t.x:
                        self.m_left = False
                    if self.right == t.right:
                        self.m_right = False
                    if t.center_x + (self.velocity.x * t.width/2) == self.center_x + (self.velocity.x * 16):
                        self.velocity.x = 0
                    break
        for t in v_tracks:
            if t.x == self.x:
                if t.x == self.x and t.top >= self.y >= t.y:
                    self.m_down = True
                    self.m_up = True
                    if t.top == self.top:
                        self.m_up = False
                    if self.y == t.y:
                        self.m_down = False
                    if t.center_y + (self.velocity.y * t.height/2) == self.center_y + (self.velocity.y * 16):
                        self.velocity.y = 0
                    break


class Clyde(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, -1)
    last_move = "up"
    make_move = False
    timer = 800

    def move(self, h_tracks, v_tracks, pac_x, pac_y):
        if self.timer > 0:
            self.spawning()
        else:
            self.choose_move(h_tracks, v_tracks, pac_x, pac_y)
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= 640:
            self.x = 40
        if self.x <= 8:
            self.x = 608

    def spawning(self):
        self.timer += -1
        if self.top > 60 + (32 * 12):
            self.velocity = Vector(0, -1)
        elif self.y < 60 + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.timer < 120:
            self.velocity = Vector(-1, 0)
        if self.x == 40 + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.y >= 60 + (32 * 12):
            self.velocity = Vector(1, 0)

    def choose_move(self, h_tracks, v_tracks, pac_x, pac_y):
        self.check_moves(h_tracks, v_tracks)
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

    def check_moves(self, h_tracks, v_tracks):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        for t in h_tracks:
            if t.y == self.y:
                if t.y == self.y and t.right >= self.x >= t.x:
                    self.m_right = True
                    self.m_left = True
                    if self.x == t.x:
                        self.m_left = False
                    if self.right == t.right:
                        self.m_right = False
                    if t.center_x + (self.velocity.x * t.width/2) == self.center_x + (self.velocity.x * 16):
                        self.velocity.x = 0
                    break
        for t in v_tracks:
            if t.x == self.x:
                if t.x == self.x and t.top >= self.y >= t.y:
                    self.m_down = True
                    self.m_up = True
                    if t.top == self.top:
                        self.m_up = False
                    if self.y == t.y:
                        self.m_down = False
                    if t.center_y + (self.velocity.y * t.height/2) == self.center_y + (self.velocity.y * 16):
                        self.velocity.y = 0
                    break


class Inky(Widget):
    m_left = False
    m_right = False
    m_up = False
    m_down = False
    speed = NumericProperty(1)
    velocity = Vector(0, -1)
    last_move = "up"
    make_move = False
    timer = 600

    def move(self, h_tracks, v_tracks, pac_x, pac_y):
        if self.timer > 0:
            self.spawning()
        else:
            self.choose_move(h_tracks, v_tracks, pac_x, pac_y)
        self.pos = (self.velocity * self.speed) + self.pos
        if self.x >= 640:
            self.x = 40
        if self.x <= 8:
            self.x = 608

    def spawning(self):
        self.timer += -1
        if self.top > 60 + (32 * 12):
            self.velocity = Vector(0, -1)
        elif self.y < 60 + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.timer < 120:
            self.velocity = Vector(1, 0)
        if self.x == 40 + (32 * 9):
            self.velocity = Vector(0, 1)
        if self.y >= 60 + (32 * 12):
            self.velocity = Vector(1, 0)

    def choose_move(self, h_tracks, v_tracks, pac_x, pac_y):
        self.check_moves(h_tracks, v_tracks)

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

    def check_moves(self, h_tracks, v_tracks):
        self.m_down = False
        self.m_up = False
        self.m_left = False
        self.m_right = False

        for t in h_tracks:
            if t.y == self.y:
                if t.y == self.y and t.right >= self.x >= t.x:
                    self.m_right = True
                    self.m_left = True
                    if self.x == t.x:
                        self.m_left = False
                    if self.right == t.right:
                        self.m_right = False
                    if t.center_x + (self.velocity.x * t.width/2) == self.center_x + (self.velocity.x * 16):
                        self.velocity.x = 0
                    break
        for t in v_tracks:
            if t.x == self.x:
                if t.x == self.x and t.top >= self.y >= t.y:
                    self.m_down = True
                    self.m_up = True
                    if t.top == self.top:
                        self.m_up = False
                    if self.y == t.y:
                        self.m_down = False
                    if t.center_y + (self.velocity.y * t.height/2) == self.center_y + (self.velocity.y * 16):
                        self.velocity.y = 0
                    break


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

    def __init__(self, **kwargs):
        super(PacGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.build_level()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.pac.curr_key = keycode[1]

    def update(self, dt):
        if not self.pac.dead:
            self.blinky.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)
            self.pinky.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)
            self.inky.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)
            self.clyde.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)
            if self.pac.collide_point(self.blinky.center_x, self.blinky.center_y) or\
                    self.pac.collide_point(self.pinky.center_x, self.pinky.center_y) or\
                    self.pac.collide_point(self.clyde.center_x, self.clyde.center_y) or\
                    self.pac.collide_point(self.inky.center_x, self.inky.center_y):
                self.pac.speed = 0
                self.pac.dead = True
            for i in self.dots:
                if self.pac.collide_point(i[0],i[1]):
                    self.score += 1
                    self.dots.remove(i)
                    with self.canvas:
                        Color(0, 0, 0)
                        Ellipse(pos=(i[0], i[1]), size=(8, 8))
                    self.remove_widget(self.pac)
                    self.add_widget(self.pac)
                    self.remove_widget(self.blinky)
                    self.add_widget(self.blinky)
                    self.remove_widget(self.pinky)
                    self.add_widget(self.pinky)
                    self.remove_widget(self.inky)
                    self.add_widget(self.inky)
                    self.remove_widget(self.clyde)
                    self.add_widget(self.clyde)

                    if not self.dots:
                        self.win()

            self.pac.update_pos(self.h_tracks, self.v_tracks)
        else:
            self.pac.death()

    def win(self):
        self.pac.speed = 0
        self.blinky.speed = 0
        self.pinky.speed = 0
        self.inky.speed = 0
        self.clyde.speed = 0

    def build_level(self):
        x_marg = 40  # margin size for sides of window
        y_marg = 60  # margin size for top and bottom
        map_l = 608  # length of map
        map_h = 640  # height of map
        tile = 32    # size of tile

        self.track1H.pos = (x_marg, y_marg)
        self.track2H.pos = (x_marg, y_marg + (tile * 2))
        self.track3H.pos = (x_marg + (tile * 6), y_marg + (2 * tile))
        self.track4H.pos = (x_marg + (tile * 10), y_marg + (tile * 2))
        self.track5H.pos = (x_marg + map_l - (tile * 5), y_marg + (2 * tile))
        self.track6H.pos = (x_marg, y_marg + (4 * tile))
        self.track7H.pos = (x_marg + (tile * 4), y_marg + (4 * tile))
        self.track8H.pos = (x_marg + map_l - (tile * 3), y_marg + (4 * tile))
        self.track9H.pos = (x_marg, y_marg + (tile * 6))
        self.track10H.pos = (x_marg + (tile * 10), y_marg + (tile * 6))
        self.track11H.pos = (x_marg + (tile * 6), y_marg + (tile * 8))
        self.track12H.pos = (0, y_marg + (tile * 10))
        self.track13H.pos = (x_marg + (tile * 12), y_marg + (tile * 10))
        self.track14H.pos = (x_marg + (tile * 6), y_marg + (tile * 12))
        self.track15H.pos = (x_marg,y_marg + (tile * 14))
        self.track16H.pos = (x_marg + (tile * 6), y_marg + (tile * 14))
        self.track17H.pos = (x_marg + (tile * 10), y_marg + (tile * 14))
        self.track18H.pos = (x_marg + (tile * 14), y_marg + (tile * 14))
        self.track19H.pos = (x_marg, y_marg + (tile * 16))
        self.track20H.pos = (x_marg, y_marg + map_h - tile)
        self.track21H.pos = (x_marg + (tile * 10), y_marg + map_h - tile)
        self.track1H.length = map_l
        self.track2H.length = 5 * tile
        self.track3H.length = 3 * tile
        self.track4H.length = 3 * tile
        self.track5H.length = 5 * tile
        self.track6H.length = 3 * tile
        self.track7H.length = 11 * tile
        self.track8H.length = 3 * tile
        self.track9H.length = 9 * tile
        self.track10H.length = 9 * tile
        self.track11H.length = 7 * tile
        self.track12H.length = 7 * tile + x_marg
        self.track13H.length = 7 * tile + x_marg
        self.track14H.length = 7 * tile
        self.track15H.length = 5 * tile
        self.track16H.length = 3 * tile
        self.track17H.length = 3 * tile
        self.track18H.length = 5 * tile
        self.track19H.length = map_l
        self.track20H.length = 9 * tile
        self.track21H.length = 9 * tile

        self.track1V.pos = (x_marg, y_marg)
        self.track2V.pos = (x_marg + (tile * 8), y_marg)
        self.track3V.pos = (x_marg + (tile * 10), y_marg)
        self.track4V.pos = (x_marg + map_l - tile, y_marg)
        self.track5V.pos = (x_marg + (tile * 2), y_marg + (tile * 2))
        self.track6V.pos = (x_marg + (tile * 4), y_marg + (tile * 2))
        self.track7V.pos = (x_marg + (tile * 6), y_marg + (tile * 2))
        self.track8V.pos = (x_marg + (tile * 12), y_marg + (tile * 2))
        self.track9V.pos = (x_marg + (tile * 14), y_marg + (tile * 2))
        self.track10V.pos = (x_marg + map_l - (3 * tile), y_marg + (tile * 2))
        self.track11V.pos = (x_marg, y_marg + (tile * 4))
        self.track12V.pos = (x_marg + (tile * 8), y_marg + (tile * 4))
        self.track13V.pos = (x_marg + (tile * 10), y_marg + (tile * 4))
        self.track14V.pos = (x_marg + map_l - tile, y_marg + (tile * 4))
        self.track15V.pos = (x_marg + (tile * 6), y_marg + (tile * 6))
        self.track16V.pos = (x_marg + (tile * 12), y_marg + (tile * 6))
        self.track17V.pos = (x_marg + (tile * 8), y_marg + (tile * 12))
        self.track18V.pos = (x_marg + (tile * 10), y_marg + (tile * 12))
        self.track19V.pos = (x_marg, y_marg + (tile * 14))
        self.track20V.pos = (x_marg + (tile * 6), y_marg + (tile * 14))
        self.track21V.pos = (x_marg + (tile * 12), y_marg + (tile * 14))
        self.track22V.pos = (x_marg + map_l - tile,y_marg + (tile * 14))
        self.track23V.pos = (x_marg + (tile * 8), y_marg + map_h - (tile * 4))
        self.track24V.pos = (x_marg + (tile * 10), y_marg + map_h - (tile * 4))
        self.track1V.length = 3 * tile
        self.track2V.length = 3 * tile
        self.track3V.length = 3 * tile
        self.track4V.length = 3 * tile
        self.track5V.length = 3 * tile
        self.track6V.length = 18 * tile
        self.track7V.length = 3 * tile
        self.track8V.length = 3 * tile
        self.track9V.length = 18 * tile
        self.track10V.length = 3 * tile
        self.track11V.length = 3 * tile
        self.track12V.length = 3 * tile
        self.track13V.length = 3 * tile
        self.track14V.length = 3 * tile
        self.track15V.length = 7 * tile
        self.track16V.length = 7 * tile
        self.track17V.length = 3 * tile
        self.track18V.length = 3 * tile
        self.track19V.length = 6 * tile
        self.track20V.length = 3 * tile
        self.track21V.length = 3 * tile
        self.track22V.length = 6 * tile
        self.track23V.length = 4 * tile
        self.track24V.length = 4 * tile

        self.h_tracks = [self.track1H, self.track2H, self.track3H, self.track4H, self.track5H,self.track6H,
                         self.track7H, self.track8H, self.track9H, self.track10H, self.track11H, self.track12H,
                         self.track13H, self.track14H, self.track15H, self.track16H, self.track17H, self.track18H,
                         self.track19H, self.track20H, self.track21H]
        self.v_tracks = [self.track1V, self.track2V, self.track3V, self.track4V, self.track5V, self.track6V,
                         self.track7V, self.track8V, self.track9V, self.track10V, self.track11V, self.track12V,
                         self.track13V, self.track14V, self.track15V, self.track16V, self.track17V, self.track18V,
                         self.track19V, self.track20V, self.track21V, self.track22V, self.track23V, self.track24V]
        self.draw_dots()

        with self.canvas:
            Color(0,0,0)
            Rectangle(pos=(269, 355), size=(150, 80))
            Color(1,1,1)
            Rectangle(pos=(325, 435), size=(40, 8))

    def draw_dots(self):
        tile = 32    # size of tile
        x_marg = 40
        y_marg = 60
        for t in self.h_tracks:
            y_dot = t.center_y - 4
            x_dot = t.x + (tile / 2) - 4
            if x_dot < x_marg:                                          # makes sure left portal doesn't have dots
                x_dot += x_marg
            for i in range(t.width / tile):
                # check to not draw dots around spawn area or portal tracks
                if t.y == y_marg + (tile * 10):
                    break
                if x_dot < (tile * 5) + x_marg or x_dot > (tile * 14) + x_marg or\
                                y_dot < (tile * 8) + y_marg or y_dot > (tile * 14) + y_marg:
                        with self.canvas:
                            Color(244, 244, 230)
                            Ellipse(pos=(x_dot, y_dot), size=(8, 8))
                            self.dots.append((x_dot, y_dot))
                            x_dot += tile
                            if x_dot > 640 or x_dot > t.right:          # keeps the portals from misplacing dots
                                break
                else:
                    x_dot += tile

        for t in self.v_tracks:
            y_dot = t.y + (tile/2) - 4
            x_dot = t.center_x - 4
            for i in range(t.height / tile):
                # check to not draw dots around spawn
                if y_dot not in self.dots[1] and y_dot < (tile * 7) + y_marg or y_dot > (tile * 14) + y_marg or\
                                x_dot < (tile * 5) + x_marg or x_dot > (tile * 14) + x_marg:
                        with self.canvas:
                            Color(244, 244, 230)
                            Ellipse(pos=(x_dot, y_dot), size=(8, 8))
                            self.dots.append((x_dot, y_dot))
                            y_dot += tile
                else:
                    y_dot += tile


class PacmanApp(App):
    def build(self):
        # ordering for game initialization
        game = PacGame()
        Window.size = (720, 840)
        Clock.schedule_interval(game.update, 20/60)
        return game

if __name__ == '__main__':
    PacmanApp().run()
