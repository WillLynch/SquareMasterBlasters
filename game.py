import pygame, sys, os
from pygame.locals import *
from constants import *
from game_board import *
from itertools import chain

class Player:
    def __init__(self, board):
        self.board = board
        self.characters = []
        self.actions = TURN_ACTIONS

    def add_character(self, character):
        self.characters.append(character)
        self.board.grid[character.x, character.y] = character

    def remove_character(self, character):
        self.characters.remove(character)
        self.board.grid[character.x, character.y] = GridTile(character.x, character.y)

    def move_character(self, current_tile, x, y):
        if current_tile in self.characters:
            if x in range(current_tile.x-current_tile.move_ability_distance, current_tile.x+current_tile.move_ability_distance+1):
                if y in range(current_tile.y-current_tile.move_ability_distance, current_tile.y+current_tile.move_ability_distance+1):
                    temp_tile = self.board.grid[(x,y)]
                    temp_coordinates = (current_tile.x, current_tile.y)
                    self.board.grid[(x,y)] = current_tile
                    self.board.grid[(x,y)].set_coordinates(x, y)
                    self.board.grid[(temp_coordinates[0], temp_coordinates[1])] = temp_tile
                    self.board.grid[(temp_coordinates[0], temp_coordinates[1])].set_coordinates(temp_coordinates[0], temp_coordinates[1])
                    self.use_action()

    def attack_character(self, current_tile, x, y):
        if current_tile in self.characters:
            if x in range(current_tile.x-current_tile.attack_ability_distance, current_tile.x+current_tile.attack_ability_distance+1):
                if y in range(current_tile.y-current_tile.attack_ability_distance, current_tile.y+current_tile.attack_ability_distance+1):
                    attacked_tile = self.board.grid[(x,y)]
                    attacked_tile.health_points = attacked_tile.health_points - current_tile.attack_power
                    self.use_action()

    def use_action(self):
        self.actions = self.actions - 1

    def restore_actions(self):
        self.actions = TURN_ACTIONS

    def get_actions(self):
        return self.actions

    def has_actions(self):
        if self.actions > 0:
            return True
        else:
            return False


class Game:

    def __init__(self):
        self.windowSurface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), 0, 32)
        self.grid = Grid()
        self.player1 = Player(self.grid)
        self.player2 = Player(self.grid)
        self.player_turn = 0

    @staticmethod
    def text_objects(text, font):
        textSurface = font.render(text, True, (BLACK))
        return textSurface, textSurface.get_rect()

    def text_objects_white(text, font):
        textSurface = font.render(text, True, (WHITE))
        return textSurface, textSurface.get_rect()
    
    def display_turn_status(self, text):
        largeText = pygame.font.Font('freesansbold.ttf',60)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((WINDOW_WIDTH+CONTROL_PANEL_WIDTH/2),(100))
        self.windowSurface.blit(TextSurf, TextRect)

    def display_instructions(self):
        text = "Move character - m, Attack - a"
        small_text = pygame.font.Font('freesansbold.ttf',14)
        TextSurf, TextRect = self.text_objects(text, small_text)
        TextRect.center = ((WINDOW_WIDTH+CONTROL_PANEL_WIDTH/2),(500))
        self.windowSurface.blit(TextSurf, TextRect)

    # displays the Stats of the currently selected character. 
    def display_moves(self, playermoves):
        #this chunk acts as an eraser to get rid of the previous text first
        #text = "Remaining moves: 100"
        #small_text = pygame.font.Font('freesansbold.ttf',14)
        #TextSurf, TextRect = self.text_objects_white(text, small_text)
        #TextRect.center = ((WINDOW_WIDTH+CONTROL_PANEL_WIDTH/2),(150))
        #self.windowSurface.blit(TextSurf, TextRect)
        # This chunk sets the text to the current moves the player has
        text = "Remaining moves: " + str(playermoves)
        small_text = pygame.font.Font('freesansbold.ttf',14)
        TextSurf, TextRect = self.text_objects(text, small_text)
        TextRect.center = ((WINDOW_WIDTH+CONTROL_PANEL_WIDTH/2),(150))
        self.windowSurface.blit(TextSurf, TextRect)

    def run(self):
        pygame.init()
        pygame.display.set_caption("Square Master Blasters")

        basic_font = pygame.font.SysFont(None, 48)
        self.windowSurface.fill(WHITE)
        self.display_instructions()
        self.display_turn_status("Player 1")
        pygame.display.update()

        # for testing our pilot project, I have placed two random characters for each player
        # I've modified these to now declare which player each belongs to. 
        self.player1.add_character(Wilfred(1,1, PLAYER_ONE))
        self.player1.add_character(Doge(1,2, PLAYER_ONE))
        self.player1.add_character(Barney(1,3, PLAYER_ONE))
        self.player1.add_character(Bridget(1,4, PLAYER_ONE))
        self.player2.add_character(Moad(5,2, PLAYER_TWO))
        self.player2.add_character(Character(5,5, PLAYER_TWO))
        self.player2.add_character(George(5,4, PLAYER_TWO))
        
        # game loop
        current_player = self.player1
        other_player = self.player2
        current_tile = None
        move = False
        attack = False
        self.player_turn = 1

        while True:
            while current_player.has_actions():
                pygame.display.update()
                for event in pygame.event.get():
                    if move is True:
                        if event.type == MOUSEBUTTONUP:
                            if event.pos[0] < SQUARE_SIZE*HOR_SQUARES:
                                xpos = event.pos[0]//SQUARE_SIZE
                                ypos = event.pos[1]//SQUARE_SIZE
                                move_tile = self.grid.grid[(xpos,ypos)]
                                if current_tile in current_player.characters and move_tile not in other_player.characters:
                                    current_player.move_character(current_tile, xpos,ypos)
                                    move = False
                                move = False

                    elif attack is True:
                        if event.type == MOUSEBUTTONUP:
                            if event.pos[0] < SQUARE_SIZE*HOR_SQUARES:
                                xpos = event.pos[0]//SQUARE_SIZE
                                ypos = event.pos[1]//SQUARE_SIZE
                                attack_tile = self.grid.grid[(xpos, ypos)]
                                if current_tile in current_player.characters and attack_tile in other_player.characters:
                                    current_player.attack_character(current_tile, xpos, ypos)
                                    attack = False
                                    # remove character if dead
                                    if attack_tile.health_points <= 0:
                                        other_player.remove_character(attack_tile)

                                attack = False
                    else:
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == MOUSEBUTTONUP:
                            if event.pos[0] < SQUARE_SIZE*HOR_SQUARES:
                                xpos = event.pos[0]//SQUARE_SIZE
                                ypos = event.pos[1]//SQUARE_SIZE
                                current_tile = self.grid.select_tile((xpos, ypos))
                        elif event.type == KEYDOWN:
                            if event.key == K_m:
                                move = True
                            if event.key == K_a:
                                attack = True
                self.grid.draw(self.windowSurface, self.player_turn)
                print(current_player.get_actions())
                self.display_moves(current_player.get_actions())
            # Update Text to display how many moves the current player has
            # change turns
            if current_player is self.player1:
                current_player = self.player2
                other_player = self.player1
                self.player_turn = 2
                self.player1.restore_actions()
                self.windowSurface.fill(WHITE)
                self.display_turn_status("Player 2")
                self.display_instructions()
            else:
                current_player = self.player1
                other_player = self.player2
                self.player_turn = 1
                self.player2.restore_actions()
                self.windowSurface.fill(WHITE)
                self.display_turn_status("Player 1")
                self.display_instructions()

if __name__ == '__main__':
    Game().run()
