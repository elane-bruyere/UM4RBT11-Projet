import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler
 
 
class GameController:
    '''Class representing the game controller.
        
        Attributes:
            screen (pygame.Surface): The main display surface for the game.
            clock (pygame.time.Clock): The clock used to control the game's frame rate. 
            model (GameModel): The game model containing the current state and data of the game.
            view (GameView): The game view responsible for rendering the game state.
            input_handler (InputHandler): The input handler responsible for processing user inputs.
            running (bool): A flag indicating whether the game loop is running.
        Methods:
            run(): Starts the main game loop, handling events, updating the model, and rendering the view.
            handle_events(): Processes Pygame events, including quitting the game and key presses.
            handle_keydown(key: int): Handles specific key presses based on the current game state.
            handle_menu_key(key: int): Handles key presses when the game is in the main menu.
            handle_menu_circuit(key: int): Handles key presses when the game is in the circuit selection menu.
            update(): Updates the game model based on user inputs and game logic.
            apply_input(car, player_input): Applies user inputs to a specific car in the game model.
            render(): Renders the current game state using the game view.
            quit(): Stops the game loop and exits the game.
    '''
 
    def __init__(self):
        '''Initializes the GameController, setting up the game window, clock, model, view, and input handler.
            
            Attributes:
                screen (pygame.Surface): The main display surface for the game.
                clock (pygame.time.Clock): The clock used to control the game's frame rate. 
                model (GameModel): The game model containing the current state and data of the game.
                view (GameView): The game view responsible for rendering the game state.
                input_handler (InputHandler): The input handler responsible for processing user inputs.
                running (bool): A flag indicating whether the game loop is running.
        '''
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True
 
    def run(self) -> None:
        '''Starts the main game loop, handling events, updating the model, and rendering the view.
            
            Returns:
                None
        '''
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
 
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
 
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
 
    def handle_keydown(self, key: int) -> None:
        '''Handles specific key presses based on the current game state.
            
            Parameters:
                key (int): The Pygame constant representing the key that was pressed.
            Returns:
                None
        '''
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)

        elif state == GameState.CIRCUIT:
            if key in [pygame.K_1, pygame.K_2]:
                self.handle_menu_circuit(key)
 
 
 
    def handle_menu_key(self, key: int) -> None:
        '''Handles key presses when the game is in the main menu.
            
            Parameters:
                key (int): The Pygame constant representing the key that was pressed.
            Returns:
                None
        '''
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT
        elif key == pygame.K_ESCAPE:
            self.quit()
 
 
    def handle_menu_circuit(self, key: int) -> None:
        '''Handles key presses when the game is in the circuit selection menu.
            
            Parameters:
                key (int): The Pygame constant representing the key that was pressed.
            Returns:
                None
        '''
        self.model.load_circuit(key)
        self.model.state = GameState.RACING
 
    
        
    def update(self) -> None:
        '''Updates the game model based on user inputs and game logic.
            
            Returns:
                None
        '''
        if self.model.state != GameState.RACING:
            return

        for index, car in enumerate(self.model.cars):
            player_input = self.input_handler.get_inputs(index)
            self.apply_input(car, player_input)
        self.model.update()
 
 
 
    def apply_input(self, car, player_input) -> None:
        '''Applies the player's input to the specified car.
            
            Parameters:
                car: The car to which the input will be applied.
                player_input (dict): A dictionary containing the player's input.
            Returns:
                None
        '''
        if player_input['accelerate']:
            car.accelerate()
        if player_input['brake']:
            car.brake()
        car.steer(player_input['left'] - player_input['right'])
 
 
    def render(self) -> None:
        '''Renders the current game state using the game view.
            
            Returns:
                None
        '''
        self.view.draw(self.model)
 
 
    def quit(self) -> None:
        '''Stops the game loop and exits the game.
            
            Returns:
                None
        '''
        self.running = False
        pygame.quit()
        sys.exit()
 