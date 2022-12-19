import time
import levels
import pygame, sys

from stats import Stats
from player import Player
from present import Present
from settings import Settings
from helpers import load_image
from power_ups import PowerUps
from evil_santa import EvilSanta
from moviepy.editor import VideoFileClip
from pygame.locals import QUIT, WINDOWRESIZED


class SnowStrider:
  """Main class to manage the game"""

  def __init__(self):
    """Initialize all the game resources"""
    pygame.init()

    # A list of levels that don't have evil santa in them
    self.no_santa = [0, 1]
    
    # Stores whether the game has been started from the user pressing enter yet
    self.game_running = False
    
    # Pygame clock to limit ticks/sec so its smoother
    self.clock = pygame.time.Clock()

    # Display and settings
    self.settings = Settings()
    self.screen = self.settings.screen
    self.WIDTH, self.HEIGHT = self.screen.get_size()
    pygame.display.set_caption('Snow Strider')

    # Stats instance to keep track of stats like # of Ls
    self.stats = Stats(self.screen)

    # Create a background surface that will have the background image
    # and the blocks of the level drawn on
    self.bg_surf = pygame.Surface((self.WIDTH, self.HEIGHT))
    self.tutorial_bg_surf = pygame.Surface((self.WIDTH, self.HEIGHT))
    
    # Load the background image and resize to the screen size
    self.bg_img = load_image('images/winter_background.webp')
    self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))
    
    # Load the background image for the tutorial 
    self.tutorial_bg_img = load_image('images/tutorial.png') 
    self.tutorial_bg_img = pygame.transform.scale(self.tutorial_bg_img, (self.WIDTH, self.HEIGHT))

    # load the title screen image
    self.title_img = load_image('images/title_screen.png')
    self.title_img = pygame.transform.scale(self.title_img, (self.WIDTH, self.HEIGHT))
    
    # Initialize the level list which contains 
    # the levels for the game.
    # Also initialize level_rects, which will
    # store the rects that rep. the blocks in the 
    # level to use to handle collisions
    self.lvl_idx = 0
    self.level_list = levels.level_list
    self.level_rects = []

    # Get the rects of the sleigh blocks
    self.sleigh_rects = levels.get_sleigh_rects(
      self.level_list[0], self.WIDTH, self.HEIGHT)

    # Instiantiate a Player instance
    self.player = Player(self)

    # Instiantiate an EvilSanta instance that will chase the player
    self.evil_santa = EvilSanta(self)
    
    # Instiantiate a Present instance to deal with the
    # player collisions with the presents and the displaying of text
    self.present_manager = Present(self.player, self.screen)

    # Instiantiate powerups
    self.powerups = PowerUps(self.settings, self.player, self)

    # Draw the level onto the background surface, and load the level
    # into the player instance, evil santa instance and present manager. 
    # Scales the sprites to the level and places the player 
    # and the evil santa on their respective spawn points
    self._load_level(self.level_list[self.lvl_idx])

  def run_game(self):
    """Main game loop"""
    while True:
      self._check_events()
      if self.game_running:
        self._check_completed_level()
        self._check_player_death()
        self.powerups.check_collect_powerups()
      self._update_screen()

  def _check_events(self):
    """Checks for the event and the type of event"""
    for event in pygame.event.get():
      # If the user presses the X button (top right), exit
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      # If the user resizes the window, then restart the level with the new screen dimensions
      elif event.type == WINDOWRESIZED:
        self._handle_resize_screen()
      # Deal with any key presses from the user
      elif event.type == pygame.KEYDOWN:
        self._handle_keydown_events(event)
      # Deal with key being released 
      elif event.type == pygame.KEYUP:
        self._handle_keyup_events(event)

  def _handle_resize_screen(self):
    """
    In the case of the screen being resized, adjust the 
    player and the evil santa's move speed accordingly. 
    Scale the all the blocks, the powerups, etc. to the new screen size. 
    Scale the background images, the background surfaces, the setting attributes.
    Also calculate the new level rects.
    """    
    # Get the new screen size and update the screen size in the settings as well
    self.WIDTH, self.HEIGHT = self.screen.get_size()
    self.settings.screen_width = self.WIDTH
    self.settings.screen_height = self.HEIGHT

    # Update the screen sizes in the player instance and in the evil santa instance
    self.player.screen_width = self.WIDTH
    self.player.screen_height = self.HEIGHT
    self.evil_santa.screen_width = self.WIDTH
    self.evil_santa.screen_height = self.HEIGHT
    
    # Resize the background surfaces
    self.bg_surf = pygame.transform.scale(self.bg_surf, (self.WIDTH, self.HEIGHT))
    self.tutorial_bg_surf = pygame.transform.scale(
                              self.tutorial_bg_surf, (self.WIDTH, self.HEIGHT))
    
    # Resize the background images
    self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))
    self.tutorial_bg_img = pygame.transform.scale(self.tutorial_bg_img, (self.WIDTH, self.HEIGHT))

    # Resize the title screen image
    self.title_img = pygame.transform.scale(self.title_img, (self.WIDTH, self.HEIGHT))
    
    # Update the settings
    self.settings.handle_screen_resized()
    
    # Update the player's speed, gravity, and jump force
    self.player.move_speed = self.settings.player_speed
    self.player.gravity = self.settings.player_gravity 
    self.player.jump_force = self.settings.player_jump_force
    
    # Update the evil santa's speed, gravity and jump force
    self.evil_santa.move_speed = self.settings.bad_santa_speed 
    self.evil_santa.gravity = self.settings.bad_santa_gravity 
    self.evil_santa.jump_force = self.settings.bad_santa_jump_force
    
    # Reload the level and in the process, resize the presents to the 
    # correct size, update the level rects for the player and the evil santa.
    # Also, draw the background surface and scale the powerups to the correct size as well.
    self._load_level(self.level_list[self.lvl_idx])
    
  def _load_level(self, level):
    """Load a level into memory"""
    # Get the rects representing the new level
    self.level_rects = levels.smush_level(level, self.WIDTH, self.HEIGHT)
    
    # Get the rects of the sleigh blocks
    self.sleigh_rects = levels.get_sleigh_rects(level, self.WIDTH, self.HEIGHT)
    
    # Draw the level onto the background surface with the background image behind
    if self.lvl_idx == 0:
      self.tutorial_bg_surf.blit(self.tutorial_bg_img, (0, 0))
      levels.draw_level(level, self.tutorial_bg_surf)
    else: 
      self.bg_surf.blit(self.bg_img, (0, 0))
      levels.draw_level(level, self.bg_surf)
    
    # Load in the new rects, scale the player images to the new level,
    # and place the player at their specified spawn point
    self.player.load_level(level, self.level_rects)
    
    # Find the new present positions, 
    # reset all the attributes that need to be reset
    # and scale the present images to the new level
    self.present_manager.load_level(level)

    # Load in the new rects for evil santa, scale evil santa's image to 
    # one block width of the new level, and place them at their specified spawn point
    self.evil_santa.load_level(level, self.level_rects)

    # load in jump boost powerups
    self.powerups.load_powerups(level)

    # reset powerup multipliers
    self.powerups.reset_powerups()

  def _check_player_death(self):
    """Respawn the player in the level at the correct position"""
    collided_with_bad_santa = self.evil_santa._check_player_collision()
    if self.lvl_idx in self.no_santa:
      collided_with_bad_santa = False
      
    if collided_with_bad_santa or self.player.rect.bottom >= self.HEIGHT:
      # Reload the level if the player died
      self._load_level(self.level_list[self.lvl_idx])
      self.stats.deaths += 1
    
  def _check_completed_level(self):
    """
    Check if the player has collected all the presents as well 
    if the player is touching the door. If both conditions are met,
    then load the next level if there is one. If there isn't, then 
    exit the game.
    """
    if self.present_manager.score == self.present_manager.total_presents:
      for sleigh_rect in self.sleigh_rects:
        if self.player.rect.colliderect(sleigh_rect):
          self.lvl_idx += 1
          # No more levels so play ending scene and quit game
          if self.lvl_idx == len(self.level_list):
            self._play_video('videos/ending_scene.mov')
            sys.exit()
          # Load the next level
          else:
            self._load_level(self.level_list[self.lvl_idx])
          break

  def _play_video(self, video_name):
    """Takes as input the filename of a video file and plays the video"""
    video = VideoFileClip(video_name)
    video.resize((self.WIDTH, self.HEIGHT)).preview()
    
  def _handle_keydown_events(self, event):
    # check if the user has pressed enter to start the game
    if event.key == pygame.K_RETURN and self.game_running == False:
      self.game_running = True
      # self._play_video('videos/cutscene.mov')
      return
    # If the player presses the - key, then quit the game
    if event.key == pygame.K_MINUS:
      sys.exit()
    # User presses W, A, D, or space to move
    elif event.key == pygame.K_a:
      self.player.moving_left = True
    elif event.key == pygame.K_d:
      self.player.moving_right = True
    elif event.key == pygame.K_w or event.key == pygame.K_SPACE:
      self.player.jumping = True

  def _handle_keyup_events(self, event):
    """Stop moving the character once they let go of the key"""
    # Stop moving if the user lets go of the A or D key
    if event.key == pygame.K_a:
      self.player.moving_left = False
    elif event.key == pygame.K_d:
      self.player.moving_right = False
    # Stop jumping if the user lets go of space or the W key
    elif event.key == pygame.K_w or event.key == pygame.K_SPACE:
      self.player.jumping = False

  def _update_screen(self):
    """Update the screen to simulate movement"""
    self.clock.tick(60)  # Max out the ticks/second so its smoother

    # if they have not pressed enter to start the game
    if self.game_running == False:
      # display title screen
      self.screen.blit(self.title_img, (0, 0))
    else:
      # Blit the background to the screen
      if self.lvl_idx == 0:
        self.screen.blit(self.tutorial_bg_surf, (0, 0))
      else:
        self.screen.blit(self.bg_surf, (0, 0))
     
      # Draw presents to the screen 
      self.present_manager.draw_presents()
        
      # Draw the player
      self.player.update_position()
      self.player.blit()

      # Update and draw evil santa
      if self.lvl_idx not in self.no_santa:
        self.evil_santa.update_position()
        self.evil_santa.blit()
    
      # Check for collisions between the player and the presents
      self.present_manager.check_collect_presents()
    
      # Draw the powerups to the screen
      self.powerups.blit()
        
      # Display the score
      self.present_manager.show_score()
  
      # Display the number of deaths
      self.stats.show_deaths()
    
    # Show the user the updated display
    pygame.display.update()


if __name__ == '__main__':
  game = SnowStrider()
  game.run_game()
