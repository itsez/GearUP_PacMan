from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse


class Pac(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    speed = NumericProperty(4)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    start_angle = NumericProperty(-50)  #-90 = closed mouth
    end_angle = NumericProperty(230)    # 270 = closed mouth
    bite_down = 1
    bite_speed = 1.5
    rotation = 0
    dead = False
    curr_key = ''
    horizontal = False
    vertical = False

    def move(self,keycode='up'):
        if not self.dead:
            if keycode[1] == 'up' and self.vertical:
                self.velocity_y = self.speed
                self.velocity_x = 0
                self.rotate(90)
            if keycode[1] == 'down' and self.vertical:
                self.velocity_y = self.speed * -1
                self.velocity_x = 0
                self.rotate(-90)
            if keycode[1] == 'left' and self.horizontal:
                self.velocity_x = self.speed * -1
                self.velocity_y = 0
                self.rotate(0)
            if keycode[1] == 'right' and self.horizontal:
                self.velocity_x = self.speed
                self.velocity_y = 0
                self.rotate(180)

    def update_pos(self):
        if self.x > 800:
            self.x = 0
        if self.x < 0:
            self.x = 800
        if self.y <= 0:
            self.y = 600
        if self.y > 600:
            self.y = 0
        self.chomp()
        self.pos = Vector(self.velocity) + self.pos

    def chomp(self):
        if not self.dead:
            if self.bite_down == 1:
                self.end_angle += self.bite_speed
                self.start_angle += -self.bite_speed
                if self.end_angle >= 270 + self.rotation:
                    self.bite_down = 0
            else:
                self.end_angle += -self.bite_speed
                self.start_angle += self.bite_speed
                if self.end_angle <= 230 + self.rotation:
                    self.bite_down = 1

    def rotate(self, val):
        self.rotation = val
        self.start_angle = -50 + val
        self.end_angle = 230 + val

    def death(self):
        if self.end_angle > 90 + self.rotation:
            self.start_angle += 1
            self.end_angle -= 1


class TrackH(Widget):
    color = 0,0,0


class TrackV(Widget):
    color = 0


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
        if self.center_x + 30 > 800:
            self.velocity.velocity_x = self.velocity
        elif self.center_x < 0:
            self.velocity.velocity_x = self.speed
        self.pos = Vector(self.velocity) + self.pos


class PacGame(Widget):
    pac = ObjectProperty(None)
    ghost = ObjectProperty(None)
    track1H = ObjectProperty(None)
    track1V = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PacGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.draw_dots()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.pac.move(keycode)

    def update(self, dt):
        if not self.pac.dead:
            self.pac.update_pos()
            self.ghost.move()
            if self.pac.collide_widget(self.ghost):
                self.pac.speed = 0
                self.pac.dead = True
            if self.pac.collide_widget(self.track1H):
                self.pac.horizontal = True
                if not self.pac.vertical:
                    self.pac.y = self.track1H.y
            else:
                self.pac.horizontal = False
            if self.pac.collide_widget(self.track1V):
                self.pac.vertical = True
                if not self.pac.horizontal:
                    self.pac.x = self.track1V.x
            else:
                self.pac.vertical = False
        else:
            self.pac.death()

    def draw_dots(self):
        with self.canvas:
            Color(244,244,230)
            Ellipse(pos=(100, 300), size=(10,10))


class PacmanApp(App):
    def build(self):
        # ordering for game initilization
        game = PacGame()
        Clock.schedule_interval(game.update, 1.0/60)
        return game

if __name__ == '__main__':
    PacmanApp().run()