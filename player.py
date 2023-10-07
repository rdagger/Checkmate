"""Both human and computer players."""
from hash_sprite import HashSprite
from head_sprite import HeadSprite
from pygame import Color, sprite
from random import choice
from square_sprite import SquareSprite

DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)

START_DIRECTIONS = [RIGHT, LEFT, DOWN, UP]

PLAYER_COLORS = {
    1: Color('red'),
    2: Color('green'),
    3: Color('green'),
    4: Color('red')
}


class Player:
    """Checkmate player."""

    def __init__(self, id, human, start_position, cell_size):
        """Create player.

        Args:
            id (int): Player number
            human (bool): True=Human, False=Computer
            start_position ((int, int)): Grid row and column to start
            cell_size (int): Length of the enclosing square for each cell.
        """
        self.id = id
        self.human = human
        self.start_position = start_position
        self.position = start_position
        self.direction = choice(START_DIRECTIONS)
        self.color = PLAYER_COLORS[self.id]
        self.alive = True
        self.score = 0
        self.tail = sprite.Group()
        self.cell_size = cell_size

    def enqueue(self):
        """Extend snake tail tail by 1 segment."""
        if self.tail:
            sprites = self.tail.sprites()
            head = sprites[0]
            previous_head_position = head.rect.center
            head.rect.center = self.position  # Move snake head to front
            head.rotate(self.direction)  # Ensure head facing correctly
            if self.id % 2:  # Add hash shaped body segment
                self.tail.add(HashSprite(position=previous_head_position,
                                         cell_size=self.cell_size,
                                         color=self.color))
            else:  # Add square shaped body segment
                self.tail.add(SquareSprite(position=previous_head_position,
                                           cell_size=self.cell_size,
                                           color=self.color))
        else:
            # Add head to empty snake
            self.tail.add(HeadSprite(position=self.position,
                                     direction=self.direction,
                                     cell_size=self.cell_size))
        # Play tone that matches player's ID & direction

    def get_move(self, direction):
        """Return new player coordinates based on direction.

        Args:
            direction((int, int)): X, Y direction
        """
        return (self.position[0] + direction[0] * self.cell_size,
                self.position[1] + direction[1] * self.cell_size)

    def get_moves(self):
        """Return the 3 possible move locations for a player."""
        up = (self.position[0] + UP[0] * self.cell_size,
              self.position[1] + UP[1] * self.cell_size)
        down = (self.position[0] + DOWN[0] * self.cell_size,
                self.position[1] + DOWN[1] * self.cell_size)
        left = (self.position[0] + LEFT[0] * self.cell_size,
                self.position[1] + LEFT[1] * self.cell_size)
        right = (self.position[0] + RIGHT[0] * self.cell_size,
                 self.position[1] + RIGHT[1] * self.cell_size)

        if self.direction == UP:
            return (up, left, right)
        elif self.direction == DOWN:
            return (down, right, left)
        elif self.direction == LEFT:
            return (left, down, up)
        elif self.direction == RIGHT:
            return (right, up, down)

    def left(self):
        """Change direction left relative to current direction."""
        if self.direction == UP:
            self.direction = LEFT
        elif self.direction == DOWN:
            self.direction = RIGHT
        elif self.direction == LEFT:
            self.direction = DOWN
        elif self.direction == RIGHT:
            self.direction = UP

    def kill(self):
        """Kill player."""
        self.alive = False
        self.tail.empty()
        self.position = self.start_position

    def move(self):
        """Advance player 1 move."""
        x = self.position[0] + self.direction[0] * self.cell_size
        y = self.position[1] + self.direction[1] * self.cell_size
        self.position = (x, y)

    def random_direction(self, left_safe, right_safe):
        """Change player direction randomly if possible.

        Args:
            left_safe(bool): Safe to turn relative left
            right_safe(bool): Safe to turn relative right
        """
        if left_safe and right_safe:  # Both safe
            # Pick randomly
            self.left() if choice([True, False]) else self.right()
        elif left_safe:  # Only left safe
            self.left()
        elif right_safe:  # Only right safe
            self.right()

    def reset(self):
        """Reset player."""
        self.alive = True
        self.tail.empty()
        self.position = self.start_position
        self.direction = choice(START_DIRECTIONS)

    def right(self):
        """Change direction right relative to current direction."""
        if self.direction == UP:
            self.direction = RIGHT
        elif self.direction == DOWN:
            self.direction = LEFT
        elif self.direction == LEFT:
            self.direction = UP
        elif self.direction == RIGHT:
            self.direction = DOWN
