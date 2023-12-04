import pygame
from fsm import FSM
import time
import sys

class npc(pygame.sprite.Sprite):
    
    # states
    WALK = "wlk"
    TASK = "tsk"
    SLEEP = "slp"

    # inputs
    TIMER_UP = "tu"
    NIGHT = "nt"
    

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Load initial image
        self.image = pygame.image.load() # add in image
        self.rect = self.image.get_rect()

        # Set rectangle
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.centerx = x
        self.rect.centery = y

        # Initalize FSM
        self.fsm = FSM(self.WALK)
        self.init_fsm()
        self.timer_duration = 2

        self.walk()

    # TODO: add all transition
    def init_fsm(self):
        self.fsm.add_transition("$", self.WEST_BREAK, self.move_west, self.WIN)

    def walk(self):
        self.rect.centerx 