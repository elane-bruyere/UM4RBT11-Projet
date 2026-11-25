import pygame
from constants import (
    TILE_SIZE, C1_COLOR, C2_COLOR,
    ROAD_GRIP, ROAD_DRIFT_FRICTION, ROAD_TRACTION,
    ICE_GRIP, ICE_DRIFT_FRICTION, ICE_TRACTION,
    HERBE_GRIP, HERBE_DRIFT_FRICTION, HERBE_TRACTION
)
 
 
class RoadTile:
    '''Class representing a road tile in the game. [TERRA-7]
    Attributes:
        col (int): The column index of the tile in the grid.
        row (int): The row index of the tile in the grid.
        grip (float): Grip of the terrain (before GRIP_SCALE): the lower it is, the easier it is to drift.
        drift_friction (float): Share of the speed lost per frame while drifting on this terrain.
        traction (float): Coefficient applied to accelerating and braking (1 = full traction).
        block (Block | None): The block placed on this tile, if any.
        sprite (pygame.Surface | None): The visual representation of the tile.
            
            Methods:
                get_sprite(tile_size: int = TILE_SIZE) -> pygame.Surface: Returns the sprite of the tile, creating it if necessary.
    '''
 
    def __init__(self, col: int, row: int):
        '''Initializes a RoadTile with the given column and row indices.
        Parameters:
            col (int): The column index of the tile in the grid.
            row (int): The row index of the tile in the grid.
        Returns:
            None'''
        self.col = col
        self.row = row
        self.grip = ROAD_GRIP
        self.drift_friction = ROAD_DRIFT_FRICTION
        self.traction = ROAD_TRACTION
        self.block = None
        self.sprite: pygame.Surface | None = None
 
    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        '''Returns the sprite of the tile, creating it if necessary.
        Parameters:
            tile_size (int): The size of the tile in pixels. Default is TILE_SIZE.
        Returns:
            pygame.Surface: The surface representing the tile's sprite.'''
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill((80, 80, 90))
        pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)
        
        self.sprite = surface
        return self.sprite
        
class IceTile:
    '''Class representing an ice tile in the game. [TERRA-7]
    Low traction, almost impossible not to drift, almost no friction when drifting.
    Attributes:
        col (int): The column index of the tile in the grid.
        row (int): The row index of the tile in the grid.
        grip (float): Grip of the terrain (before GRIP_SCALE): the lower it is, the easier it is to drift.
        drift_friction (float): Share of the speed lost per frame while drifting on this terrain.
        traction (float): Coefficient applied to accelerating and braking (1 = full traction).
        block (Block | None): The block placed on this tile, if any.
        sprite (pygame.Surface | None): The visual representation of the tile.
 
            Methods:
                get_sprite(tile_size: int = TILE_SIZE) -> pygame.Surface: Returns the sprite of the ice tile, creating it if necessary.
    '''
    
    def __init__(self, col: int, row: int):
        '''Initializes an IceTile with the given column and row indices.
        Parameters:
            col (int): The column index of the tile in the grid.
            row (int): The row index of the tile in the grid.
        Returns:
            None'''
        self.col = col
        self.row = row
        self.grip = ICE_GRIP
        self.drift_friction = ICE_DRIFT_FRICTION
        self.traction = ICE_TRACTION
        self.block = None
        self.sprite: pygame.Surface | None = None
 
    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        '''Returns the sprite of the ice tile, creating it if necessary.
        Parameters:
            tile_size (int): The size of the tile in pixels. Default is TILE_SIZE.
        Returns:
            pygame.Surface: The surface representing the ice tile's sprite.'''
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        ice_surface = pygame.Surface((tile_size, tile_size))
        ice_surface.fill((78, 222, 212))
        pygame.draw.rect(ice_surface, (60, 60, 70), ice_surface.get_rect(), 2) 
        
            
        self.sprite = ice_surface
        return self.sprite
 
class HerbeTile:
    '''Class representing a grass tile in the game. [TERRA-7]
    Medium traction, easy to drift on, strong friction when drifting.
    Attributes:
        col (int): The column index of the tile in the grid.
        row (int): The row index of the tile in the grid.
        grip (float): Grip of the terrain (before GRIP_SCALE): the lower it is, the easier it is to drift.
        drift_friction (float): Share of the speed lost per frame while drifting on this terrain.
        traction (float): Coefficient applied to accelerating and braking (1 = full traction).
        block (Block | None): The block placed on this tile, if any.
        sprite (pygame.Surface | None): The visual representation of the tile.
 
            Methods:
                get_sprite(tile_size: int = TILE_SIZE) -> pygame.Surface: Returns the sprite of the grass tile, creating it if necessary.
    '''
    
    def __init__(self, col: int, row: int):
        '''Initializes a HerbeTile with the given column and row indices.
        Parameters:
            col (int): The column index of the tile in the grid.
            row (int): The row index of the tile in the grid.
        Returns:
            None'''
        self.col = col
        self.row = row
        self.grip = HERBE_GRIP
        self.drift_friction = HERBE_DRIFT_FRICTION
        self.traction = HERBE_TRACTION
        self.block = None
        self.sprite: pygame.Surface | None = None
    
    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        '''Returns the sprite of the grass tile, creating it if necessary.
        Parameters:
            tile_size (int): The size of the tile in pixels. Default is TILE_SIZE.
        Returns:
            pygame.Surface: The surface representing the grass tile's sprite.'''
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        herbe_surface = pygame.Surface((tile_size, tile_size))
        herbe_surface.fill((34, 139, 34))
        pygame.draw.rect(herbe_surface, (79, 214, 79), herbe_surface.get_rect(), 2) 
        
            
        self.sprite = herbe_surface
        return self.sprite