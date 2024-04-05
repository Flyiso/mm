import os
import cv2
import pygame
import random
import shutil
import numpy as np
from PIL import Image, ImageDraw


class ColorSlides:
    """
    Class to generate color slides to loop through
    """
    def __init__(self, active_colors: list, height,
                 width) -> None:
        """
        Create images to use for color slides animations.

        Parameters:
            active_colors (list[GameParams.Color]):
                    List of currently, in game, active colors.
                    List content should be color objects from
                    Color class in game_values.py
            height (int):
                    height of the field to create images for.
                    set height of the image (from 0)
            width (int):
                    width of the field to create images for.
                    sets width of the image (from 0)
        """
        # remove frames if any.
        if os.path.exists('frames'):
            directory_path = os.path.join(os.getcwd(), 'frames')
            shutil.rmtree(directory_path)

        self.height = height
        self.width = width
        self.colors = [color() for color in active_colors]
        self.n_val_shown = (self.height//self.width)+2
        height_adjust = [(((width/2)/5) * n) for n in range(0, 6)]
        for col in height_adjust[1:]:
            height_adjust.append(-col)
        height_adjust.sort(reverse=True)
        self.height_adjust = height_adjust
        self.get_images()

    def get_images(self):
        """
        Loop through each color, and each position in animation
        each color can have to create images for animation.
        """
        for color_id, color in enumerate(self.colors):
            for frame_id, \
                height_adjustment \
                    in enumerate(self.height_adjust[:-1]):
                active_slot_width, active_slot_height = \
                    (self.width/2, self.height/2 + height_adjustment)
                slots_up = -(active_slot_height // -self.width)
                slots_down = -((self.height-active_slot_height) // -self.width)

                up_colors = [self.colors[slot % (len(self.colors))] for slot
                             in range(
                                 ((color_id)-int(slots_up)), color_id)]

                down_colors = [self.colors[(color_id+(slot_d)) -
                                           (((color_id+1+slot_d) //
                                            (len(self.colors))) *
                                            len(self.colors))]
                               for slot_d in range(1, int(slots_down)+1)]

                self.create_image(color_id, frame_id,
                                  active_slot_width, active_slot_height,
                                  color, reversed(up_colors), down_colors)

    def create_image(self, color_index: int, frame_index: int,
                     active_slot_width, active_slot_height,
                     color, up_colors: list, down_colors: list):
        """
        creates and
        saves image in folder 'frames',

        parameters:
            color_index(int):
                the index of the current color
            frame_index(int):
                What index of current color/ allow
                one color to be valid during multiple frames.
            active_slot_width:
                horizontal co-ordinate for active slot/color
            active_slot_height:
                vertical co-ordinate for active slot/color
            color(GameParams.Color):
                currently active color/center color of frame.
            up_colors(list[GameParams.Color]):
                list of colors(GameParams.Color) visible above
                center color.(first one closest to main color)
            down_colors(list[GameParams.COlor]):
                list of colors(GameParams.Color) visible below
                center color.(firs one closest to main color)
        """

        if len(str(color_index)) == 1:
            color_index = f'0{color_index}'
        if len(str(frame_index)) == 1:
            frame_index = f'0{frame_index}'
        folder_path = 'frames'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        image = Image.new("RGBA", (int(self.width), int(self.height)),
                          (0, 0, 0, 0))

        center = [int(active_slot_width), int(active_slot_height)]
        radius = (active_slot_width*0.85)
        draw_color = color.value + (255,)

        draw = ImageDraw.Draw(image)
        draw.ellipse((center[0] - radius, center[1] - radius,
                     center[0] + radius, center[1] + radius),
                     fill=draw_color)
        draw.ellipse((center[0] - radius*0.33, center[1] - radius*0.33,
                     center[0] + radius*0.33, center[1] + radius*0.33),
                     fill=(0, 0, 0, 255))

        for color_u in up_colors:
            center[1] -= (active_slot_width*2)
            draw_color = color_u.value + (255, )
            draw.ellipse((center[0] - radius, center[1] - radius,
                         center[0] + radius, center[1] + radius),
                         fill=draw_color)

        center = [int(active_slot_width), int(active_slot_height)]

        for color_d in down_colors:
            center[1] += active_slot_width*2
            draw_color = color_d.value + (255,)
            draw.ellipse((center[0] - radius, center[1] - radius,
                         center[0] + radius, center[1] + radius),
                         fill=draw_color)

        img_pathname = \
            f'{folder_path}/{color_index}_{frame_index}_{color.name}.png'
        image.save(img_pathname)


class RollField(object):
    def __init__(self, top_left: tuple, top_right: tuple,
                 bottom_left: tuple, bottom_right: tuple,
                 frames: list):
        """
        create roll object with perspective transformed
        version of frame to make frame fit roll field.
        """
        self.time = 0
        self.stop = False
        self.itter_interval = 0
        self.spinning = True
        self.speed_modifier = (random.randint(45, 77))*0.01
        self.main_top_left = (int(top_left[0]), int(top_left[1]))
        self.main_top_right = (int(top_right[0]), int(top_right[1]))
        self.main_bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
        self.main_bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

        self.width_start = (min(self.main_top_left[0],
                            self.main_bottom_left[0],
                            self.main_bottom_right[0],
                            self.main_top_right[0]))
        self.height_start = self.main_top_left[1]
        self.frame_paths = frames
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
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
        frame = cv2.warpPerspective(frame, self.matrix,
                                    (frame.shape[1], frame.shape[0]),
                                    flags=cv2.INTER_NEAREST)
        return pygame.image.frombuffer(frame.tobytes(),
                                       frame.shape[1::-1],
                                       'RGBA')

    def draw_roller_on_frame(self, frame, time):
        """
        Returns frame with roller drawn on it
        """
        if self.stop is True and self.itter_interval >= self.time:
            return self.slow_roller(frame, time)

        else:
            self.itter_interval += 1
            frame = frame.blit(self.frames[self.current_index],
                               (self.width_start, self.height_start))
            if self.spinning:
                self.current_index += 1
            if self.current_index > self.index_max:
                self.current_index = 0
            return frame

    def slow_roller(self, frame, time):
        if self.itter_interval > self.time and self.time > 0:
            dist = ((time*(2+(self.speed_modifier*10))) -
                    self.end_time)*0.00001
            speed = (self.speed_modifier-dist)
            self.time = abs(speed*(self.speed_modifier*100))-0.3
            self.itter_interval = 0
            frame = frame.blit(self.frames[self.current_index-1],
                               (self.width_start, self.height_start))
            return frame

        else:
            frame = frame.blit(self.frames[self.current_index],
                               (self.width_start, self.height_start))
            self.spinning = False
            if self.current_index >= self.index_max:
                self.current_index = 0
            self.frame_name = self.frame_paths[self.current_index]
            return frame

    def stop_roller(self, time):
        """
        slow the frame down exponentially.
        """
        self.time = time/10
        self.end_time = time
        self.itter_interval = 0
        self.stop = True

    def start_roller(self, time):
        print('RESTART...')
        self.time = 0
        self.stop = False
        self.itter_interval = 0
        self.end_time = time
        self.spinning = True
