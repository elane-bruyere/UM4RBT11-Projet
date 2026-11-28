# Kart-Engine v2.3
import pygame
from constants import GameState, GRID_ROWS, GRID_COLS, PLAYER_COLORS, C1_COLOR, C2_COLOR, C3_COLOR, CIRCUITS, TOURS, TILE_SIZE
from model.car import Car
from model.circuit import Circuit
from model.road_tile import (RoadTile, IceTile, HerbeTile, LigneArrivee, PointPassage, BonusPassage, VideTile)
 
TILE_CLASSES = { 
    "R": RoadTile,
    "I": IceTile,
    "H": HerbeTile,
    "L": LigneArrivee,
    "C": PointPassage,
    "B": BonusPassage,
    "V": VideTile
}
 
BLOCK_CLASSES = {
    
}
 
class GameModel:
    
    def __init__(self):
        
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []
        self.selected_circuit: int = 0
        self.pointpassage: list[set] = []
        self.passed: list[set] = []
        self.tours: list[int] = []
        self.on_finish: list[bool] = []
        self.winner: int | None = None
 
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
        self.pointpassage = self.find_point_passage()
        self.passed = [set() for _ in self.cars]
        self.tours = [0 for _ in self.cars]
        self.on_finish = [False for _ in self.cars]
        self.winner = None
        
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
        if self.winner is not None:
            return 
        for car in self.cars:

            tile = self.circuit.get_tile_at_pixel(car.x, car.y)
            if tile is not None:
                car.apply_terrain(tile)
            car.update_position()
        self.update_laps()
 
    def find_point_passage(self) -> list[set]:
        '''Regroupe les cases PointPassage qui se touchent : chaque groupe est un point de passage.
        Returns:
            list[set]: Les points de passage, chacun étant un ensemble de cases (col, ligne).'''
        cells = {(col, row)
                 for row, line in enumerate(self.circuit.grid)
                 for col, tile in enumerate(line)
                 if isinstance(tile, PointPassage) and not isinstance(tile, LigneArrivee)}
        groups = []
        while cells:
            first = cells.pop()
            group = {first}
            to_visit = [first]
            while to_visit:
                col, row = to_visit.pop()
                for neighbour in ((col + 1, row), (col - 1, row), (col, row + 1), (col, row - 1)):
                    if neighbour in cells:
                        cells.remove(neighbour)
                        group.add(neighbour)
                        to_visit.append(neighbour)
            groups.append(group)
        return groups
 
    def update_laps(self) -> None:
        '''Compte un tour quand une voiture entre sur la ligne d'arrivée après avoir franchi tous
        les points de passage ; la première à atteindre TOURS tours gagne la course.
        Returns:
            None'''
        for i, car in enumerate(self.cars):
            tile = self.circuit.get_tile_at_pixel(car.x, car.y)
            cell = (int(car.x // TILE_SIZE), int(car.y // TILE_SIZE))
            on_finish = isinstance(tile, LigneArrivee)
 
            if isinstance(tile, PointPassage) and not on_finish:
                for number, group in enumerate(self.pointpassage):
                    if cell in group:
                        self.passed[i].add(number)
            if on_finish and not self.on_finish[i] and len(self.passed[i]) == len(self.pointpassage):
                self.tours[i] += 1
                self.passed[i].clear()
                if self.tours[i] >= TOURS and self.winner is None:
                    self.winner = i
            self.on_finish[i] = on_finish
            
    
            
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
 