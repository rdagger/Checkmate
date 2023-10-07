"""Checkmate game options."""
from game_fonts import GameFonts, Size
from pygame import Color, draw, display, event, quit
from pygame.locals import KEYDOWN, QUIT

MAX_PLAYERS = 4
MAX_GAMES = 99


class Options:
    """Checkmate game options."""

    def __init__(self, key_select, key_decrement, key_increment, key_exit):
        """Game options constructor.

        Args:
            key_select(pygame.key): Keyboard key for selection
            key_decrement(pygame.key): Keyboard key to increment value
            key_increment(pygame.key): Keyboard key to decrement value
            key_exit(pygame.key): Keyboard key to exit game
        """
        self.games = 3  # Number of games
        self.players = 1  # Number of players
        self.key_select = key_select
        self.key_decrement = key_decrement
        self.key_increment = key_increment
        self.key_exit = key_exit

    def prompt(self, screen, play_area):
        """Prompt for the number of games and players.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
            play_area(Rect): Rectangle bounding the play area.
        """
        fonts = GameFonts()
        title_text = "CHECKMATE"
        players_text = "ENTER # OF PLAYERS"
        games_text = "ENTER # OF GAMES"

        _, y_offset = fonts.measure(players_text, Size.LARGE)

        input = "players"
        while True:
            for e in event.get():
                if (e.type == QUIT or
                        e.type == KEYDOWN and e.key == self.key_exit):
                    quit()
                    exit()
                if e.type == KEYDOWN:
                    if e.key == self.key_decrement:
                        if input == "players" and self.players > 0:
                            self.players -= 1
                        elif input == "games" and self.games > 1:
                            self.games -= 1
                    elif e.key == self.key_increment:
                        if input == "players" and self.players < MAX_PLAYERS:
                            self.players += 1
                        elif input == "games" and self.games < MAX_GAMES:
                            self.games += 1
                    elif e.key == self.key_select:
                        if input == "players":
                            input = "games"
                        else:
                            return

            screen.fill(Color('red'))  # Background color
            draw.rect(screen, Color('white'), play_area, 0)  # Play area
            # Checkmate title
            _, title_height = fonts.measure(title_text, Size.LARGE)
            title_x = play_area.centerx // 2
            title_y = play_area.top - (title_height * 1.25)
            fonts.draw(title_text, Size.LARGE, (title_x, title_y),
                       screen, Color("white"))
            # Set input either players or games
            input_text = players_text if input == "players" else games_text
            input_value = self.players if input == "players" else self.games
            # Draw input prompt and value
            fonts.draw(input_text, Size.LARGE,
                       (play_area.centerx, play_area.centery - y_offset),
                       screen, Color("blue"), center=True)
            fonts.draw(str(input_value), Size.HUGE,
                       (play_area.centerx, play_area.centery + y_offset),
                       screen, Color("blue"), center=True)
            display.flip()
