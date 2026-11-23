# Kart-Engine v2.3
import pygame
 
 
# Un dictionnaire par joueur (touches conformes à l'énoncé) : touche pygame -> nom de l'action
PLAYER1_MAPPING = {
    pygame.K_z:      "accelerate",
    pygame.K_w:      "accelerate",
    pygame.K_s:      "brake",
    pygame.K_q:      "left",
    pygame.K_a:      "left",
    pygame.K_d:      "right",
    pygame.K_SPACE:  "use_item",
}
 
PLAYER2_MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:   "brake",
    pygame.K_LEFT:   "left",
    pygame.K_RIGHT:  "right",
    pygame.K_RETURN: "use_item",
}
 
 
class InputHandler:
    '''Class responsible for handling user input in the game.
    Attributes:
        mappings (list): One dictionary per player (index 0 = player 1, index 1 = player 2),
            each mapping pygame key constants to action strings.
 
    Methods:
        get_inputs(player) -> dict: Returns a dictionary of actions and their corresponding boolean states
            for the given player, based on the current key presses.'''
 
 
    def __init__(self):
        self.mappings = [PLAYER1_MAPPING, PLAYER2_MAPPING]
 
    def get_inputs(self, player: int) -> dict:
        mapping = self.mappings[player]
        keys = pygame.key.get_pressed()
        p = {action: False for action in mapping.values()}
 
        for key, action in mapping.items():
            if keys[key]:
                p[action] = True
 
        return p
 