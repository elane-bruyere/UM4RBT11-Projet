import pygame
from constants import GameState, GRID_ROWS, GRID_COLS, PLAYER_COLORS, C1_COLOR, C2_COLOR
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
        '''Initializes the GameModel with default values.  
          
            Attributes:
                state (GameState): The current state of the game, initialized to GameState.MENU.
                circuit (Circuit | None): The current circuit in the game, initialized to None.
                cars (list[Car]): The cars in the game, initialized as an empty list.
        '''
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []
 
    def load_circuit(self, choice) -> None:
        '''Loads a new circuit based on the player's choice and spawns the cars.
            
            Parameters:
                choice (int): The player's choice for the circuit (pygame key constant).
            Returns:
                None
        '''
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
        if choice == pygame.K_1:
            RoadTile.color = C1_COLOR
        elif choice == pygame.K_2:
            RoadTile.color = C2_COLOR
            
        self.circuit = Circuit(grid=grid)
        self.spawn_cars()
 
 
    def spawn_cars(self) -> None:
        '''Spawns the two cars at predefined locations on the circuit.
            
            Returns:
                None
        '''
        self.cars = [Car(7, 1, PLAYER_COLORS[0]),
                     Car(8, 1, PLAYER_COLORS[1])]
 
 
    def update(self) -> None:
        '''Updates the game state, including the cars' positions if racing.
            
            Returns:
                None
        '''
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
            
    def nokey(self) ->None:
        '''Stops all cars by setting their speed to zero.
            
            Returns:
                None
        '''
        if self.state != GameState.RACING or self.circuit is None:
            return 
        for car in self.cars:
            if car.speed != 0.0: 
                car.speed = 0.0
            