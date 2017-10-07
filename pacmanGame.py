from kivy.app import App
from kivy.uix.widget import Widget

class PacGame(Widget):
	
class PacApp(App):
	def build(self):
    #initialize and return game
	game = PacGame()
	return game
    
if __name__ == '__main__':
	PacApp().run()
