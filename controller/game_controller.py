import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler
 
 
class GameController:
    '''Class responsible for controlling the game flow.
        
        Attributes:
            screen (pygame.Surface): The main display surface for the game.
            clock (pygame.time.Clock): The clock used to control the frame rate.
            model (GameModel): The game model containing the game state and logic.
            view (GameView): The game view responsible for rendering the game.
            input_handler (InputHandler): The input handler for processing user inputs.
            running (bool): A flag indicating whether the game loop is running.
        Methods:
            run() -> None: Starts the main game loop.
            handle_events() -> None: Handles user input events.
            handle_keydown(key: int) -> None: Processes keydown events based on the current game state.
            handle_menu_key(key: int) -> None: Handles key presses in the main menu.
            handle_menu_circuit(key: int) -> None: Handles key presses in the circuit selection menu.
            update() -> None: Updates the game state based on user inputs and game logic.
            apply_input(car, player_input) -> None: Applies user inputs to the specified car.
            render() -> None: Renders the game view based on the current game model.
            quit() -> None: Exits the game and closes the application.'''
 
 
 
    def __init__(self):
        '''Initializes the GameController with the necessary components for the game.
        Attributes:
            screen (pygame.Surface): The main display surface for the game.
            clock (pygame.time.Clock): The clock used to control the frame rate.
            model (GameModel): The game model containing the game state and logic.
            view (GameView): The game view responsible for rendering the game.
            input_handler (InputHandler): The input handler for processing user inputs.
            running (bool): A flag indicating whether the game loop is running.
        Returns:
            None'''
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True
 
    def run(self) -> None:
        """Lance la boucle principale du jeu.

        Exécute continuellement la gestion des événements, la mise à jour logique
        et le rendu graphique tout en respectant le nombre d'images par seconde (FPS).

        Retourne
        --------
        None
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
 
    def handle_events(self) -> None:
        '''Handles user input events, including quitting the game and key presses.
        Returns:
            None'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
 
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
 
    def handle_keydown(self, key: int) -> None:
        '''Processes keydown events based on the current game state.
        Parameters:
            key (int): The Pygame constant representing the key that was pressed.
        Returns:
            None'''
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)

        elif state == GameState.CIRCUIT:
            if key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                self.handle_menu_circuit(key)
 
 
 
    def handle_menu_key(self, key: int) -> None:
        '''Handles key presses in the main menu.
        Parameters:
            key (int): The Pygame constant representing the key that was pressed.
        Returns:
            None'''
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT
        elif key == pygame.K_ESCAPE:
            self.quit()
 
    def handle_menu_circuit(self, key: int) -> None:
        '''Handles key presses in the circuit selection menu.
        Parameters:
            key (int): The Pygame constant representing the key that was pressed.
        Returns:
            None'''
        self.model.load_circuit(key)
        self.model.state = GameState.RACING
 
    
        
    def update(self) -> None:
        '''Updates the game state based on user inputs and game logic.
        Returns:
            None'''
        if self.model.state != GameState.RACING:
            return

        for index, car in enumerate(self.model.cars):
            player_input = self.input_handler.get_inputs(index)
            self.apply_input(car, player_input)
        self.model.update()
 
    def apply_input(self, car, player_input) -> None:
        '''Applies user input to a car.
        Parameters:
            car: The car to apply input to.
            player_input (dict): A dictionary containing the player's input.
        Returns:
            None'''
        if player_input['accelerate']:
            car.accelerate()
        if player_input['brake']:
            car.brake()
        car.steer(player_input['left'] - player_input['right'])
 
    def render(self) -> None:
        '''Renders the game view based on the current game model.
        Returns:
            None'''
        self.view.draw(self.model)
    
 
    def quit(self) -> None:
        '''Exits the game and closes the application.
        Returns:
            None '''
        self.running = False
        pygame.quit()
        sys.exit()