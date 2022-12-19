import pygame

from constants import ENEMY_SPAWN
from helpers import load_transparent_image, get_block_size


class EvilSanta:
  """Here to ruin christmas"""
  
  def __init__(self, game):
    """Initialize resources for evil santa"""
    self.settings = game.settings
    self.screen = game.screen
    self.screen_width, self.screen_height = self.screen.get_size()

    self.player = game.player
    self.level_rects = game.level_rects
    
    # Load evil santa's image
    # Keep a copy of the orignal image so pixels aren't lost in the scaling process
    self.image_og = load_transparent_image('images/santa_og.png')
    self.image = load_transparent_image('images/santa_og.png')
    
    # Evil santa's rect 
    self.rect = self.image.get_rect()

    # Float values for x and y position
    self.x = self.rect.x
    self.y = self.rect.y
    
    # Evil santa's x move speed
    self.move_speed = self.settings.bad_santa_speed
    
    # Evil santa's y velocity, jumping power, and gravity
    self.y_velocity = 0
    self.jump_force = self.settings.bad_santa_jump_force
    self.gravity = self.settings.bad_santa_gravity
    
    # Collision flags
    self.collided_right = False
    self.collided_left = False
    self.collided_bottom = False

  def set_position(self, x, y): 
    """Set evil santa's position to the specified x and y values"""
    self.x = x
    self.rect.x = x
    self.y = y
    self.rect.y = y

  def _find_spawn_point(self, level):
    """Return a tuple (x, y) representing the spawn point of the evil santa"""
    block_width, block_height = get_block_size(level, self.screen_width, self.screen_height)
    for i, row in enumerate(level):
      for j, block in enumerate(row):
        if block == ENEMY_SPAWN:
          x = j*block_width
          y = i*block_height + block_height - self.rect.height
          return (x, y)
    raise Exception('Missing spawn point for evil santa')

  def load_level(self, level, level_rects):
    """
    Load the new level rects, 
    scale the evil santa to the new level,
    and place evil santa on his spawn block
    """
    self.level_rects = level_rects

    # Scale evil santa's image to 80% of the width of one block in the level
    block_width = self.screen_width / len(level[0])
    self.scale_image(block_width * 0.8)
    
    # Place evil santa at spawn
    spawn_x, spawn_y = self._find_spawn_point(level)
    self.set_position(spawn_x, spawn_y)

  def scale_image(self, width):
    """
    Scale evil santa's image to the specified width.
    Additionally scales evil santa's rect along with his image.
    """
    image_width, image_height = self.image_og.get_size()
    new_height = width * (image_height / image_width)
    self.image = pygame.transform.scale(self.image_og, (width, new_height))
    
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y
    
  def update_position(self):
    """
    Move the evil santa in the direction of the player.
    Handle any collisions with blocks or the floor.
    """
    # Finds out where player is and move in their direction 
    if self.player.x - self.x > 0:
      self.x += self.move_speed
    else:
      self.x -= self.move_speed

    # If being restricted by a wall and not midair, then jump
    if not self._is_midair() and (self.collided_left or self.collided_right):
      self.y_velocity = -self.jump_force

    # If midair, then apply gravity
    if self._is_midair():
      self.y_velocity += self.gravity

    # Update y position
    self.y += self.y_velocity

    # Sync rect position with float x and y positions
    self.rect.x = self.x
    self.rect.y = self.y

    # Deal with collisions with blocks in the level and with the player
    self._handle_collisions()
    self._check_player_collision()
    
  def _handle_collisions(self):
    """Deal with any collisions that evil santa faces"""
    # Don't let santa pass through floor
    if self.rect.bottom > self.screen_height:
      self.y = self.screen_height - self.rect.height
      self.y_velocity = 0
                        
    # Sync the rect position to the float x and y values
    self.rect.x = self.x
    self.rect.y = self.y

    # Reset collision varaibles
    self.collided_bottom = False
    self.collided_right = False
    self.collided_left = False
    
    for rect in self.level_rects:
      if self.rect.colliderect(rect):
        # Figure out whether the evil santa is closing to the horizontal part of the block 
        # or the vertical part and do the evil santa translation to the one closer
        dist_left = abs(rect.right - self.rect.left)
        dist_right = abs(rect.left - self.rect.right)
        dist_top = abs(rect.bottom - self.rect.top)
        dist_bottom = abs(rect.top - self.rect.bottom)

        # Collision with right or left side is closer than the collision to the top or bottom
        if min(dist_left, dist_right) < min(dist_top, dist_bottom):
          # Evil santa's left side hit wall
          if dist_left < dist_right:
            self.collided_left = True
            self.x = rect.right + 1
            
          # Evil santa's right side hit wall
          else:
            self.collided_right = True
            self.x = rect.left - self.rect.width - 1
          
        else:
          # Evil santa's feet hit block
          if dist_bottom < dist_top:
            self.y = rect.top - self.rect.height + 1
            self.collided_bottom = True
            self.y_velocity = 0
              
          # Evil santa's head hit block
          else:
            self.y = rect.bottom + 1
            self.y_velocity = 0

        # Update the evil santa's rects
        self.rect.x = self.x
        self.rect.y = self.y

  def _is_midair(self):
    """
    Returns true if evil santa is not standing on anyting, else
    returns False
    """
    if self.rect.bottom >= self.screen_height:
      return False
    return not self.collided_bottom

  def _check_player_collision(self):
    """
    Checks if evil santa collided with the player and if
    True, then return True, otherwise returns False
    """
    if self.rect.colliderect(self.player.rect):
      return True
    return False
      
  def blit(self):
    """Draw evil santa to the screen"""
    self.screen.blit(self.image, self.rect)