from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty, StringProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle


class Pac(Widget):
    speed = 2
    velocity = Vector(0, 0)
    rotation = 0
    start_angle = NumericProperty(-50)  # -90 = closed mouth
    end_angle = NumericProperty(230)    # 270 = closed mouth
    dead = False
    curr_key = ''
    horizontal = False
    vertical = False
    m_right = False
    m_left = False
    m_up = False
    m_down = False
    chomp_down = True

    def setup(self):
        self.pos = 40 + (32 * 9), 60 + (32 * 4)
        self.dead = False
        self.rotation = 0
        self.curr_key = ''
        self.start_angle = -50
        self.end_angle = 230
        self.velocity = Vector(0,0)

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
        self.chomp()

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
    make_move = False

    def setup(self):
        self.pos = 40 + (32 * 9), 60 + (32 * 12)
        self.velocity = Vector(1,0)

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

    def setup(self):
        self.pos = 40 + (32 * 9), 60 + (32 * 10)
        self.velocity = Vector(0,1)
        self.timer = 400

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

    def setup(self):
        self.pos = 40 + (32 * 10), 60 + (32 * 10)
        self.velocity = Vector(0,-1)
        self.timer = 800

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

    def setup(self):
        self.pos = 40 + (32 * 8), 60 + (32 * 10)
        self.velocity = Vector(0,-1)
        self.timer = 600

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
    lives = NumericProperty(3)
    status = ObjectProperty()
    status2 = ObjectProperty()
    ready_check = True

    def __init__(self, **kwargs):
        super(PacGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.build_level()
        self.status.text = "Ready?"
        self.redraw(self.status)
        self.redraw()

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
                self.status.text = ''
                self.redraw(self.status)
                self.move_ghosts()
                if self.pac.collide_point(self.blinky.center_x, self.blinky.center_y) or\
                        self.pac.collide_point(self.pinky.center_x, self.pinky.center_y) or\
                        self.pac.collide_point(self.clyde.center_x, self.clyde.center_y) or\
                        self.pac.collide_point(self.inky.center_x, self.inky.center_y):
                    self.pac.dead = True
                    self.lives += -1
                else:
                    for i in self.dots:
                        if self.pac.collide_point(i[0],i[1]):
                            self.score += 1
                            self.dots.remove(i)
                            with self.canvas:
                                Color(0, 0, 0)
                                Ellipse(pos=(i[0], i[1]), size=(8, 8))
                            self.redraw()
                    self.pac.update_pos(self.h_tracks, self.v_tracks)
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

    def move_ghosts(self):
        self.blinky.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)
        self.pinky.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)
        self.inky.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)
        self.clyde.move(self.h_tracks, self.v_tracks, self.pac.center_x, self.pac.center_y)

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
        x_marg = 40  # margin size for sides of window
        y_marg = 60  # margin size for top and bottom
        map_l = 608  # length of map
        map_h = 640  # height of map
        tile = 32  # size of tile
        # h_positions = (#tiles x, #tiles y, #tiles length)
        h_positions = [(0,0,19), (0,2,5), (6,2,3), (10,2,3), (14,2,5), (0,4,3), (4,4,11), (16,4,3), (0,6,9), (10,6,9),
                       (6,8,7), (-1,10,8), (12,10,8), (6,12,7), (0,14,5), (6,14,3), (10,14,3), (14,14,5), (0,16,19),
                       (0,19,9), (10,19,9)]
        v_positions = [(0,0,3),(8,0,3),(10,0,3),(18,0,3),(2,2,3),(4,2,18),(6,2,3),(12,2,3),(14,2,18),(16,2,3), (0,4,3),
                      (8,4,3),(10,4,3),(18,4,3),(6,6,7), (12,6,7), (8,12,3),(10,12,3),(0,14,6),(6,14,3),(12,14,3),
                                                          (18,14,6), (8,16,4), (10,16,4)]

        for i in h_positions:
            # self.h_tracks.append(TrackH(Color=(1,1,1,1),pos=(x_marg + (tile * i[0]), y_marg + (tile * i[1]))))
            track = TrackH(Color=(1,1,1,1),pos=(x_marg + (tile * i[0]), y_marg + (tile * i[1])))
            track.length = i[2] * tile
            self.h_tracks.append(track)
            self.add_widget(track)

        for i in v_positions:
            track = TrackV(Color=(1, 1, 1, 1), pos=(x_marg + (tile * i[0]), y_marg + (tile * i[1])))
            track.length = i[2] * tile
            self.v_tracks.append(track)
            self.add_widget(track)
        self.draw_dots()

        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(269, 355), size=(150, 80))
            Color(1, 1, 1)
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
        Window.top = 100
        Clock.schedule_interval(game.update, 20/60)
        return game

if __name__ == '__main__':
    PacmanApp().run()
