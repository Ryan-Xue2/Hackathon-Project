"""
Contains a list with all the levels for the game
as well as some functions to help with dealing with 
things related to the levels
"""


import pygame
from constants import *
from copy import deepcopy
from helpers import get_block_size, load_image, load_transparent_image

# SINGLE_BLOCK = 1
# MIDDLE_BLOCK = 2
# LEFT_BLOCK = 3
# RIGHT_BLOCK = 4
# DIRT_BLOCK = 5
# PRESENT_BLOCK = 6
# SPAWN_POINT = 7
# JUMP_BOOST = 8
# EXIT_BLOCK = 9
# SLEIGH2 = 10
# ENEMY_SPAWN = 11

# #tutorial stuff
# MOVEMENT1 = 21
# MOVEMENT2 = 22
# MOVEMENT3 = 23
# MOVEMENT4 = 24

tutorial = [ #complete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 9, 10, 0, 0],
  [2, 2, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4],
]

level1 = [#complete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 9, 10, 0],
  [2, 2, 2, 5, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2],
]

level2 = [#incomplete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 9, 10, 0],
  [2, 2, 2, 2, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2],
]

level3 = [#incomplete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 9, 10, 0],
  [2, 2, 2, 2, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2],
]

level4 = [#incomplete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [9, 10, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [3, 4, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 3, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
  [0, 0, 0, 6, 0, 3, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 4],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 8, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 0, 0],
  [0, 0, 0, 2, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 0, 0],
  [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [7, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 6],
  [3, 2, 2, 5, 5, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4],
]

level5 = [#incomplete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 9, 10, 0],
  [2, 2, 2, 2, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2],
]

level6 = [#incomplete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 9, 10, 0],
  [2, 2, 2, 2, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2],
]

level7 = [#incomplete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
  [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 9, 10, 0],
  [2, 2, 2, 2, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2],
]


level9 = [  # Complete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0],
  [0, 0, 0, 6, 6, 0, 0, 0, 9, 10, 0, 0, 0, 6, 6, 6, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 3, 2, 2, 4, 0],
  [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 5, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 5, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 5, 6, 6, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 5, 2, 2, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

level10 = [  # Complete
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 9, 10, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0],
  [0, 0, 3, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 0, 0, 0, 0, 0, 6],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
  [6, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0],
  [1, 0, 3, 2, 4, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 3, 2, 2, 2, 4, 0],
  [0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0],
]

# real level list
level_list = [tutorial, tutorial, level9, level10,
]

# level list to test levels
# level_list = [tutorial, level2, level3, level4]


def draw_level(level, surface):
  """Draws the level to the surface"""
  # Load all the images
  single_block_img = load_transparent_image('images/single_block.png')
  middle_block_img = load_transparent_image('images/middle_block.png')
  left_block_img = load_transparent_image('images/left_block.png')
  right_block_img = load_transparent_image('images/right_block.png')
  dirt_block_img = load_image('images/dirt_block.png')
  # Exit block 
  sleigh1_img = load_transparent_image('images/sleigh1.png')
  sleigh2_img = load_transparent_image('images/sleigh2.png')
  #Tutorial stuff
  movement1_img = load_transparent_image('images/movement1.png')
  movement2_img = load_transparent_image('images/movement2.png')
  movement3_img = load_transparent_image('images/movement3.png')
  movement4_img = load_transparent_image('images/movement4.png')
  
  # Scale the images to the correct width and height
  surf_width, surf_height = surface.get_size()
  block_width, block_height = get_block_size(level, surf_width, surf_height)
  
  single_block_img = pygame.transform.scale(single_block_img, (block_width+1, block_height+1))
  middle_block_img = pygame.transform.scale(middle_block_img, (block_width+1, block_height+1))
  left_block_img = pygame.transform.scale(left_block_img, (block_width+1, block_height+1))
  right_block_img = pygame.transform.scale(right_block_img, (block_width+1, block_height+1))
  dirt_block_img = pygame.transform.scale(dirt_block_img, (block_width+1, block_height+1))
  sleigh1_img = pygame.transform.scale(sleigh1_img, (block_width+1, block_height+1))
  sleigh2_img = pygame.transform.scale(sleigh2_img, (block_width+1, block_height+1))
  movement1_img = pygame.transform.scale(movement1_img, (block_width+1, block_height+1))
  movement2_img = pygame.transform.scale(movement2_img, (block_width+1, block_height+1))
  movement3_img = pygame.transform.scale(movement3_img, (block_width+1, block_height+1))
  movement4_img = pygame.transform.scale(movement4_img, (block_width+1, block_height+1))

  # Draw the blocks to the screen
  for i, row in enumerate(level):
    for j, block in enumerate(row):
      x = j * block_width
      y = i * block_height
      if block == SINGLE_BLOCK:
        surface.blit(single_block_img, (x, y))
      elif block == MIDDLE_BLOCK:
        surface.blit(middle_block_img, (x, y))
      elif block == LEFT_BLOCK:
        surface.blit(left_block_img, (x, y))
      elif block == RIGHT_BLOCK:
        surface.blit(right_block_img, (x, y))
      elif block == DIRT_BLOCK:
        surface.blit(dirt_block_img, (x, y))
      elif block == SLEIGH1:
        surface.blit(sleigh1_img, (x, y))
      elif block == SLEIGH2:
        surface.blit(sleigh2_img, (x, y))
      elif block == MOVEMENT1:
        surface.blit(movement1_img, (x, y))
      elif block == MOVEMENT2:
        surface.blit(movement2_img, (x, y))
      elif block == MOVEMENT3:
        surface.blit(movement3_img, (x, y))
      elif block == MOVEMENT4:
        surface.blit(movement4_img, (x, y))
      
        
def get_rect_size(level, row, col):
  """
  Find the width and height of the widest, highest rectangle
  you can make if the top-left corner of the rectangle starts at (row, col)
  and the rectangle can only consist of the same value.
  """
  # Represents the value that the rectangle will consist of 
  target_value = level[row][col]

  # Initalize the width and height of the rect
  rect_width = 0
  rect_height = 1

  # Find the maximum width of the rectangle you can make
  for i in range(col, len(level[row])):
    if level[row][i] != target_value:
      break
    rect_width += 1

  # Find the maximum height of the rectangle given 
  reached_max_height = False
  for i in range(row+1, len(level)):
    for j in range(col, min(len(level[i]), col+rect_width)):
      if level[i][j] != target_value:
        reached_max_height = True
        break
    if reached_max_height:
      break
    rect_height += 1
    
  return rect_width, rect_height


def set_zero(matrix, row, col, width, height):
  """Zeroes out the selected range of blocks in the 2d list"""
  for i in range(row, row+height):
    for j in range(col, col+width):
      matrix[i][j] = 0
      
  
def smush_level(level, screen_width, screen_height):
  """
  This function will take as input a 2d list representing a level,
  the screen width and screen height, and will compress the level by 
  making connected blocks of the same type a single rect, scaled to the screen size. 
  This function will return a list of pygame rects representing the blocks.
  """
  level = deepcopy(level)  # Copy the level to avoid making changes to the original level list
  smushed = []
  
  # Calculate how large each block in the level would be on the screen
  block_width, block_height = get_block_size(level, screen_width, screen_height)

  ignore_blocks = [0, PRESENT_BLOCK, SLEIGH1,
                   SLEIGH2, SPAWN_POINT, ENEMY_SPAWN,
                   JUMP_BOOST, MOVEMENT1, MOVEMENT2,
                   MOVEMENT3, MOVEMENT4]
  
  for i, row in enumerate(level):
    for j, block in enumerate(row):
      # If the block isn't nothing and isn't a present, make the rect
      if block not in ignore_blocks:
        # Get the width and height of the biggest rectangle that can be made from (i, j)
        width, height = get_rect_size(level, i, j)
        
        # Set the blocks that are part of the rectangle to 
        # zero to avoid using these blocks again in another rectangle
        set_zero(level, i, j, width, height)  

        # Create a pygame Rect for the rectangle and add it to the list of rects
        x, y = j * block_width, i * block_height
        rect_width = block_width * width + 1
        rect_height = block_height * height + 1
        smushed.append(pygame.Rect(x, y, rect_width, rect_height))
        
  return smushed


def get_sleigh_rects(level, screen_width, screen_height):
  """Gets the rects of the sleigh"""
  # Calculate how large each block in the level would be on the screen
  block_width, block_height = get_block_size(level, screen_width, screen_height)
  
  # Get the rects of the sleigh
  sleigh_rects = []
  for i, row in enumerate(level):
    for j, block in enumerate(row):
      if block == SLEIGH1 or block == SLEIGH2:
        sleigh_rect = pygame.Rect(j*block_width, i*block_height,
                                      block_width+1, block_height+1)
        sleigh_rects.append(sleigh_rect)
        
  return sleigh_rects