import pygame
import random

from helpers import get_block_size, load_transparent_image
from constants import PRESENT_BLOCK


class Present:
  """
  Class to manage the collection of the presents, keep score of presents collected
  and display to the screen the number of presents collected
  """
  def __init__(self, player, screen):
    self.screen = screen
    self.player = player
    self.present_types = []
    self.present_rects = []
    
    self.score = 0  # Presents collected
    self.total_presents = len(self.present_rects)  # Total presents in level
    self.font = pygame.font.SysFont(None, 48)  # The font for the score

    # Load the images of the presents
    self.present_img = load_transparent_image('images/present1.png')
    self.present_img2 = load_transparent_image('images/present2.png')
    self.present_img3 = load_transparent_image('images/present3.png')

  def load_level(self, level):
    """
    Load the presents in the level, 
    reset the presents collected and the 
    total number of presents
    """
    self.present_rects = []
    self.present_types = []
    self.score = 0
    self.total_presents = 0
    
    screen_width, screen_height = self.screen.get_size()
    block_width, block_height = get_block_size(level, screen_width, screen_height)

    # Scale the images to the new block size
    self.present_img = pygame.transform.scale(
      self.present_img, (block_width, block_height)
    )
    self.present_img2 = pygame.transform.scale(
      self.present_img2, (block_width, block_height)
    )
    self.present_img3 = pygame.transform.scale(
      self.present_img3, (block_width, block_height)
    )

    for i, row in enumerate(level):
      for j, block in enumerate(row):
        if block == PRESENT_BLOCK:
          self.present_rects.append(pygame.Rect(j * block_width, i * block_height ,
                                                block_width, block_height))
          self.present_types.append(random.randint(1, 3))
          self.total_presents += 1

  def draw_presents(self):
    """Draw the presents to the screen"""
    images = [self.present_img,
              self.present_img2,
              self.present_img3]
    for rect, type in zip(self.present_rects, self.present_types):
      self.screen.blit(images[type-1], rect)
    
  def check_collect_presents(self):
    """Collect any presents that have collided with the player"""
    for i, present in enumerate(self.present_rects):
      # If present collided with player, remove present and increase score
      if self.player.rect.colliderect(present):
        self.present_rects.remove(present)
        self.present_types.pop(i)
        self.score += 1

  def show_score(self):
    """
    Display the number of presents collected
    onto the top right part of the screen
    """
    score_text = f"{self.score} / {self.total_presents}"
    score_surf = self.font.render(score_text, True, (255, 255, 255), (0, 0, 0, 0))

    # Place score 10 pixels down and 10 pixels from the right of the screen
    score_rect = score_surf.get_rect()
    score_rect.left = self.screen.get_width() - score_rect.width - 10
    score_rect.top = 10

    self.screen.blit(score_surf, score_rect)