"""
@author: Ms. Namasivayam and Julia Lau
"""

import pygame
import sys
import time
from npc import NPC
from player import Player
from pathnode import PathNode

class Game:

    # Constants
    WIDTH, HEIGHT = 910, 1000 
    START_X, START_Y = 55, 80 
    SPACING = 23.2  # Spacing of rows/cols
    FPS_NPC = 30
    FPS_PLAYER = 35

    # Colors
    WHITE = (255, 255, 255)
    BACKGROUND_COLOR = (255, 255, 255)

    def __init__(self):

        # Toggle to see Nodes and paths
        self.DEBUG = True

        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.dt_2 = 0

        # Initialize the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Life of Julia")
        self.background_img = pygame.image.load("Assets/background_town.png")
        self.background_img = pygame.transform.scale(self.background_img, (850, 915))

        # Sprites
        self.path_nodes = pygame.sprite.Group()
        self.npc = None
        self.destination_node = None
        self.player = None

        # Paths
        self.txt_grid = []
        self.grid = []

        print("before path")
        self.load_path()
        print("after path")

        # Load the NPC's initial paths
        self.npc.find_destination_path()


    def is_path(self, letter):
            """
            Returns True if the letter indicates a path
            exists at this location and false otherwise
            Args:
                letter (String): Letter from the text file

            Returns:
                boolean: True if a path exists, False otherwise
            """
            return self.is_path_node(letter) or letter == "*"

    def is_path_node(self, letter):
            """
            Returns True if the letter indicates that a 
            path NODE exists and False otherwise. This is different
            from just having a path exist.
            Args:
                letter (String): Letter from the text file

            Returns:
                boolean: True if it's a PathNode, False otherwise
            """
            options = ["X", "1", "P"]
            return letter in options

    def load_path(self):
        """
        Reads in the path file one character at a time
        and creates a Ghost and PathNodes from it.

        The maze and paths are saved into 2 different 2D arrays.
        self.grid saves PathNode objects in their appropriate 
        [row][col] location. It will save None if no Node exists there.

        self.txt_grid[] saves each text letter of the maze in its 
        [row][col] location.
        """
        row = 0
        with open("assets/map_town.txt", "r") as file:
            line = file.readline()
            while line:
                txt_row = []
                grid_row = []
                for col in range(len(line)-1):
                    letter = line[col]
                    txt_row.append(letter)

                    # Find position
                    pos_x = self.START_X + (self.SPACING * col)
                    pos_y = self.START_Y + (self.SPACING * row)

                    # Determine the type of Sprite to create
                    if self.is_path_node(letter):
                        node = PathNode(pos_x, pos_y, PathNode.DEFAULT)
                        if letter == "1":
                            self.npc = NPC(self, "1", pos_x, pos_y)
                            self.npc.set_spawn_node(node)
                        elif letter == "P":
                            self.player = Player(self, pos_x, pos_y)
        
                        self.path_nodes.add(node)
                        grid_row.append(node)
                    else:
                        grid_row.append(None)
                        
                self.txt_grid.append(txt_row)
                self.grid.append(grid_row)
                line = file.readline()
                row += 1

        # Set the NPC's destination node
        self.npc.set_destination_node(self.destination_node)

        # Connect the nodes
        self.connect_paths()

    def connect_paths(self):
        """
        Loops through self.txt_grid and self.grid to connect 
        each PathNode to it's next adjacent PathNode. We know 
        that there is a path between 2 Nodes if there is a 
        '*' indicated in the txt_grid array. '*'s connect our
        PathNodes "X" together.
        """
        # Connect the paths
        num_rows = len(self.txt_grid)
        num_cols = len(self.txt_grid[0])

        for row in range(num_rows):
            for col in range(num_cols):
                if self.is_path_node(self.txt_grid[row][col]):
                    # Is there a path to the right?
                    if col < (num_cols - 1) and self.is_path(self.txt_grid[row][col+1]):
                        # Find the next path node
                        for new_col in range(col+1, num_cols):
                            if (self.grid[row][new_col] is not None):
                                self.grid[row][col].add_adjacent(self.grid[row][new_col])
                                self.grid[row][new_col].add_adjacent(self.grid[row][col])
                                break
                    
                    # Is there a path down?
                    if row < (num_rows - 1) and self.is_path(self.txt_grid[row+1][col]):
                        # Find the next path node
                        for new_row in range(row+1, num_rows):
                            if(self.grid[new_row][col] is not None):
                                self.grid[row][col].add_adjacent(self.grid[new_row][col])
                                self.grid[new_row][col].add_adjacent(self.grid[row][col])
                                break

    def run(self):
        
        start_time = time.time()

        running = True
        while running:
            # Set frame rate
            self.dt += self.clock.tick(60)
            self.dt_2 += self.clock.tick(60)

            # Check for keyboard input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            keys = pygame.key.get_pressed()
            self.player.move(keys)

            # Update player location
            if self.dt_2 > self.FPS_PLAYER:
                self.player.update()
                self.dt_2 = 0
        
            # Update FSM input 
            if self.dt > self.FPS_NPC and len(self.npc.path) > 0:
                self.npc.fsm.process(self.npc.CAN_WALK)
                self.dt = 0
            
            # Wait 2 sec then find new destination_node when path empty
            if len(self.npc.path) == 0:
                if self.dt > 2000:
                    self.npc.find_destination_path()
                    self.dt = 0

            # Clear the screen
            self.screen.fill(self.BACKGROUND_COLOR)
            self.screen.blit(self.background_img, (30, 40)) #removed 250 from x

            # Check timer for FSM
            elapsed_time = time.time() - start_time
            if elapsed_time > self.npc.timer_duration:
                self.npc.fsm.process(self.npc.TIMER_UP)
                start_time = time.time()
            
            # Draw sprites
            if self.DEBUG:
                self.player.draw(self.screen)
            self.npc.draw(self.screen)

            # Update the display
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()