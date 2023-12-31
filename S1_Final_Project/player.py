"""
@author: ChatGPT, editted by Julia Lau
"""

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        super().__init__()
        self.game = game

        # Load initial image
        self.image = pygame.image.load("assets/player.png") 
        self.rect = self.image.get_rect()

        # Set rectangle
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.centerx = x
        self.rect.centery = y

        # Set initial velocity
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 10

        self.current_node = None

    def set_spawn_node(self, node):
        self.spawn_node = node
        self.set_current_node(node)

    def set_current_node(self, node):
        self.current_node = node

    def move(self, keys):

        # Reset velocity to zero
        self.vel_x = 0
        self.vel_y = 0

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.vel_x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < self.game.WIDTH - self.width:
            self.vel_x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.vel_y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < self.game.HEIGHT - self.height:
            self.vel_y += self.speed

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y ))

"""
End of ChatGPT code
"""