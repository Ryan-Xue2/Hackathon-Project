"""Helper functions go here"""
import pygame


def get_block_size(level, screen_width, screen_height):
  """
  Calculates and returns the size of a block using
  the number of blocks horizontally and vertically in
  a level and the dimensions of the screen
  """
  block_size = (screen_width / len(level[0]), screen_height / len(level))
  return block_size


def load_transparent_image(image_name):
  """Load an image with the transparent pixels kept"""
  image = pygame.image.load(image_name).convert_alpha()
  return image


def load_image(image_name):
  """Load and return an image"""
  image = pygame.image.load(image_name).convert()
  return image