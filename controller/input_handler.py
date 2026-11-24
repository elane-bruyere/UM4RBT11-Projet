import pygame
 
 
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
    '''Class to handle player inputs for the game.
        
        Attributes:
            mappings (list): A list containing the key mappings for each player.
        Methods:
            get_inputs(player: int) -> dict: Returns a dictionary of the current inputs for the specified player.
    '''
 
    def __init__(self):
        '''Initializes the InputHandler with key mappings for two players.
            
            Attributes:
                mappings (list): A list containing the key mappings for each player.
        '''
        self.mappings = [PLAYER1_MAPPING, PLAYER2_MAPPING]
 
    def get_inputs(self, player: int) -> dict:
        '''Returns a dictionary of the current inputs for the specified player.
            
            Parameters:
                player (int): The index of the player (0 for Player 1, 1 for Player 2).
            Returns:
                dict: A dictionary where keys are action names and values are booleans indicating whether the action is currently being performed.
        '''
        mapping = self.mappings[player]
        keys = pygame.key.get_pressed()
        p = {action: False for action in mapping.values()}
 
        for key, action in mapping.items():
            if keys[key]:
                p[action] = True
 
        return p
 