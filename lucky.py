from colorslides import ColorSlides
from game_values import GameParams
from itertools import zip_longest
import numpy as np
import shutil
import random
import pygame
import sys
import os
import cv2


class Board:
    def __init__(self,
                 game_params: GameParams = GameParams()) -> None:
        self.board_width = game_params.n_slots
        self.board_height = game_params.n_turns
        self.active_colors = game_params.active_colors
        self.win_colors = game_params.correct
        self.guesses = []
        self.roll_fields = []
        self.draw_board()

    def draw_board(self):
        pygame.init()
        clock = pygame.time.Clock()
        info = pygame.display.Info()
        self.set_screen_values(info)
        ColorSlides(self.active_colors, self.field_height,
                    self.field_width)
        directory_path = os.path.join(os.getcwd(), 'frames')
        self.spin_frames_routes = [(os.path.join(directory_path, frame))
                                   for frame in os.listdir(directory_path)]
        for field in range(int(self.board_width)):
            self.roll_fields.append(RollField(
                top_left=(self.display_top_left[0] +
                          (self.roller_width_top * field),
                          self.display_top_left[1]),
                top_right=(self.display_top_left[0] +
                           self.roller_width_top * (field+1),
                           self.display_top_right[1]),
                bottom_left=(self.display_bottom_left[0] +
                             (self.roller_width_bottom * field),
                             self.display_bottom_left[1]),
                bottom_right=(self.display_bottom_left[0] +
                              (self.roller_width_bottom * (field + 1)),
                              self.display_bottom_right[1]),
                frames=self.spin_frames_routes,
                width_top=int(self.roller_width_top),
                width_btm=int(self.roller_width_bottom)))

        screen = pygame.display.set_mode((self.screen_width,
                                         self.screen_height))
        pygame.display.set_caption("Mastermind For lucky people")

        self.black = (0, 0, 0)
        self.gray = (125, 125, 241)
        self.red = (225, 50, 50)
        self.green = (50, 255, 25)
        self.line_color = (225, 225, 225)

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # draw background.
            screen.fill(self.black)
            screen = self.draw_grid(screen)
            screen = self.draw_guesses(screen)
            screen = self.draw_background(screen)
            screen = self.draw_display(screen)
            [roll_field.draw_roller_on_frame(screen) for
             roll_field in self.roll_fields]
            screen = self.draw_roller_fields(screen)
            screen = self.draw_buttons(screen)
            pygame.display.flip()

            # Cap the frame rate
            # pygame.time.Clock().tick(60)
            clock.tick(1)

        # Remove directory of images.
        if os.path.exists('frames'):
            directory_path = os.path.join(os.getcwd(), 'frames')
            shutil.rmtree(directory_path)
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

    def draw_guesses(self, screen):
        """
        Print guesses in grid.
        """
        for id_g, guess_sequence in enumerate(self.guesses, 0):
            for id_c, c in enumerate([c() for c in guess_sequence], 0):
                center_w = self.padding_lft_rgt+((id_c*self.cell_size)
                                                 + self.cell_size/2)
                center_h = ((self.padding_lft_rgt+(self.cell_size *
                                                   self.board_height) -
                            self.cell_size/2) -
                            (self.cell_size*id_g))
                pygame.draw.circle(screen, c.value,
                                   (center_w, center_h),
                                   (self.cell_size/2)*0.8)
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
        pygame.draw.polygon(screen, self.black, (self.display_top_left,
                                                 self.display_top_right,
                                                 self.display_bottom_right,
                                                 self.display_bottom_left))
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
        pygame.draw.rect(screen, self.green, (
            self.button_start_width, self.button_height,
            self.button_size, self.button_size), 0, 2)

        pygame.draw.rect(screen, self.red, (
            self.button_end_width, self.button_height,
            self.button_size, self.button_size), 0, 2)
        return screen

    def set_screen_values(self, info):
        # grid for guesses display and frame settings.
        self.screen_height = info.current_h
        self.cell_size = ((self.screen_height * 0.67)/self.board_height) * 0.97
        self.screen_width = ((self.cell_size * 1.02) * self.board_width)
        self.padding_lft_rgt = self.screen_width * 0.01
        self.padding_up_down = self.screen_height + 0.01
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

        self.field_width = ((int(self.display_bottom_right[0] +
                            self.display_top_right[0]) -
                            (int(self.display_bottom_left[0] +
                             self.display_top_left[0]) / 2))
                            / self.board_width)
        self.field_height = (int(self.display_bottom_left[1] +
                                 self.display_top_left[1]) / 2)

        self.roller_width_top = (self.display_top_right[0] -
                                 self.display_top_left[0]) / self.board_width
        self.roller_width_bottom = (self.display_bottom_right[0] -
                                    self.display_bottom_left[0]
                                    ) / self.board_width

        # Button placement
        self.button_height = \
            self.display_bottom_left[1]+(self.screen_height//15)
        self.button_size = self.screen_height//20
        self.button_start_width = self.screen_width-(self.button_size*3)
        self.button_end_width = self.button_start_width+(self.button_size*1.5)


class RollField(object):
    def __init__(self, top_left: tuple, top_right: tuple,
                 bottom_left: tuple, bottom_right: tuple,
                 frames: list, width_top: int, width_btm: int):
        """
        create roll object with perspective transformed
        version of frame to make frame fit roll field
        """
        self.main_top_left = (int(top_left[0]), int(top_left[1]))
        self.main_top_right = (int(top_right[0]), int(top_right[1]))
        self.main_bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
        self.main_bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        width = max(self.main_top_left[0], self.main_top_right[0],
                    self.main_bottom_left[0], self.main_bottom_right[0])

        self.width_start = (min(self.main_top_left[0],
                            self.main_bottom_left[0],
                            self.main_bottom_right[0],
                            self.main_top_right[0]))
        self.height_start = self.main_top_left[1]
        frame_vals = cv2.imread(frames[1])
        frame_vals = frame_vals.shape

        self.matrix = cv2.getPerspectiveTransform(
            np.float32([[0, frame_vals[0]], [frame_vals[1], frame_vals[0]],
                        [0, 0], [frame_vals[1], 0]]),
            np.float32(([
                        (self.main_bottom_left[0]-self.width_start,
                         self.main_bottom_left[1]-self.height_start),

                        (self.main_bottom_right[0]-self.width_start,
                         self.main_bottom_right[1]-self.height_start),

                        (self.main_top_left[0]-self.width_start,
                         self.main_top_left[1]-self.height_start),

                        (self.main_top_right[0]-self.width_start,
                         self.main_top_right[1]-self.height_start)
                        ])))
        self.frames = [self.adjust_frame(frame) for frame in frames]
        self.index_max = len(self.frames)-1
        self.current_index = 0

    def adjust_frame(self, frame):
        """
        return frame to fit coordinate proportions
        """
        frame = cv2.imread(frame, cv2.IMREAD_UNCHANGED)
        frame = cv2.warpPerspective(frame, self.matrix,
                                    (frame.shape[1], frame.shape[0]),
                                    flags=cv2.INTER_NEAREST)
        return pygame.image.frombuffer(frame.tobytes(),
                                       frame.shape[1::-1],
                                       'RGBA')

    def draw_roller_on_frame(self, frame):
        """
        Returns frame with roller drawn on it
        """
        frame = frame.blit(self.frames[self.current_index],
                           (self.width_start, self.height_start))
        self.current_index += 1
        
        if self.current_index > self.index_max:
            self.current_index = 0
        return frame


Board(GameParams(9, 5))
