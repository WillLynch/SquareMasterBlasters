from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty


class GridTile(Button):
    coords = ListProperty([0, 0])

class GameBoard(GridLayout):
    current_player = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        for row in range(20):
            for column in range(20):
                grid_tile = GridTile(coords=(row, column))
                grid_tile.bind(on_release=self.button_pressed)
                self.add_widget(grid_tile)

    def button_pressed(self, button):
        print ('{} button clicked!'.format(button.coords))

class GameApp(App):
    def build(self):
        return GameBoard()

if __name__ == '__main__':
    GameApp().run()