"""
@author: Ms. Namasivayam
"""

import pygame

class PathNode(pygame.sprite.Sprite):
    DEFAULT = 0

    def __init__(self, x=50, y=50, node_type=0):
        super().__init__()

        self.image = pygame.image.load("assets/node.png")
        self.type = node_type
        
        # Set the position to be the center of the image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x - self.width/2
        self.rect.y = y - self.height/2

        # Creates an array of adjacent nodes
        self.adjacent_nodes = []
    
    def add_adjacent(self, p):
        self.adjacent_nodes.append(p)
    
    def __repr__(self):
        return str(self.rect.center)
        
