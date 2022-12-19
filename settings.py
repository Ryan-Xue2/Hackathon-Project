import pygame


class Settings:
  """Define the settings of the game"""

  def __init__(self):
    """Defining variables"""
    self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

    self._set_variables()
    self._adjust_values_to_screen_size()

  def _set_variables(self):
    """Set or reset the settings to their default values"""
    # Screen dimensions
    self.screen_width, self.screen_height = self.screen.get_size()
    
    # Player settings
    self.player_gravity = 1
    self.player_speed = 5
    self.player_jump_force = 17

    # jump boost multiplier
    self.jump_multiplier = 1

    # Evil santa's settings
    self.bad_santa_speed = 1
    self.bad_santa_gravity = 1
    self.bad_santa_jump_force = 10
    
  def handle_screen_resized(self):
    """
    In the case that the screen is resized, 
    this method should be called to adjust the speeds,
    gravities, and jump forces to the new screen size
    """
    self.screen_width, self.screen_height = self.screen.get_size()
    
    self._set_variables()
    self._adjust_values_to_screen_size()

  def _adjust_values_to_screen_size(self):
    """
    Adjust the variables to the screen size,
    assuming the variables are set to their default value
    """
    # Base line is roughgly (900, 550) so find ratio between the baseline
    # and the screen size and adjust the movement speeds, 
    # jump heights, and gravities accordingly
    hor_multiplier = self.screen_width / 900
    ver_multiplier = self.screen_height / 550 
    
    self.player_speed *= hor_multiplier
    self.bad_santa_speed *= hor_multiplier

    self.player_jump_force *= ver_multiplier
    self.player_gravity *= ver_multiplier
    self.bad_santa_gravity *= ver_multiplier
    self.bad_santa_jump_force *= ver_multiplier