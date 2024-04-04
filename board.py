"""
Method to draw the board
uses parameters for width(how many colors to guess)
height(total/maximum amount of guesses per turn),
active colors(how many different colors are active in game)
"""


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
        """
        display the current board
        """
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        info = pygame.display.Info()
        self.set_screen_size(info)

        screen = pygame.display.set_mode((self.screen_width,
                                          self.screen_height),
                                         pygame.SCALED)
        pygame.display.set_caption("Mastermind")

        # Colors
        BLACK = (0, 0, 0)

        # Main loop
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw
            screen.fill(BLACK)
            screen = self.draw_grid(screen)
            screen = self.draw_toolbox_bg(screen)
            screen = self.draw_toolbox_active_colors(screen)
            screen = self.draw_toolbox_submit_button(screen)
            screen = self.draw_guesses(screen)
            # Add drawing functions here

            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def draw_grid(self, screen):
        LINE = (255, 255, 255)
        for i, j in zip_longest(range(0, self.board_height+1),
                                range(0, self.board_width+1),
                                fillvalue=0):
            pygame.draw.line(screen, LINE, (self.padding_lft_rgt,
                                            self.padding_up_down+(
                                                self.cell_size*i)),
                                           (self.padding_lft_rgt+(
                                            self.cell_size*self.board_width),
                                            self.padding_up_down+(
                                                self.cell_size*i)))

            pygame.draw.line(screen, LINE, (self.padding_lft_rgt+(
                                            self.cell_size*j),
                                            self.padding_up_down),
                                           (self.padding_lft_rgt+(
                                            self.cell_size*j),
                                            self.padding_up_down+(
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
                center_h = self.screen_height-self.padding_up_down-(
                    (id_g*self.cell_size)
                    + self.cell_size/2)
                pygame.draw.circle(screen, c.value,
                                   (center_w, center_h),
                                   (self.cell_size/2)*0.8)
        return screen

    def draw_toolbox_bg(self, screen):
        color = (55, 55, 55)
        pygame.draw.rect(screen, color, (((self.board_w-self.toolbox_size[0])
                                          + self.padding_lft_rgt),
                                         self.padding_up_down,
                                         self.toolbox_size[0],
                                         self.toolbox_size[1]), 0, 5)
        return screen

    def draw_toolbox_active_colors(self, screen):
        toolbox_color_size = self.toolbox_size[1]*0.66 / len(
            self.active_colors)
        for id_c, color in enumerate([color() for color
                                      in self.active_colors], 1):
            center_h = (id_c*toolbox_color_size)+self.padding_up_down
            center_w = (self.screen_width -
                        (self.padding_lft_rgt+toolbox_color_size))
            pygame.draw.circle(screen, color.value, (center_w, center_h),
                               (toolbox_color_size*0.45))
        return screen

    def draw_toolbox_submit_button(self, screen):
        color = (55, 255, 55)
        pygame.draw.rect(screen, color, (
            ((self.board_w-self.toolbox_size[0] + self.padding_lft_rgt) + self.toolbox_size[0]*0.1),
            (self.padding_up_down + self.toolbox_size[1] - self.toolbox_size[1] * 0.15),
            self.toolbox_size[0]-(self.toolbox_size[0]*0.2),
            self.toolbox_size[1]/10),
            0, 5)
        return screen

    def set_screen_size(self, info):
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.padding_up_down = self.screen_height*0.05
        self.padding_lft_rgt = self.screen_width*0.05
        self.board_h = self.screen_height-(2*self.padding_up_down)
        self.board_w = self.screen_width-(2*self.padding_lft_rgt)
        self.toolbox_size = (self.board_w/3, self.board_h)
        cell_max_width = (self.board_w-self.toolbox_size[0])/self.board_width
        cell_max_height = self.board_h/self.board_height
        self.cell_size = min(cell_max_width, cell_max_height)


Board(GameParams(7))
