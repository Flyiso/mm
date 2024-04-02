from game_values import GameParams
from itertools import zip_longest
import random
import pygame
import sys
from PIL import Image


class Board:
    def __init__(self,
                 game_params: GameParams = GameParams()) -> None:
        self.board_width = game_params.n_slots
        self.board_height = game_params.n_turns
        self.active_colors = game_params.active_colors
        self.win_colors = game_params.correct
        self.guesses = []
        self.guesses = game_params.guesses
        self.draw_board()

    def draw_board(self):
        pygame.init()
        info = pygame.display.Info()
        self.set_screen_values(info)
        screen = pygame.display.set_mode((self.screen_width,
                                         self.screen_height))
        pygame.display.set_caption("Mastermind For lucky people")

        self.black = (0, 0, 0)
        self.gray = (125, 125, 241)
        self.red = (225, 50, 50)
        self.line_color = (255, 255, 255)

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # draw background.
            screen.fill(self.black)
            screen = self.draw_grid(screen)
            screen = self.draw_background(screen)
            screen = self.draw_display(screen)
            ColorSlides(self.active_colors, self.field_height,
                        self.field_width, (1, 1, 2, 3))
            screen = self.draw_roller_fields(screen)
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def draw_grid(self, screen):
        for i, j in zip_longest(range(0, self.board_height+1),
                                range(0, self.board_width+1),
                                fillvalue=0):
            pygame.draw.line(screen, self.line_color,
                             (self.padding_lft_rgt,
                              self.padding_lft_rgt+(
                                self.cell_size*i)),

                             (self.padding_lft_rgt+(
                                self.cell_size*self.board_width),
                              self.padding_lft_rgt+(
                                self.cell_size*i)))

            pygame.draw.line(screen, self.line_color,
                             (self.padding_lft_rgt+(
                              self.cell_size*j),
                              self.padding_lft_rgt),

                             (self.padding_lft_rgt+(
                              self.cell_size*j),
                              self.padding_lft_rgt+(
                              self.cell_size*self.board_height)
                              ))
        return screen

    def draw_background(self, screen):
        pygame.draw.polygon(screen, self.gray, (
            # bottom left
            (0+self.padding_lft_rgt,
             self.screen_height),
            # mid left
            (self.screen_width // 30,
             self.screen_height - (self.screen_height // 6)),
            # top left
            (self.screen_width // 8,
             (self.screen_height // 3.2) * 2),
            # top right
            (self.screen_width - (self.screen_width // 8),
             (self.screen_height // 3.2) * 2),
            # mid right
            (self.screen_width - (self.screen_width // 30),
             self.screen_height - (self.screen_height // 6)),
            # bottom right
            (self.screen_width-self.padding_lft_rgt,
             self.screen_height)
             ))
        return screen

    def draw_display(self, screen):
        mul = 1
        self.display_top_left = ((self.screen_width // 8)
                                 + abs(self.padding_lft_rgt * mul),
                                 ((self.screen_height // 3.2) * 2) +
                                 (self.padding_lft_rgt * mul))

        self.display_top_right = ((self.screen_width - (self.screen_width
                                                        // 8)
                                   - (self.padding_lft_rgt * mul)),
                                  ((self.screen_height // 3.2) * 2) +
                                  (self.padding_lft_rgt * mul))

        self.display_bottom_left = ((self.padding_lft_rgt * mul) +
                                    (self.screen_width // 30),
                                    self.screen_height - (self.screen_height
                                                          // 6))

        self.display_bottom_right = ((self.screen_width - (self.screen_width
                                                           // 30))
                                     - abs(self.padding_lft_rgt * mul),
                                     self.screen_height - (self.screen_height
                                                           // 6))

        pygame.draw.polygon(screen, self.black, (self.display_top_left,
                                                 self.display_top_right,
                                                 self.display_bottom_right,
                                                 self.display_bottom_left))
        self.roller_width_top = (self.display_top_right[0] -
                                 self.display_top_left[0]) / self.board_width
        self.roller_width_bottom = (self.display_bottom_right[0] -
                                    self.display_bottom_left[0]
                                    ) / self.board_width
        self.field_width = (int(self.display_bottom_right[0] +
                                self.display_top_right[0]) -
                            (int(self.display_bottom_left[0] +
                                 self.display_top_left[0]) / 2))
        self.field_height = ((int(self.display_bottom_left[1] +
                                  self.display_top_left[1]) / 2) -
                             (int(self.display_bottom_left[1] +
                                  self.display_top_left[1]) / 2))
        return screen

    def draw_roller_fields(self, screen):
        pygame.draw.line(screen, self.red,
                         (int(self.display_bottom_left[0] +
                          self.display_top_left[0]) / 2,
                             int(self.display_bottom_left[1] +
                                 self.display_top_left[1]) / 2),
                         (int(self.display_bottom_right[0] +
                          self.display_top_right[0]) / 2,
                             int(self.display_bottom_left[1] +
                                 self.display_top_left[1]) / 2))

        for n in range(0, self.board_width):
            pygame.draw.line(screen, self.gray,
                             (self.display_top_left[0] +
                              (self.roller_width_top * n),
                              (self.display_top_left[1])),
                             (self.display_bottom_left[0] +
                              (self.roller_width_bottom * n),
                              self.display_bottom_left[1]), 3)

        return screen

    def draw_buttons(self, screen):
        return screen

    def set_screen_values(self, info):
        self.screen_height = info.current_h
        self.cell_size = ((self.screen_height * 0.67)/self.board_height) * 0.97
        self.screen_width = ((self.cell_size * 1.02) * self.board_width)
        self.padding_lft_rgt = self.screen_width * 0.01
        self.padding_up_down = self.screen_height + 0.01


class RollColors:
    def __init__(self, field_coords, colors) -> None:
        """
        create a roll effect for game
        input:
        field_coords: (top_left, top_right,
                       bottom_left, bottom_right)
        colors: list of colors active.
        """
        self.t_l, self.t_r, self.b_l, self.b_r = field_coords
        self.colors = colors
        self.start = random.choice(colors)

    def get_images(self):
        pass

    def spin(self):
        pass

    def current_image(self):
        pass


class ColorSlides:
    """
    Class to generate color slides to loop through
    """
    def __init__(self, active_colors: list, height,
                 width, field_coords: list | tuple) -> None:
        """
        Create images to use for color slides animations.

        Parameters:
            active_colors (list[GameParams.Color]):
                    List of currently, in game, active colors.
                    List content should be color objects from
                    Color class in game_values.py 
            height (int):
                    height of the field to create images for.
            width (int):
                    width of the field to create images for.
            field_coords (list|tuple):
                    locations for each corner of the field
                    to make images shape adjust to the relevant
                    quadrilateral field.
        """
        self.height = height
        self.width = width
        self.colors = [color() for color in active_colors]
        self.n_val_shown = (self.height//self.width)+2
        color_height_adjust = [(((width/2)/5) * n) for n in range(0, 6)]
        for col in color_height_adjust[1:]:
            color_height_adjust.append(-col)
        color_height_adjust.sort()
        self.color_height_adjust = color_height_adjust
        self.t_l, self.t_r, self.b_l, self.b_r = field_coords
        print(color_height_adjust)

    def get_images(self):
        """
        Loop through each color, and each position in animation
        each color can have to create images for animation.
        """
        for color_id, color in enumerate(self.colors):
            for frame_id, color_view in enumerate(self.color_places):
                w, h = (self.width/2, self.height + color_view)

Board(GameParams(7, 5))
