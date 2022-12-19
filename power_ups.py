import pygame

from constants import JUMP_BOOST
from helpers import get_block_size, load_transparent_image

class PowerUps:
  """Class to manage powerups"""
  def __init__(self, settings, player, game):
    """Initialize values"""
    self.settings = settings   
    self.screen = game.screen
    self.player = player

    # initialize list of powerup rects
    self.powerup_rects = []

  def load_powerups(self, level):
    """Checks if the player has collected a powerup"""
    self.powerup_rects = []

    # gets the screen width and height
    screen_width, screen_height = self.screen.get_size()
    block_width, block_height = get_block_size(level, screen_width, screen_height)

    # Scale the images to the new block size
    self.jump_boost_img = load_transparent_image('images/jump_boost.png')
    self.jump_boost_img = pygame.transform.scale(
      self.jump_boost_img, (block_width, block_height)
    )

    # for each block, if it is jumpboost, append its rect to powerup_rects
    for i, row in enumerate(level):
      for j, block in enumerate(row):
        if block == JUMP_BOOST:
          self.powerup_rects.append(pygame.Rect(j * block_width, i * block_height ,
                                                block_width, block_height))
  
  def check_collect_powerups(self):
    """Checks if the player has collected a powerup"""
    for i, powerup in enumerate(self.powerup_rects):
      # If powerup collided with player, remove powerup and give the intended effect
      if self.player.rect.colliderect(powerup):
        self.powerup_rects.remove(powerup)
        self.player.jump_multiplier += 0.15

  
  def reset_powerups(self):
    """Resets the powerups once the player enters a new level"""
    self.player.jump_multiplier = 1


  def blit(self):
    """Draws the powerups to the screen"""
    for rect in self.powerup_rects:
      self.screen.blit(self.jump_boost_img, rect)