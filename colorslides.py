import os
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
