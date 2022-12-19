import pygame

class Stats:
  """Class to manage stats (excluding presents)"""
  
  def __init__(self, screen):
    self.screen = screen
    self.deaths = 0

    # initialize the font for displaying deaths
    self.font = pygame.font.SysFont(None, 48)

    # 

  def show_deaths(self):
    """
    Display how many times the player has died
    onto the top right part of the screen
    """
    deaths_text = f"{self.deaths} Ls"
    deaths_surf = self.font.render(deaths_text, True, (255, 255, 255), (0, 0, 0, 0))

    # Place # of deaths 10 pixels down and 125 pixels from the right of the screen
    deaths_rect = deaths_surf.get_rect()
    deaths_rect.left = self.screen.get_width() - deaths_rect.width - 125
    deaths_rect.top = 10

    self.screen.blit(deaths_surf, deaths_rect)

  def show_highscore(self):
    """Display the highscores of the game onto the screen"""
    pass