import pygame

from constants import SPAWN_POINT
from helpers import load_transparent_image, get_block_size


class Player:
  """A class to manage the player's position and the """

  def __init__(self, game):
    """Initialize the player's resources"""
    # Initialize game settings
    self.settings = game.settings

    # List of rects representing the blocks in the level
    self.level_rects = game.level_rects

    # Display surface and its dimensions
    self.screen = game.screen
    self.screen_width = game.WIDTH
    self.screen_height = game.HEIGHT

    # Load the santa images into memory
    # Original copies of the images so that there isn't any loss of pixels when scaling
    self.image_og = load_transparent_image('images/santa_standing.png')
    self.image_walking_og = load_transparent_image('images/santa_walking.png')
    self.image_jumping_og = load_transparent_image('images/santa_jumping.png')

    # Copies of the images to use to blit to the screen
    self.image = load_transparent_image('images/santa_standing.png')
    self.image_walking = load_transparent_image('images/santa_walking.png')
    self.image_jumping = load_transparent_image('images/santa_jumping.png')

    # Get the position and dimensions of the player and place the character
    # at the bottom right of the screen
    self.rect = self.image.get_rect()
    self.rect.bottom = self.screen_height
    self.rect.right = self.screen_width
    
    # Store the float values of x and y, since rects only store integer numbers
    self.x = self.rect.x
    self.y = self.rect.y

    # Define the player's move speed, jumping power, y velocity, and the force of gravity
    self.y_velocity = 0
    self.jump_multiplier = 1
    self.gravity = self.settings.player_gravity 
    self.move_speed = self.settings.player_speed
    self.jump_force = self.settings.player_jump_force

    # Movement flags
    self.moving_left = False
    self.moving_right = False
    self.jumping = False

    # Collision flags
    self.collided_bottom = False
    self.collided_right = False
    self.collided_left = False

    # Direction santa is facing
    self.facing_left = True

  def set_position(self, x, y):
    """Sets player's x and y position to the specified x and y values"""
    self.x = x
    self.y = y
    self.rect.x = x
    self.rect.y = y

  def load_level(self, level, level_rects):
    """
    Load the new rects representing the level,
    scale the images to the new level,
    and place the player on the correct spot
    """
    # Load in the new level rects
    self.level_rects = level_rects
    
    # Scale the images to the new level
    block_width = self.screen_width / len(level[0])
    self.scale_images(block_width)

    # Place the player at spawn
    spawn_x, spawn_y = self._find_spawn_point(level, 
                                              self.screen_width, 
                                              self.screen_height)
    self.set_position(spawn_x, spawn_y) 

  def scale_images(self, width):
    """
    Scale the santa images to the new width.
    Additionally, scales santa's rect along with the images.
    """
    # Calculate the height and width of the new images
    image_width, image_height = self.image_og.get_size()
    new_height = width * (image_height / image_width)
    
    # Scale the still image to the width of one block
    self.image = pygame.transform.scale(self.image_og, (width, new_height))
    # Scale the walking image to the width of one block
    self.image_walking = pygame.transform.scale(self.image_walking_og, (width, new_height))
    # Scale the jumping image to the width of one block
    self.image_jumping = pygame.transform.scale(self.image_jumping_og, (width, new_height))

    # Update player's rect
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y

  def update_position(self):
    """
    Update the players position based on the players movement flags 
    and also their y velocity. Doesn't allow the player to clip through objects.
    If the player is midair, then apply the force of gravity to the player's y velocity.
    """
    # Apply gravity to the y velocity if the player is midair
    if self._is_midair():
      self.y_velocity += self.gravity
    # Otherwise, if player is also jumping, then jump
    elif self.jumping:
      self.y_velocity = -self.jump_force * self.jump_multiplier

    # If the player is moving left or moving right but not both, then update x position
    if self.moving_left ^ self.moving_right:
      # Update the player's x position
      if self.moving_left and not self.collided_left:
        self.x -= self.move_speed
      elif self.moving_right and not self.collided_right:
        self.x += self.move_speed
        
      # If player runs past the screen, then put them back where they should be
      # and stop their movement
      if self.x + self.rect.width > self.screen_width:
        self.x = self.screen_width - self.rect.width
        self.moving_right = False
      elif self.x < 0:
        self.x = 0
        self.moving_left = False
      self.rect.x = self.x

    # Update the player's y position
    self.y += self.y_velocity
    
    # If player goes under the floor
    # put them back where they should be and cancel velocity
    if self.y + self.rect.height > self.screen_height:
      self.y_velocity = 0
      self.y = self.screen_height - self.rect.height
    self.rect.y = self.y
    
    # Deal with any collisions with blocks in the level 
    self._check_block_collision()
    
  def _is_midair(self):
    """Return True if player is midair, else return False"""
    # Check whether the player on the bottom of the screen
    if self.rect.bottom == self.screen_height:
      return False
    return not self.collided_bottom

  def _check_block_collision(self):
    """
    If the player collided with a block that is drawn on the screen, 
    stop their movement in that direction
    """
    # Reset the flags because otherwise, for example if the player
    # collided with the left wall, then moved away but is still colliding 
    # with a rect on the bottom for example, then even though the player
    # is no longer colliding with the left wall, they are still restricted from
    # moving in the left direction
    self.collided_right = False
    self.collided_left = False
    self.collided_bottom = False
    
    for rect in self.level_rects:
      if self.rect.colliderect(rect):
        # Figure out whether the player is closing to the horizontal part of the block 
        # or the vertical part and do the player translation to the one closer
        dist_left = abs(rect.right - self.rect.left)
        dist_right = abs(rect.left - self.rect.right)
        dist_top = abs(rect.bottom - self.rect.top)
        dist_bottom = abs(rect.top - self.rect.bottom)

        # Collision with right or left side is closer than the collision to the top or bottom
        if min(dist_left, dist_right) < min(dist_top, dist_bottom):
          # Player's left side hit wall
          if dist_left < dist_right:
            self.collided_left = True
            self.x = rect.right + 1
            
          # Player's right side hit wall
          else:
            self.collided_right = True
            self.x = rect.left - 1 - self.rect.width
          
        else:
          # Player's feet hit block
          if dist_bottom < dist_top:
            # Add 1 so that the player continues to collide and so that self.collided_bottom is 
            # always True when it appears the player is standing
            self.y = rect.top - self.rect.height + 1   
            
            self.collided_bottom = True
            self.y_velocity = 0
              
          # Player's head hit block
          else:
            self.y = rect.bottom + 1
            self.y_velocity = 0

        # Update the player's position
        self.rect.x = self.x
        self.rect.y = self.y

  def _find_spawn_point(self, level, screen_width, screen_height):
    """
    Returns the (x, y) position that the player 
    should be spawned at once a level is completed
    """
    # Calculate how large each block in the level would be on the screen
    block_width, block_height = get_block_size(level, screen_width, screen_height)
    
    # Find the spawn position
    for i, row in enumerate(level):
      for j, block in enumerate(row):
        if block == SPAWN_POINT:
          x = j*block_width + (block_width / 2)
          y = i*block_height + block_height - self.rect.height
          return (x, y)
    raise Exception('Player spawn position is missing from level')

  def blit(self):
    """Draw the player onto the game screen"""
    # Flip santa images
    image_flip = pygame.transform.flip(self.image, True, False) 
    image_walking_flip = pygame.transform.flip(self.image_walking, True, False) 
    image_jumping_flip = pygame.transform.flip(self.image_jumping, True, False)

    # If the player is midair
    if self._is_midair():
      # If moving left
      if self.moving_left:
          self.screen.blit(image_jumping_flip, self.rect) 
          self.facing_left = True
  
      # If moving right
      elif self.moving_right:
          self.screen.blit(self.image_jumping, self.rect) 
          self.facing_left = False

      # Not moving and facing left
      elif self.facing_left:
        self.screen.blit(image_jumping_flip, self.rect)

      # Not moving and facing right
      else:
        self.screen.blit(self.image_jumping, self.rect)
        
    # If the player is not midair
    else:
      # If moving left
      if self.moving_left:
         self.screen.blit(image_walking_flip, self.rect) 
         self.facing_left = True 
            
      # If moving right
      elif self.moving_right:
        self.screen.blit(self.image_walking, self.rect)
        self.facing_left = False
  
      # If facing left and standing still
      elif self.facing_left:
          self.screen.blit(image_flip, self.rect) 
        
      # If facing right and standing still
      else:
          self.screen.blit(self.image, self.rect) 