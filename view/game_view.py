import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel
 
 
class GameView:
    '''Class responsible for rendering the game view.
    Attributes:
        screen (pygame.Surface): The main display surface for the game.
        font (pygame.font.Font): The font used for rendering text.      
        
    Methods:
        draw(model: GameModel) -> None: Draws the game view based on the current game model.
        _draw_menu(model: GameModel) -> None: Draws the main menu
        _draw_circuit(model: GameModel) -> None: Draws the circuit selection menu
        _draw_racing(model: GameModel) -> None: Draws the racing view, including the circuit and cars.'''
    
 
    def __init__(self, screen: pygame.Surface):
        '''Initializes the GameView with the given screen surface.
        Parameters:
            screen (pygame.Surface): The main display surface for the game.
        Returns:
            None'''
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
 
    def draw(self, model: GameModel) -> None:
        '''Draws the game view based on the current game model.
        Parameters:
            model (GameModel): The game model containing the current state, circuit, and cars information
        Returns:
            None'''
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self.draw_menu(model)
            
        if model.state == GameState.CIRCUIT:
            self.draw_circuit(model)
            
        elif model.state == GameState.RACING:
            self.draw_racing(model)
        pygame.display.flip()
 
    def draw_menu(self, model: GameModel) -> None:
        '''Draws the main menu.
        Parameters:
            model (GameModel): The game model containing the current state and circuit information.
        Returns:
            None
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
    
    
    def draw_circuit(self, model: GameModel) -> None: 
        cx = WINDOW_WIDTH // 2
        ''' Draws the circuit selection menu.
        Parameters:
            model (GameModel): The game model containing the current state and circuit information.
        Returns:
            None
        '''
        title_surf = self.font.render("Choose a circuit", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx,100)))

        options = [("CIRCUIT 1 (Press 1)", GameState.RACING),
                   ("CIRCUIT 2 (Press 2)", GameState.RACING),
                   ("CIRCUIT 3 (Press 3)", GameState.RACING)]

        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                                rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
 
 
    def draw_racing(self, model: GameModel) -> None:
        '''Draws the racing view, including the circuit and cars.
        Parameters:
            model (GameModel): The game model containing the current state, circuit, and cars information
        Returns:
            None'''
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
            
    def draw_race_info(self, model: GameModel) -> None:
        
        for i in range(len(model.cars)):
            label = f"J{i + 1} : {model.laps[i]}/{LAPS} tours"
            text = self.font.render(label, True, PLAYER_COLORS[i])
            self.screen.blit(text, (10, 10 + i * 30))
        if model.winner is not None:
            banner = self.font.render(f"Joueur {model.winner + 1} VICTOIRE ! (Échap : retour au menu)",
                                      True, COLOR_ACCENT)
            self.screen.blit(banner, banner.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
    
 