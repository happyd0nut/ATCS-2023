import pygame
from fsm import FSM
import time
import sys

class NPC(pygame.sprite.Sprite):
    
    # states
    WALK = "wlk"
    TASK = "tsk"
    SLEEP = "slp"

    # inputs
    TIMER_UP = "tu"
    NIGHT = "nt"

    RIGHT, LEFT, UP, DOWN = 0, 1, 2, 3
    PEOPLE = {"1": "Friend"}

    def __init__(self, game, name, x, y):
        super().__init__()
        
        self.game = game
        self.name = self.PEOPLE[name]

        # Setting up animation
        self.anim = []
        self.anim_count = 0
        self.anim_uption = self.UP
        # self.load_images()

        # Load initial image
        self.image = pygame.image.load("assets/npc.png") # add in image
        self.rect = self.image.get_rect()

        # Set rectangle
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.centerx = x
        self.rect.centery = y

        # Set velocity
        self.vel_y = 0
        self.vel_x = 0
        self.speed = 3

        # Initalize FSM
        self.fsm = FSM(self.WALK)
        self.init_fsm()
        self.timer_duration = 2

        self.walk()

    def set_spawn_node(self, node):
        """
        Assigns the spawn node and sets the 
        current node to it.
        Args:
            node (PathNode): The node to spawn at
        """
        self.spawn_node = node
        self.set_current_node(node)

    def set_current_node(self, node):
        self.current_node = node


    def load_images(self):
        """
        Load the images for walking NPC
        """
        right = self.load_image_directions("right")
        left = self.load_image_directions("left")
        up = self.load_image_directions("up")
        down = self.load_image_directions("down")

        self.anim.append(right)
        self.anim.append(left)
        self.anim.append(up)
        self.anim.append(down)


    def load_image_directions(self, dir):
        """
        Loads the animations for the specific ghost
        in the provided direction
        Args:
            dir (String): "right", "left", "up", or "down"

        Returns:
            list: A list of the animation images
        """
        filepath = "assets/" + self.name + "/" + dir
        anim = []
        for i in ["0", "1"]:
            anim.append(pygame.image.load(filepath+i+".png"))
        return anim

    # TODO: add all transition
    def init_fsm(self):
        # self.fsm.add_transition("$", self.WEST_BREAK, self.move_west, self.WIN)
        pass
    def walk(self):
        self.rect.centerx 

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y ))