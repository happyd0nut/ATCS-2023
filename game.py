import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1400, 800
CELL_SIZE = 50
ROWS, COLS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Game Board")

clock = pygame.time.Clock()

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(WHITE)

        # Draw the game board
        draw_board()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

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
    with open("Assets/NoTunnelPaths.txt", "r") as file:
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
                        self.ghost = Ghost(self, line[col], pos_x, pos_y)
                        self.ghost.set_spawn_node(node)
                    elif letter == "D":
                        self.scatter_node = node
                    
                    self.path_nodes.add(node)
                    grid_row.append(node)
                else:
                    grid_row.append(None)
                    

            self.txt_grid.append(txt_row)
            self.grid.append(grid_row)
            line = file.readline()
            row += 1

    # Set the ghost's scatter node
    self.ghost.set_scatter_node(self.scatter_node)

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

if __name__ == "__main__":
    main()
