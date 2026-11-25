import pygame
from constants import GameState, GRID_ROWS, GRID_COLS, PLAYER_COLORS, C1_COLOR, C2_COLOR, C3_COLOR, CIRCUITS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile, IceTile, HerbeTile

TILE_CLASSES = { #les lettres pour les matrices de circuits dans le fichier constantes
    "R": RoadTile,
    "I": IceTile,
    "H": HerbeTile
}
 
 
class GameModel:
    '''Class representing the game model.
    
    Attributes:
        state (GameState): The current state of the game.
        circuit (Circuit | None): The current circuit in the game.
        cars (list[Car]): The cars in the game (index 0 = player 1, index 1 = player 2).
        selected_circuit (int): Index, in CIRCUITS, of the circuit that will be loaded.
        
    Methods:
        load_circuit(choice): Loads a new circuit and spawns the cars.
        select_next_circuit(): Selects the next circuit of the menu (wraps around).
        select_previous_circuit(): Selects the previous circuit of the menu (wraps around).
        build_grid(layout, name): Builds the grid of tiles from the matrix of a circuit.
        spawn_cars(starts): Spawns the two cars on the starting positions of the circuit.
        update(): Updates the game state, including the cars' positions if racing.
        nokey(): Stops the cars if no key is pressed.
    '''
    
    def __init__(self):
        '''Initializes the GameModel with default values.
        Attributes:
            state (GameState): The initial state of the game, set to MENU.
            circuit (Circuit | None): The current circuit, initially None.
            cars (list[Car]): The list of cars in the game, initially empty.
            selected_circuit (int): The circuit to load, initially the first one.
        
        
        Returns:
            None
        '''
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []
        self.selected_circuit: int = 0
 
    def load_circuit(self, choice=None) -> None:
        '''Loads a new circuit based on the player's choice and spawns the cars.
        Parameters:
            choice (int | None): The key pressed by the player to select the circuit
                (pygame.K_1 or pygame.K_2 or pygame.K_3). If None, the circuit currently selected
                in the menu (selected_circuit) is loaded.
        Returns:
            None
        '''
        if choice == pygame.K_1:
            self.selected_circuit = 0
            RoadTile.color = C1_COLOR
        elif choice == pygame.K_2:
            self.selected_circuit = 1
            RoadTile.color = C2_COLOR
        elif choice == pygame.K_3:
            self.selected_circuit = 2
            RoadTile.color = C3_COLOR
 
        name, layout = CIRCUITS[self.selected_circuit]
        grid, starts = self.build_grid(layout, name)
        self.circuit = Circuit(grid=grid)
        self.spawn_cars(starts)
        
    def select_next_circuit(self) -> None:
        '''Selects the next circuit in the menu, wrapping around if necessary.
        Returns:
            None
        '''
        self.selected_circuit = (self.selected_circuit + 1) % len(CIRCUITS)
 
    def select_previous_circuit(self) -> None:
        '''Selects the previous circuit in the menu, wrapping around if necessary.
        Returns:
            None
        '''
        self.selected_circuit = (self.selected_circuit - 1) % len(CIRCUITS)
 
    def build_grid(self, layout: list, name: str) -> tuple[list[list], dict]:
        '''Construit la grille de cases d'un circuit à partir de sa matrice de caractères.
 
        La matrice contient GRID_ROWS lignes de GRID_COLS caractères, une lettre par case
        (layout[ligne][colonne]). Les caractères '1' et '2' sont les positions de départ
        des deux joueurs (sur une case de route). Une lettre inconnue donne une case de route.
        Renvoie la grille et un dictionnaire {'1': (col, ligne), '2': (col, ligne)}.
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
                if letter in ("1", "2"):
                    starts[letter] = (col, row)
                tile_class = TILE_CLASSES.get(letter, RoadTile)
                grid_row.append(tile_class(col=col, row=row))
            grid.append(grid_row)
 
        if "1" not in starts or "2" not in starts:
            raise ValueError(f"{name} : il faut un bloc '1' et un bloc '2'")
        return grid, starts
 
    def spawn_cars(self, starts: dict) -> None:
        '''Spawns the two cars on the starting positions of the circuit.
        Parameters:
            starts (dict): The starting position (col, row) of each player, e.g. {'1': (7, 1), '2': (8, 1)}.
        Returns:
            None'''
        self.cars = [Car(*starts["1"], PLAYER_COLORS[0]), #lieu de spawn 
                     Car(*starts["2"], PLAYER_COLORS[1])]
 
    def update(self) -> None:
        '''Updates the game state, including the cars' positions if racing.
        Returns:
            None'''
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            # La voiture prend les propriétés du terrain sur lequel elle roule
            tile = self.circuit.get_tile_at_pixel(car.x, car.y)
            if tile is not None:
                car.apply_terrain(tile)
            car.update_position()
            
            
    
            
    def nokey(self) ->None:
        '''Stops the cars if no key is pressed.
        Returns:
            None'''
        if self.state != GameState.RACING or self.circuit is None:
            return 
        for car in self.cars:
            if car.vx != 0.0 or car.vy != 0.0:
                car.vx = 0.0
                car.vy = 0.0
 
            