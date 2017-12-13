from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse


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

    def change_direction(self, h_tracks, v_tracks):
        self.horizontal = False
        self.vertical = False
        for t in h_tracks:
            if t.y == self.y and t.right >= self.x >= t.x:
                self.horizontal = True
        for t in v_tracks:
            if t.x == self.x and t.top >= self.y >= t.y:
                self.vertical = True
        if self.curr_key == 'right' and self.horizontal:
            self.rotate(180)
            self.velocity = Vector(1, 0)
        elif self.curr_key == 'left' and self.horizontal:
            self.rotate(0)
            self.velocity = Vector(-1, 0)
        elif self.curr_key == 'up' and self.vertical:
            self.rotate(90)
            self.velocity = Vector(0, 1)
        elif self.curr_key == 'down' and self.vertical:
            self.rotate(-90)
            self.velocity = Vector(0, -1)

    def check_walls(self, h_tracks, v_tracks):
        if self.velocity.x:
            for t in h_tracks:
                if t.collide_widget(self):
                    if t.center_x + (self.velocity.x * t.width/2) == self.center_x + (self.velocity.x * 16):
                        self.velocity.x = 0
                    break
        if self.velocity.y:
            for t in v_tracks:
                if t.collide_widget(self):
                    if t.center_y + (self.velocity.y * t.height/2) == self.center_y + (self.velocity.y * 16):
                        self.velocity.y = 0
                    break

    def update_pos(self, h_tracks, v_tracks):
        self.change_direction(h_tracks, v_tracks)
        self.check_walls(h_tracks, v_tracks)
        self.pos = (self.velocity * self.speed) + self.pos

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
    length = NumericProperty(600)


class TrackV(Widget):
    length = NumericProperty(200)


class Ghost(Widget):
    velocity_x = NumericProperty(4)
    velocity_y = NumericProperty(0)
    speed = NumericProperty(4)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        if self.x > 800:
            self.x = 0
        if self.x < 0:
            self.x = 800
        if self.y <= 0:
            self.y = 600
        if self.y > 600:
            self.y = 0
        if self.center_x + 32 > 800:
            self.velocity.velocity_x = self.velocity
        elif self.center_x < 0:
            self.velocity.velocity_x = self.speed
        self.pos = Vector(self.velocity) + self.pos


class PacGame(Widget):
    pac = ObjectProperty(None)
    ghost = ObjectProperty(None)
    track1H = ObjectProperty(None)
    track1V = ObjectProperty(None)
    track2V = ObjectProperty(None)
    track2H = ObjectProperty(None)
    track3H = ObjectProperty(None)
    h_tracks = ListProperty()
    v_tracks = ListProperty()

    def __init__(self, **kwargs):
        super(PacGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.track2H.length = 270
        self.track3H.length = 270
        self.h_tracks = [self.track1H, self.track2H, self.track3H]
        self.v_tracks = [self.track1V, self.track2V]

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.pac.curr_key = keycode[1]

    def update(self, dt):
        if not self.pac.dead:
            self.ghost.move()
            if self.pac.collide_widget(self.ghost):
                self.pac.speed = 0
                self.pac.dead = True
            self.pac.update_pos(self.h_tracks, self.v_tracks)
        else:
            self.pac.death()

    def draw_dots(self):
        with self.canvas:
            Color(244,244,230)
            Ellipse(pos=(100, 300), size=(10,10))


class PacmanApp(App):
    def build(self):
        # ordering for game initialization
        game = PacGame()
        Clock.schedule_interval(game.update, 1.0/60)
        return game

if __name__ == '__main__':
    PacmanApp().run()
