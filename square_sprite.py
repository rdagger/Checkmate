"""Square sprite."""
from pygame import Color, draw, Rect, sprite, Surface
from pygame.locals import SRCALPHA

SQUARE = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]


class SquareSprite(sprite.Sprite):
    """Create class for tail sprites that are hollow squares."""

    def __init__(self, position, cell_size, color):
        """Square sprite constructor.

        Args:
            position((int, int)): X, Y coordinates.
            cell_size (int): length of the enclosing square.
            color((int, int, int)): RGB color.
        """
        super().__init__()

        self.cell_size = cell_size
        self.color = color
        self.image = Surface((self.cell_size, self.cell_size), SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.draw_shape()

    def draw_shape(self):
        """Draw sprite using square dict."""
        self.image.fill(Color(0, 0, 0, 0))  # Transparent fill
        cell_size = self.cell_size // len(SQUARE)
        for row in range(len(SQUARE)):
            for col in range(len(SQUARE[row])):
                if SQUARE[row][col] == 1:
                    cell_rect = Rect(col * cell_size, row * cell_size,
                                     cell_size, cell_size)
                    draw.rect(self.image, self.color, cell_rect)
