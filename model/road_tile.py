import pygame
from constants import TILE_SIZE, C1_COLOR, C2_COLOR


class RoadTile:
    '''Class representing a road tile in the game.
    Attributes:
        col (int): The column index of the tile in the grid.
        row (int): The row index of the tile in the grid.
        sprite (pygame.Surface | None): The surface representing the tile's appearance. Initialized as None.
        Methods:
            get_sprite(tile_size: int = TILE_SIZE) -> pygame.Surface: Returns the sprite for the tile, creating it if necessary.
    '''

    def __init__(self, col: int, row: int):
        '''Initializes a RoadTile with the specified column and row indices.
            
            Parameters:
                col (int): The column index of the tile in the grid.
                row (int): The row index of the tile in the grid.
        '''
        self.col = col
        self.row = row
        self.sprite: pygame.Surface | None = None


    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        '''Returns the sprite for the tile, creating it if necessary.
            
            Parameters:
                tile_size (int): The size of the tile in pixels. Default is TILE_SIZE.
            Returns:
                pygame.Surface: The surface representing the tile's appearance.
        '''
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill((80, 80, 90))
        pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite
