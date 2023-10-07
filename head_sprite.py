"""Sprite for snake head (includes head explosion)."""
from pygame import Color, draw, Rect, sprite, Surface, transform
from pygame.locals import SRCALPHA

HEAD = [
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 0]
]

EXPLOSION_1 = [
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
]

EXPLOSION_2 = [
    [0, 0, 0, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [0, 0, 0, 0]
]

EXPLOSION_3 = [
    [0, 0, 1, 1],
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0]
]

EXPLOSION_4 = [
    [0, 1, 0, 1],
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 1, 0]
]

ANGLES = {
    (0, 1): 180,  # Down
    (-1, 0): 90,  # Left
    (1, 0): 270,  # Right
    (0, -1): 0  # Up
}

FRAMES = [HEAD, EXPLOSION_1, EXPLOSION_2, EXPLOSION_3, EXPLOSION_4]


class HeadSprite(sprite.Sprite):
    """Create class for snake head sprite."""

    def __init__(self, position, direction, cell_size):
        """Head sprite constructor.

        Args:
            position((int, int)): X, Y coordinates.
            direction(int): Direction head is pointing (0=Up)
            cell_size (int): length of the enclosing square.
        """
        super().__init__()
        self.cell_size = cell_size
        self.color = Color("blue")  # Snake head always blue
        self.image = Surface((self.cell_size, self.cell_size), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.current_frame = 0
        self.draw_shape()
        self.direction = (0, -1)  # Use Up (zero) initial angle
        # Rotate head if necessary which will also correct direction
        if ANGLES[direction]:
            self.rotate(direction)

    def draw_shape(self):
        """Draw sprite using hash dict."""
        self.image.fill(Color(0, 0, 0, 0))  # Transparent fill
        cell_size = self.cell_size // len(FRAMES[self.current_frame])
        for row in range(len(FRAMES[self.current_frame])):
            for col in range(len(FRAMES[self.current_frame][row])):
                if FRAMES[self.current_frame][row][col] == 1:
                    cell_rect = Rect(col * cell_size, row * cell_size,
                                     cell_size, cell_size)
                    draw.rect(self.image, self.color, cell_rect)

    def update_frame(self):
        """Update the frame of the explosion animation."""
        self.current_frame += 1
        if self.current_frame >= len(FRAMES):
            # Reached the end of the animation, remove the sprite
            self.kill()
        else:
            self.draw_shape()

    def rotate(self, direction):
        """Rotate the snake head.

        Args:
            direction ((int, int)): X, Y direction.
        """
        new_angle = ANGLES[direction]
        old_angle = ANGLES[self.direction]
        angle = new_angle - old_angle
        if angle:
            self.image = transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.direction = direction
