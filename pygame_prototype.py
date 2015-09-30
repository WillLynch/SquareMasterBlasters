import pygame, sys
from pygame.locals import *

# pygame constants
SQUARE_SIZE = 50

VERT_SQUARES = 16
HOR_SQUARES = 16
WINDOW_HEIGHT = SQUARE_SIZE*VERT_SQUARES
WINDOW_WIDTH = SQUARE_SIZE*HOR_SQUARES

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (127,127,127)

class GridTile():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.selected = False

    def select(self):
        self.selected = True

    def draw(self, windowSurface):
        X = self.x*SQUARE_SIZE+1
        Y = self.y*SQUARE_SIZE+1
        if self.selected:
			pygame.draw.rect(windowSurface, BLACK, (X,Y,SQUARE_SIZE-1,SQUARE_SIZE-1))


class Grid():
    def __init__(self):
        self.grid = {(x, y): GridTile(x,y) for x in range(HOR_SQUARES) for y in range(VERT_SQUARES)}

    def draw_grid_lines(self, windowSurface):
        for x in range(0,WINDOW_HEIGHT,SQUARE_SIZE):
            pygame.draw.line(windowSurface, GREY, [x,0], [x,WINDOW_WIDTH], 2)
        for y in range(0,WINDOW_WIDTH,SQUARE_SIZE):
            pygame.draw.line(windowSurface,GREY,[0,y], [WINDOW_HEIGHT,y], 2)

    def draw(self, windowSurface):
        for x in range(HOR_SQUARES):
            for y in range(VERT_SQUARES):
                self.grid[(x, y)].draw(windowSurface)

    def select_tile(self, coordinates):
        self.grid[coordinates].select()



class Game():

    def __init__(self):
        self.windowSurface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), 0, 32)
        self.grid = Grid()

    def run(self):
        pygame.init()
        pygame.display.set_caption("SENG 330 PROJECT")

        basic_font = pygame.font.SysFont(None, 48)
        self.windowSurface.fill(WHITE)

        self.grid.draw_grid_lines(self.windowSurface)
        pygame.display.update()

        # game loop
        while True:
            pygame.display.update()
            # user event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    xpos = event.pos[0]//SQUARE_SIZE
                    ypos = event.pos[1]//SQUARE_SIZE
                    self.grid.select_tile((xpos, ypos))
            self.grid.draw(self.windowSurface)


if __name__ == '__main__':
	Game().run()