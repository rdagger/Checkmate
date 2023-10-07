"""Pygame version of the Bally Astrocade game Checkmate."""
from configparser import ConfigParser
from game_board import Board
from game_options import Options
from game_sounds import GameSounds
from player import Player, DOWN, LEFT, RIGHT, UP
from pygame import Color, display, event, init, key, quit, time
from pygame.locals import FULLSCREEN, QUIT
from random import choices, sample
from sys import exit, modules

DIRECTIONS = {
    "up": UP,
    "down": DOWN,
    "left": LEFT,
    "right": RIGHT
}


class Game:
    """Checkmate."""

    def __init__(self):
        """Game constructor."""
        init()  # Initialize pygame library
        self.clock = time.Clock()
        # Load game settings file
        config = ConfigParser()
        config.read('settings.ini')
        # Get game settings
        screen_width = config.getint('GameSettings', 'screen_width')
        screen_height = config.getint('GameSettings', 'screen_height')
        cell_size = config.getint('GameSettings', 'cell_size')
        full_screen = config.getboolean('GameSettings', 'full_screen')
        self.cocktail = config.getboolean('GameSettings', "cocktail")
        self.countdown_each_game = config.getboolean("GameSettings",
                                                     "countdown_each_game")
        self.display_logo = config.getboolean('GameSettings', "display_logo")
        # Get keyboard input keys for each player
        self.input_keys = {}
        for player_num in range(1, 5):
            player = "Player{}".format(player_num)
            self.input_keys[player] = {}
            for direction in ["up", "down", "left", "right"]:
                key = config.get(player, f"{direction}_key")
                self.input_keys[player][direction] = getattr(
                    modules["pygame"], key)
        self.key_select = getattr(modules["pygame"],
                                  config.get("Player1", "select_key"))
        self.key_exit = getattr(modules["pygame"],
                                config.get("Player1", "exit_key"))

        self.game = 1  # Game round 1
        if full_screen:
            self.screen = display.set_mode((0, 0), FULLSCREEN)
        else:
            self.screen = display.set_mode((screen_width, screen_height))

        self.sounds = GameSounds()
        self.board = Board(screen_width, screen_height, cell_size,
                           self.cocktail, self.key_select, self.key_exit,
                           self.display_logo, self.sounds)
        self.options = Options(self.key_select,  # In game user options
                               self.input_keys["Player1"]["left"],
                               self.input_keys["Player1"]["right"],
                               self.key_exit)
        self.options.prompt(self.screen, self.board.play_area)
        self.players = [Player(id=i,
                               human=i <= self.options.players,
                               start_position=self.board.start_coords[i],
                               cell_size=self.board.cell_size
                               ) for i in range(1, 5)]
        self.board.game_start(self.options.games, (0, 0, 0, 0),
                              self.screen, display)  # Count down

    def explode(self, player):
        """Explode player's head.

        Args:
            player(class): The player to target.
        """
        self.sounds.play("explode")  # Play explosion sound
        for i in range(5):
            sprites = player.tail.sprites()
            head = sprites[0]
            head.update_frame()  # Cycle through exploding head sprites
            color = Color("White") if i % 2 else Color("Grey")
            self.render(board_color=color)
            display.flip()
            time.wait(100)

    def handle_input(self):
        """Handle keyboard input."""
        keys = key.get_pressed()
        if keys[self.key_exit]:  # Exit game
            quit()
            exit()
        # Loop through players and check for movement
        for i in range(self.options.players):
            player = "Player{}".format(self.players[i].id)
            for direction in ["up", "down", "left", "right"]:
                if keys[self.input_keys[player][direction]]:
                    if self.is_safe_position(
                            self.players[i].get_move(DIRECTIONS[direction])):
                        self.players[i].direction = DIRECTIONS[direction]

    def is_safe_position(self, position):
        """Check if a position collides with anything.

        Args:
            position(int, int): X,Y position coordinates.
        Returns:
            True if safe and False if not safe
        """
        if not self.board.play_area.collidepoint(*position):
            return False
        else:
            tails = [player.tail for player in self.players]
            for tail in tails:
                for sprite in tail:
                    if sprite.rect.collidepoint(*position):
                        return False
            return True

    def render(self, board_color=Color("yellow")):
        """Render game elements.

        Args:
            board_color((int, int, int)): RGB board color (default=yellow)
        """
        self.screen.fill(Color('blue'))  # Game background
        self.board.draw(self.screen, board_color)  # Play area

        # Draw each player's snake
        for player in self.players:
            if player.alive:
                player.tail.draw(self.screen)

        # Draw the score
        self.board.display_score([p.score for p in self.players],
                                 max(self.options.games - self.game + 1, 1),
                                 self.screen, board_color)

    def run(self):
        """Run game."""
        while self.game <= self.options.games:
            # Play tone corresponding to player number and direction
            alive_players = [player for player in self.players if player.alive]
            has_human_players = any(player.human for player in alive_players)
            speed = (f"human{len(alive_players)}" if has_human_players
                     else "computer")
            sounds = [f"{player.id}_{player.direction}_{speed}"
                      for player in self.players if player.alive]
            sound_length = self.sounds.play_mult(sounds)

            # Record the starting time of sound effect
            start_time = time.get_ticks()

            for e in event.get():
                if e.type == QUIT:
                    quit()
                    exit()

            self.handle_input()
            self.update()
            self.render()
            display.flip()

            # Calculate how much time should be spent on the current frame
            frame_time = sound_length - (time.get_ticks() - start_time)
            self.clock.tick_busy_loop(1000 / frame_time if frame_time > 0
                                      else 0)
        self.board.game_over(self.screen, display)

    def update(self):
        """Update player position and check for collisions."""
        players = sample(self.players, len(self.players))  # random order
        for player in players:
            if player.alive:
                if not player.human:  # Handle non-human movement
                    moves = player.get_moves()  # Get possible moves
                    forward_safe = self.is_safe_position(moves[0])
                    # Avoid crash if possible and occasional random change
                    if not forward_safe or choices([True, False], [1, 77])[0]:
                        left_safe = self.is_safe_position(moves[1])
                        right_safe = self.is_safe_position(moves[2])
                        player.random_direction(left_safe, right_safe)

                player.move()  # Update player position
                if not self.is_safe_position(player.position):
                    self.explode(player)
                    player.kill()  # Player crashed

                if player.alive:
                    player.enqueue()  # Add segment to snake

        # Check if round is over (only one player left)
        alive_players = [player for player in self.players if player.alive]

        if len(alive_players) <= 1:
            if len(alive_players):
                alive_players[0].score += 1
            self.game += 1

            # Reset players if there are more games
            if self.game <= self.options.games:
                for player in self.players:
                    player.reset()
                # Display count down each round if specified in settings
                if self.countdown_each_game:
                    self.board.game_start(self.options.games - self.game + 1,
                                          [p.score for p in self.players],
                                          self.screen, display)


if __name__ == "__main__":
    while True:
        game = Game()
        game.run()
