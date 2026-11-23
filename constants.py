WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.2
CAR_WIDTH = 30
CAR_HEIGHT = 50


#trucs que j'ai rajouté
CAR_MAX_STEERING = 20     # max de comment ça tourne 
CAR_STEERING_SPEED = 2    # vitesse de comment ça tourne
CAR_WHEELBASE = 40        # longueur entre l'anavant et l'arreiere 
PLAYER_COLORS = [(255, 0, 0), (180, 39, 245)]   # rouge -> 1 et violetttt -> 2 c'est parce que pygame fait automatiquement une voiture rouge et pk pas en faire une d'une autre couleur
CAR_BRAKE_FORCE = 0.1      # force de freinage
CAR_AIR_FRICTION = 0.015   # frottements de l'air
 
class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
