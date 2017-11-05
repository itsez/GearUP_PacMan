from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock


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

    def move(self,keycode='up'):
        if keycode[1] == 'up':
            self.velocity_y = self.speed
            self.velocity_x = 0
        if keycode[1] == 'down':
            self.velocity_y = self.speed * -1
            self.velocity_x = 0
        if keycode[1] == 'left':
            self.velocity_x = self.speed * -1
            self.velocity_y = 0
        if keycode[1] == 'right':
            self.velocity_x = self.speed
            self.velocity_y = 0
        self.pos = Vector(self.velocity) + self.pos

    def chomp(self):
        if self.bite_down == 1:
            self.end_angle += self.bite_speed
            self.start_angle += -self.bite_speed
            if self.end_angle >= 270:
                self.bite_down = 0
        else:
            self.end_angle += -self.bite_speed
            self.start_angle += self.bite_speed
            if self.end_angle <= 230:
                self.bite_down = 1


class PacGame(Widget):
    pac = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PacGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.pac.move(keycode)

    def update(self, dt):
        self.pac.chomp()
        self.pac.move()


class PacmanApp(App):
    def build(self):
        # ordering for game initilization
        game = PacGame()
        Clock.schedule_interval(game.update, 1.0/60)
        return game

if __name__ == '__main__':
    PacmanApp().run()