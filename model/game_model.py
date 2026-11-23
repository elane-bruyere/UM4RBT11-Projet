# Kart-Engine v2.3
from constants import GameState, GRID_ROWS, GRID_COLS, PLAYER_COLORS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
 
 
class GameModel:
    '''Class representing the game model.
    
    Attributes:
        state (GameState): The current state of the game.
        circuit (Circuit | None): The current circuit in the game.
        cars (list[Car]): The cars in the game (index 0 = player 1, index 1 = player 2).
        
    Methods:
        load_circuit(): Loads a new circuit and spawns the cars.
        spawn_cars(): Spawns the two cars at predefined locations.
        update(): Updates the game state, including the cars' positions if racing.
    '''
    
    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []
 
    def load_circuit(self) -> None:
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_cars()
 
    def spawn_cars(self) -> None:
        # positions provisoires : elles viendront des blocs de départ du circuit
        self.cars = [Car(7, 1, PLAYER_COLORS[0]),
                     Car(8, 1, PLAYER_COLORS[1])]
 
    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
 