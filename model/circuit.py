from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:
    """Représente le circuit du jeu sous forme d'une grille de tuiles de route

    Attributs
    --------
    grid: list[list[RoadTile]]
        Grille bidimensionnelle représentant le circuit
    rows: int
        Nombre de lignes dans la grille
    cols: int
        Nombre de colonnes dans la grille
    """

    def __init__(self,  grid: list[list[RoadTile]]):
        """Initialise le circuit avec une grille de tuiles donnée

        Paramètres
        --------
        grid: list[list[RoadTile]]
            Grille à deux dimensions représentant le circuit
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        """Récupère la tuile située à une colonne et une ligne données, ou None si hors limites

        Paramètres
        --------
        col: int
            Indice de la colonne
        row: int
            Indice de la ligne

        Retourne
        --------
        RoadTile | None
            La tuile correspondante ou None
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        """Récupère la tuile située aux coordonnées en pixels (px, py)

        Paramètres
        --------
        px: float
            Position horizontale en pixels
        py: float
            Position verticale en pixels

        Retourne
        --------
        RoadTile | None
            La tuile correspondante ou None
        """
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        """Calcule et renvoie la largeur totale du circuit en pixels

        Retourne
        --------
        int
            Largeur totale en pixels
        """
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Calcule et renvoie la hauteur totale du circuit en pixels

        Retourne
        --------
        int
            Hauteur totale en pixels
        """
        return self.rows * TILE_SIZE

def build_circuit(layout: list, name: str = "circuit") -> tuple[list[list], dict[str, tuple[int, int]]]:
    '''Builds the grid of a circuit from its matrix of characters.
 
    The matrix contains GRID_ROWS lines of GRID_COLS characters, one character
    per tile, read as layout[row][col]. Each line can be a string or a list of
    characters. The characters '1' and '2' are the starting blocks of the two
    players (placed on a road tile).
 
    Args:
        layout (list): The matrix of characters describing the circuit.
        name (str): Name of the circuit, only used in error messages.
 
    Returns:
        tuple: The grid (list of rows of tiles) and a dictionary giving the
            starting position (col, row) of each player, e.g. {'1': (7, 1), '2': (8, 1)}.
 
    Raises:
        ValueError: If the matrix does not have the right size or lacks a starting block.
    '''
    lines = ["".join(row) for row in layout]
    if len(lines) != GRID_ROWS or any(len(line) != GRID_COLS for line in lines):
        raise ValueError(
            f"{name} : il faut {GRID_ROWS} lignes de {GRID_COLS} caractères")
 
    grid = []
    starts = {}
    for row, line in enumerate(lines):
        grid_row = []
        for col, letter in enumerate(line):
            # Lettre inconnue (ou bloc pas encore codé) : case de route par défaut
            tile = TILE_CLASSES.get(letter, RoadTile)(col=col, row=row)
            if letter in ("1", "2"):
                starts[letter] = (col, row)
                tile.block = StartBlock(col, row, int(letter))
                
            grid_row.append(tile)
        grid.append(grid_row)
     
    if "1" not in starts or "2" not in starts:
            raise ValueError(f"{name} : il faut un bloc '1' et un bloc '2'")
    return grid, starts
