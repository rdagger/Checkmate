"""Checkmate game board."""
from game_fonts import GameFonts, Size
from hash_sprite import HashSprite
from os import path
from pygame import Color, draw, event, image, Rect, transform, quit
from pygame.locals import KEYDOWN, KEYUP, QUIT
from square_sprite import SquareSprite


PLAYER_COLOR = {
    1: Color("red"),
    2: Color("green"),
    3: Color("green"),
    4: Color("red")
    }

HORIZONTAL_CELLS = 39  # Horizontal cells on play area grid
VERTICAL_CELLS = 21  # Vertical cells on play area grid


class Board:
    """Checkmate game board."""

    def __init__(self, screen_width, screen_height, cell_size,
                 cocktail, key_select, key_exit, display_logo, sounds):
        """Create game board.

        Args:
            screen_width (int): Overall screen width of game.
            screen_height (int): Overall screen height of game.
            cell_size (int): Size of cells on the play area grid.
            cocktail (bool): True if cocktail cabinet.
            key_select(pygame.key): Keyboard key for selection
            key_exit(pygame.key): Keyboard key to exit game
            display_logo (bool): True to display Astrocade logo.
            sounds(class): Game sounds
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Cell size determines dimensions of play area
        self.cell_size = cell_size
        self.play_width = HORIZONTAL_CELLS * self.cell_size
        self.play_height = VERTICAL_CELLS * self.cell_size
        assert self.play_width < screen_width, \
            "Cell size is too large for screen width."
        assert self.play_height * 1.1 < screen_height, \
            "Cell size is too large for screen height."

        self.fonts = GameFonts()
        self.sounds = sounds

        # Create the PLAY_AREA rectangle
        self.play_area = Rect((self.screen_width - self.play_width) // 2,
                              (self.screen_height - self.play_height) // 2,
                              self.play_width,
                              self.play_height)

        # Set up grid to ensure sprites are initially aligned with board
        self.grid = []
        # Loop through the play area in cell size increments
        for y in range(self.play_area.top, self.play_area.bottom,
                       self.cell_size):
            y = y + (self.cell_size // 2)
            row = []
            for x in range(self.play_area.left, self.play_area.right,
                           self.cell_size):
                x = x + (self.cell_size // 2)
                row.append((x, y))
            # Add the row list to the grid_coordinates
            self.grid.append(row)

        # Find the grid row closest to the center
        center_row = len(self.grid) // 2
        # Find the grid column closest to the center
        center_column = len(self.grid[0]) // 2
        quarter_column = len(self.grid[0]) // 4
        quarter_row = len(self.grid) // 4
        # Player start coordinates
        self.start_coords = {
            1: self.grid[center_row][quarter_column],
            2: self.grid[center_row][quarter_column + center_column],
            3: self.grid[quarter_row][center_column],
            4: self.grid[quarter_row + center_row][center_column]
        }
        self.cocktail = cocktail
        self.key_select = key_select
        self.key_exit = key_exit
        self.display_logo = display_logo  # Configure Astrocade logo
        if self.display_logo:
            self.logo = image.load(path.join("images", "astrocade.png"))
            if self.cocktail:
                self.logo_rect = self.logo.get_rect(
                    centerx=self.play_area.centerx, top=0)
            else:
                self.logo_rect = self.logo.get_rect(
                    centerx=self.play_area.centerx, bottom=screen_height - 1)

    def draw(self,  screen, color):
        """Draw the play area.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
            color((int, int, int)): RGB background color of play area.
        """
        draw.rect(screen, color, self.play_area, 0)

    def display_score(self, scores, games, screen, background):
        """Display score on screen.

        Args:
            scores([int,int,int,int]): All 4 player scores.
            games(int): Game rounds left.
            screen(pygame.Surface): Graphical window to display graphics.
            background:((int, int, int)): Score box background color.
        """
        score_box_width = ((self.play_area.width) - (self.cell_size * 7)) // 4

        for index in range(4):
            if index == 0:
                xpos = self.play_area.left + self.cell_size // 2
                num_text = "1"  # Player 1
            elif index == 1:
                xpos += score_box_width + self.cell_size
                num_text = "3"  # Player 3
            elif index == 2:
                xpos += score_box_width + (self.cell_size * 4)
                num_text = "4"  # Player 4
            elif index == 3:
                xpos += score_box_width + self.cell_size
                num_text = "2"  # Player 2

            color = PLAYER_COLOR[int(num_text)]
            score_text = f"{scores[int(num_text) - 1]:0>3}"
            # Draw box containing score
            score_box = Rect(xpos,
                             self.play_area.top - (self.cell_size * 3),
                             score_box_width,
                             (self.cell_size * 2))
            draw.rect(screen, background, score_box, 0)
            # Draw player number
            num_width, num_height = self.fonts.measure(num_text, Size.MEDIUM)
            num_x = score_box.left + self.cell_size
            num_y = score_box.centery - (num_height // 2)
            self.fonts.draw(num_text,
                            Size.MEDIUM,
                            (num_x, num_y),
                            screen,
                            color)
            # Draw sprite
            sprite_x = num_x + num_width + self.cell_size // 1.5
            sprite_y = score_box.centery

            if index > 1:
                sprite = SquareSprite(position=(sprite_x, sprite_y),
                                      cell_size=self.cell_size,
                                      color=color)
            else:
                sprite = HashSprite(position=(sprite_x, sprite_y),
                                    cell_size=self.cell_size,
                                    color=color)
            screen.blit(sprite.image, sprite.rect)

            # Draw score
            score_width, score_height = self.fonts.measure(score_text,
                                                           Size.SMALL)
            score_X = sprite_x + self.cell_size * 1.5
            score_y = score_box.centery - (score_height // 2.2)
            self.fonts.draw(score_text,
                            Size.SMALL,
                            (score_X, score_y),
                            screen,
                            color)

        # Draw game round
        game_text = f"{games:0>2}"
        game_width, game_height = self.fonts.measure(game_text,
                                                     Size.SMALL)
        game_X = self.play_area.centerx - (game_width // 2)
        game_y = score_box.centery - (game_height // 2.2)
        self.fonts.draw(game_text,
                        Size.SMALL,
                        (game_X, game_y),
                        screen,
                        background)

        if self.display_logo:
            screen.blit(self.logo, self.logo_rect)  # Astrocade Logo

        # Prepare cocktail mode flipped display
        if self.cocktail:
            hud_rect = Rect(0, 0, self.screen_width,
                            self.play_area.topleft[1] - 1)
            hud = screen.subsurface(hud_rect).copy()
            rotated_hud = transform.rotate(hud, 180)
            screen.blit(rotated_hud,
                        (0, self.play_area.bottomleft[1] + 1))

    def game_over(self, screen, display):
        """Display game over and wait for select key press and release.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
            display(pygame.display): Visual output.
        """
        game_text = "GAME"
        _, game_height = self.fonts.measure(game_text, Size.HUGE)
        game_y = self.play_area.centery - game_height * .8
        self.fonts.draw(game_text,
                        Size.HUGE,
                        (self.play_area.centerx, game_y),
                        screen,
                        Color("green"),
                        background=Color("yellow"),
                        center=True)

        over_text = "OVER"
        self.fonts.draw(over_text,
                        Size.HUGE,
                        self.play_area.center,
                        screen,
                        Color("green"),
                        background=Color("yellow"),
                        center=True)
        display.flip()
        waiting = True
        while waiting:  # Pause until CTRL pressed or ESC to quit
            for e in event.get():
                if (e.type == QUIT or
                        e.type == KEYDOWN and e.key == self.key_exit):
                    quit()
                    exit()
                elif e.type == KEYUP and e.key == self.key_select:
                    waiting = False

    def game_start(self, games, scores, screen, display):
        """Display game start count down.

        Args:
            games(int): Number of games.
            scores((int,int,int,int)): Player scores.
            screen(pygame.Surface): Graphical window to display graphics.
            display(pygame.display): Visual output.
        """
        screen.fill(Color('blue'))  # Game background
        self.draw(screen, Color("yellow"))  # Play area
        self.display_score(scores, games,
                           screen, Color("yellow"))  # Player scores

        # Draw player numbers at starting positions
        for index in range(1, 5):  # Draw player numbers at starting positions
            flip = True if self.cocktail and not index % 2 else False
            self.fonts.draw(str(index),
                            Size.MEDIUM,
                            self.start_coords[index],
                            screen,
                            PLAYER_COLOR[index],
                            center=True,
                            flip=flip)

        digits = ["lll", " ll ", " l "] if self.cocktail else ["3", "2", " 1 "]
        for count in range(3):  # Draw count down
            self.fonts.draw(digits[count],
                            Size.HUGE,
                            (self.start_coords[3][0], self.play_area.centery),
                            screen,
                            Color("blue"),
                            background=Color("yellow"),
                            center=True)
            display.flip()
            self.sounds.play(str(3 - count), delay=800)
