"""
@author: Julia Lau and Ms. Namasivayam
"""

import pygame
from fsm import FSM
import random


class NPC(pygame.sprite.Sprite):
    
    # states
    WALK = "wlk"
    TASK = "tsk"
    SLEEP = "slp"

    # inputs
    TIMER_UP = "tu"
    NIGHT = "nt"
    CAN_WALK = "cw"

    RIGHT, LEFT, UP, DOWN = 0, 1, 2, 3
    PEOPLE = {"1": "Friend"}

    def __init__(self, game, index, x, y):
        super().__init__()
        
        self.game = game
        self.name = self.PEOPLE[index]

        # Load initial image
        self.image = pygame.image.load("assets/npc.png") 
        self.rect = self.image.get_rect()

        # Set rectangle
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.centerx = x
        self.rect.centery = y

        # Set velocity and constants for speed
        self.vel_y = 0
        self.vel_x = 0
        self.speed = 3

        # Set the current node to Null
        self.spawn_node = None
        self.current_node = None
        self.destination_node = None

        # Initalize FSM
        self.fsm = FSM(self.SLEEP)
        self.init_fsm()
        self.timer_duration = 2
        self.clock = pygame.time.Clock()
        self.dt = 0
        
        # Set the path
        self.path = []

    def set_spawn_node(self, node):
        self.spawn_node = node
        self.set_current_node(node)

    def set_current_node(self, node):
        self.current_node = node

    def set_destination_node(self, node):
        self.destination_node = node

    def find_destination_path(self):
        """
        Picks a random node to go to and
        finds the path from the current 
        node to the ghost's next destination node.
        """
        # Pick a random node to go to 
        rand = random.randint(0, len(self.game.path_nodes)-1)
        self.destination_node = self.game.path_nodes.sprites()[rand]

        # Use DFS to find path to destination node
        self.find_dfs_path_helper(self.current_node, self.destination_node)

    def find_dfs_path_helper(self, start_node, end_node): # uses Stacks
        """
        Finds a path from the start_node to the end_node
        using DFS
        """
        parents = {}
        visited = []
        open_set = []
        self.current_node = start_node
        while self.current_node != end_node:
            for node in self.current_node.adjacent_nodes: # for all adjacent nodes to curr_node
                if node not in visited: 
                    # print(node)
                    visited.append(self.current_node) # add current node to visited
                    open_set.append(node) # add adjacent node at back of list
                    parents[node] = self.current_node # assign parent to adjacent node
            self.current_node = open_set.pop() # pop from back, and now repeat (Stack)
            
        trace_node = end_node
        while trace_node != start_node:
            self.path.insert(0, trace_node)
            trace_node = parents[trace_node]
        self.path.insert(0, start_node)

    def stop(self):
        self.vel_x = 0
        self.vel_y = 0
    
    def move(self, input=None):
        self.update_velocities()
        
        # Update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def update_velocities(self):
        """
        Determines the direction of the next node
        in the path and sets the velocity towards
        that direction.
        """
        # Reset velocities to 0
        self.stop()

        if len(self.path) == 0:
            return
        
        # Determine which direction to go
        next_node = self.path[0]

        diffx = next_node.rect.centerx - self.rect.centerx
        diffy = next_node.rect.centery - self.rect.centery

        # If we're there (or close enough), switch nodes
        if abs(diffx) <= self.speed and abs(diffy) <= self.speed:
            self.current_node = next_node
            self.path.pop(0)

            # update position to be the node's position
            self.rect.centerx = self.current_node.rect.centerx
            self.rect.centery = self.current_node.rect.centery
            return

        # If we're in line with x, we're going up or down
        if abs(diffx) < self.speed:
            if diffy > 0:
                # The node is below us
                self.vel_y = self.speed
            else:
                self.vel_y = -self.speed
        
        # Otherwise we're going left or right
        else:
            if diffx > 0:
                # The node is to the right
                self.vel_x = self.speed
            else:
                self.vel_x = -self.speed

    # FSM Methods Below:

    def init_fsm(self): # print out what it should be doing
        self.fsm.add_transition(self.TIMER_UP, self.SLEEP, self.do_task, self.TASK)
        self.fsm.add_transition(self.TIMER_UP, self.TASK, self.walk, self.WALK)
        self.fsm.add_transition(self.TIMER_UP, self.WALK, self.sleep, self.SLEEP)
        self.fsm.add_transition(self.CAN_WALK, self.WALK, self.move, self.WALK)
        self.fsm.add_transition(self.CAN_WALK, self.SLEEP, None, None)
        self.fsm.add_transition(self.CAN_WALK, self.TASK, None, None)

    def do_task(self):
        print("i am doing my task!")
        self.timer_duration = 5
        self.image = pygame.image.load("assets/npc_task.png")
    
    def walk(self):
        print("i am walking")
        self.timer_duration = 15
        self.image = pygame.image.load("assets/npc.png")

    def sleep(self):
        print("zz zz zzzz")
        self.timer_duration = 5
        self.image = pygame.image.load("assets/npc_sleep.png")

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y ))