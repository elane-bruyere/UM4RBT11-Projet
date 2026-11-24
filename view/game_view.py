import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel
 
 
class GameView:
    '''Class representing the game view.
        
        Attributes:
            screen (pygame.Surface): The main display surface for the game.
            font (pygame.font.Font): The font used for rendering text in the game.
        Methods:
            draw(model: GameModel): Draws the current state of the game based on the provided model.
            _draw_menu(model: GameModel): Draws the main menu of the game.
            _draw_circuit(model: GameModel): Draws the circuit selection menu.
            _draw_racing(model: GameModel): Draws the racing state of the game, including the circuit and cars.
    '''
    
    
    def __init__(self, screen: pygame.Surface):
        '''Initializes the GameView with the provided screen surface.
            
            Parameters:
                screen (pygame.Surface): The main display surface for the game.
        '''
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
 
 
    def draw(self, model: GameModel) -> None:
        '''Draws the current state of the game based on the provided model.
            
            Parameters:
                model (GameModel): The game model containing the current state and data to be rendered.
            Returns:
                None'''
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
            
        if model.state == GameState.CIRCUIT:
            self._draw_circuit(model)
            
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()
 
 
    def _draw_menu(self, model: GameModel) -> None:
        '''Dessine le menu principal du jeu
            
            Parametres : 
            ------------
            model: GameModel 
            model du jeu 
        '''
        cx = WINDOW_WIDTH // 2
 
        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))
 
        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
    
    
    
    def _draw_circuit(self, model: GameModel) -> None: 
        '''Dessine le menu de sélection du circuit
        Parametres :
        ------------
        model: GameModel
            model du jeu
        '''
        cx = WINDOW_WIDTH // 2
        title_surf = self.font.render("Choose a circuit", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx,100)))

        options = [("CIRCUIT 1 (Press 1)", GameState.RACING),
                   ("CIRCUIT 2 (Press 2)", GameState.RACING)]

        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                                rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
 
 
    def _draw_racing(self, model: GameModel) -> None:
        '''Dessine l'état de course du jeu, y compris le circuit et les voitures.
        Parametres :
        ------------
        model: GameModel
            model du jeu
        '''
        if model.circuit is None:
            return
 
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))
 
        for car in model.cars:
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)
 