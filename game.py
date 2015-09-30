import pygame, sys
from pygame.locals import *

# pygame constants
SQUARE_SIZE = 50
CONTROL_PANEL_WIDTH = 400
VERT_SQUARES = 16
HOR_SQUARES = 16
WINDOW_WIDTH = SQUARE_SIZE*VERT_SQUARES
WINDOW_HEIGHT = SQUARE_SIZE*HOR_SQUARES + CONTROL_PANEL_WIDTH

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (127,127,127)
GREEN_TRANSPARENT = (0, 255, 0, 128)
GRID_LINE_THICKNESS = 2

class GridTile:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.selected = False

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def draw(self, windowSurface):
        X = self.x*SQUARE_SIZE+1
        Y = self.y*SQUARE_SIZE+1
        self.draw_border(windowSurface)
        if self.selected:
            pygame.draw.rect(windowSurface, GREEN_TRANSPARENT, (X,Y,SQUARE_SIZE-1,SQUARE_SIZE-1))
        else:
            pygame.draw.rect(windowSurface, WHITE, (X,Y,SQUARE_SIZE-1,SQUARE_SIZE-1))

    def draw_border(self, windowSurface):
        pygame.draw.lines(windowSurface, GREY, True, [(self.x*SQUARE_SIZE,self.y*SQUARE_SIZE), (self.x*SQUARE_SIZE+SQUARE_SIZE,self.y*SQUARE_SIZE)
            , (self.x*SQUARE_SIZE+SQUARE_SIZE,self.y*SQUARE_SIZE+SQUARE_SIZE), (self.x*SQUARE_SIZE,self.y*SQUARE_SIZE+SQUARE_SIZE)], GRID_LINE_THICKNESS)


class Grid:
    def __init__(self):
        self.grid = {(x, y): GridTile(x,y) for x in range(HOR_SQUARES) for y in range(VERT_SQUARES)}
        self.current_tile = None

    def draw(self, windowSurface):
        for x in range(HOR_SQUARES):
            for y in range(VERT_SQUARES):
                self.grid[(x, y)].draw(windowSurface)

    def select_tile(self, coordinates):
        if self.current_tile:
            self.current_tile.deselect()
        self.current_tile = self.grid[coordinates]
        self.current_tile.select()


class Game:

    def __init__(self):
        self.windowSurface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), 0, 32)
        self.grid = Grid()

    def run(self):
        pygame.init()
        pygame.display.set_caption("SENG 330 PROJECT")

        basic_font = pygame.font.SysFont(None, 48)
        self.windowSurface.fill(WHITE)

        pygame.display.update()

        # game loop
        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    if event.pos[0] < SQUARE_SIZE*HOR_SQUARES:
                        xpos = event.pos[0]//SQUARE_SIZE
                        ypos = event.pos[1]//SQUARE_SIZE
                        self.grid.select_tile((xpos, ypos))
            self.grid.draw(self.windowSurface)


if __name__ == '__main__':
    Game().run()