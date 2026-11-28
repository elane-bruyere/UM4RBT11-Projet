WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.2
CAR_WIDTH = 30
CAR_HEIGHT = 50


SPEED_MAX = CAR_ACCELERATION*100
CAR_ANGULAR_DECAY = 1.1

CAR_MAX_STEERING = 20     # max de comment ça tourne 
CAR_STEERING_SPEED = 2    # vitesse de comment ça tourne
CAR_WHEELBASE = 40        # longueur entre l'anavant et l'arreiere 

PLAYER_COLORS = [(255, 0, 0), (45, 87, 36)]   # rouge -> 1 et vertt -> 2 c'est parce que pygame fait automatiquement une voiture rouge et pk pas en faire une d'une autre couleur

CAR_BRAKE_FORCE = 0.1      # force de freinage
CAR_AIR_FRICTION = 0.015   # frottements de l'air

ROAD_GRIP = 0.10            # frottements de la route
ROAD_DRIFT_FRICTION = 0.05  # frottements en dérapage sur la route
ROAD_TRACTION = 2.0         # facilité à accélérer / freiner

DRIFT_GRIP_RATIO = 0.2     # ça grippe moins quand on glisse
 
ICE_GRIP = 0.012            # frottements de la glace
ICE_DRIFT_FRICTION = 0.001  # frottements en dérapage sur la glace
ICE_TRACTION = 0.3          #facilité à freiner/accel

HERBE_GRIP = 0.09           #frottements de l'herbe
HERBE_DRIFT_FRICTION = 0.05 #frottements en dérapage sur l'herbe
HERBE_TRACTION = 0.5         #facilité à freiner/accel

class GameState:
    """Définit les différents états possibles du jeu

    Attributs
    --------
    MENU: str
        État correspondant au menu principal
    CIRCUIT: str 
        Etat pour choisir le circuit
    RACING: str
        État correspondant à la course en cours
    """
    MENU = "menu"
    CIRCUIT = "circuit"
    RACING = "racing"

# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)

# Couleur du premier circuit 
C1_COLOR = (80, 80, 20)

# Couleur du deuxieme circuit 
C2_COLOR = (30, 30, 100)

C3_COLOR = (100, 30, 30)

TOURS = 1

CIRCUITS = [
    ("Circuit 1", [
        "RRRRRRRRRRRRRRRR",
        "RRRRRRR12RRRRRRR",
        "RRRRRRRRRRRRRRRR",
        "RRRRRRRRRRRRRRRR",
        "RRRRRRRRRRRRRRRR",
        "RRRRRRRCRRRRRRRR",
        "RRRRRRRRRRRRRRRR",
        "LLLLLLLLLLLLLLLL",
        "RRRRRRRRRRRRRRRR",
        "RRRRRRRRRRRRRRRR",
        "RRRRRVRRRRCRRRRR",
        "RRRRRBBRRRRRRRRR",
    ]),
    ("Circuit 2", [
        "RRRRRRRRRLRRRRRR",
        "RRRRRRRRVRRRRRRR",
        "RRRRRCRRRRRRRRRR",
        "RRRRRRRRRRRRRRRR",
        "RRRRRRRRRRRRRRRR",
        "HHHHHHHHHHHHHHHH",
        "HHHHHHHHCHHHHHHH",
        "HHHHHHHHHHHHHHHH",
        "HHHHHHHHHHHHHHHH",
        "RRRRRBRRRRRCRRRR",
        "RR12RRRRRRRRRRRR",
        "RRRRRRRRRRRRRRRR",
    ]),
    ("Circuit 3", [
        "RBRRRRRRRLRRRRRR",
        "RRVRCRRRRRRRRRRR",
        "RRIIIIIIIIIIIIRR",
        "RRIIIIIIIIIIIIRR",
        "RRIIIIRRRRIIIIRR",
        "RRIIIIRRRRIIIIRR",
        "RRIIIIRRRCIIIIRR",
        "RRIIIIIIIIIIIIRR",
        "RRIIIIIIIIIIIIRR",
        "RRRRRRRRRRRRRRRR",
        "RRRRRR12RRRRRRRR",
        "RRRRRRRRRRRRRRRR",
]),
]

