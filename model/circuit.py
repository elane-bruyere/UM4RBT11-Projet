from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:
    '''Class representing a circuit in the game.
    Attributes:
        grid (list[list[RoadTile]]): A 2D list representing the grid of road tiles in the circuit.
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
    Methods:
        get_tile(col: int, row: int) -> RoadTile | None: Returns the tile at the specified column and row, or None if out of bounds.
        get_tile_at_pixel(px: float, py: float) -> RoadTile | None: Returns the tile at the specified pixel coordinates, or None if out of bounds.
        pixel_width() -> int: Returns the total width of the circuit in pixels.
        pixel_height() -> int: Returns the total height of the circuit in pixels.
    '''

    def __init__(self,  grid: list[list[RoadTile]]):
        '''Initializes a Circuit with the specified grid of road tiles.
            
            Parameters:
                grid (list[list[RoadTile]]): A 2D list representing the grid of road tiles in the circuit.
        '''
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        '''Returns the tile at the specified column and row, or None if out of bounds.
            
            Parameters:
                col (int): The column index of the tile in the grid.
                row (int): The row index of the tile in the grid.
            Returns:
                RoadTile | None: The tile at the specified column and row, or None if out of bounds.
        '''
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        '''Returns the tile at the specified pixel coordinates, or None if out of bounds.
            
            Parameters:
                px (float): The x-coordinate in pixels.
                py (float): The y-coordinate in pixels.
            Returns:
                RoadTile | None: The tile at the specified pixel coordinates, or None if out of bounds.
        '''
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        '''Calcule et renvoie la largeur totale du circuit en pixels
        Retourne
        --------
        int
            Largeur totale en pixels
        '''
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        '''Calcule et renvoie la hauteur totale du circuit en pixels
        Retourne
        --------
        int
            Hauteur totale en pixels
        '''
        return self.rows * TILE_SIZE
