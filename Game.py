from kivy.app import App
from kivy.uix.button import Button

class Game(App):
    def build(self):
        return Button(text='Hello World')

Game().run()