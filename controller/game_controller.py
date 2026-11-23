# Kart-Engine v2.3
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
        clock (pygame.time.Clock): The clock object to manage the game's frame rate.
        model (GameModel): The game model containing the game state and logic.
        view (GameView): The game view responsible for rendering the game.
        input_handler (InputHandler): The input handler for processing user inputs.
        running (bool): A flag indicating whether the game loop is running.
        
        Methods:
            run(): Starts the main game loop, handling events, updating the model, and rendering the view.
            handle_events(): Processes user input events such as quitting the game or key presses.
            handle_keydown(key: int): Handles keydown events based on the current game state.
            handle_menu_key(key: int): Handles key presses when in the menu state.
            update(): Updates the game model based on the current state and the inputs of each player.
            apply_input(car, player_input): Applies the inputs of one player to its car.
            render(): Renders the current state of the game using the view.
            quit(): Exits the game and closes the application.'''
 
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True
 
    def run(self) -> None:
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
 
        state = self.model.state
 
        if state == GameState.MENU:
            self.handle_menu_key(key)
 
    def handle_menu_key(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING
        elif key == pygame.K_ESCAPE:
            self.quit()
 
    def update(self) -> None:
        if self.model.state != GameState.RACING:
            return
 
        
        for index, car in enumerate(self.model.cars):
            player_input = self.input_handler.get_inputs(index)
            self.apply_input(car, player_input)
        self.model.update()
 
    def apply_input(self, car, player_input) -> None:
        if player_input['accelerate']:
            car.accelerate()
        if player_input['brake']:
            car.brake()
        car.steer(player_input['left'] - player_input['right'])
 
    def render(self) -> None:
        self.view.draw(self.model)
 
    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
 