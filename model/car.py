import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_MAX_STEERING, CAR_STEERING_SPEED, CAR_WHEELBASE, GRID_COLS, GRID_ROWS, CAR_BRAKE_FORCE, CAR_AIR_FRICTION,
    ROAD_GRIP, ROAD_DRIFT_FRICTION, ROAD_TRACTION, DRIFT_GRIP_RATIO, GRIP_SCALE
)
 

 
class Car:
    '''
      Class representing a car in the game.
 
      The car keeps a velocity vector (vx, vy) that is distinct from its orientation.
      When the two are not aligned, the car has a sideways (lateral) velocity: the tires
      try to cancel it, and if the terrain does not give enough grip the car drifts.
 
      Attributes:
          x (float): The x-coordinate of the car's position.
          y (float): The y-coordinate of the car's position.
          vx (float): The x component of the car's velocity (pixels per frame).
          vy (float): The y component of the car's velocity (pixels per frame).
          angle (float): The orientation of the car in degrees. 0 means the car
              points up, and a positive angle is a counter-clockwise rotation
              (the car turns left).
          steering_angle (float): The angle of the steering wheel in degrees.
              Positive means left, negative means right.
          grip (float): Grip of the terrain under the car (before GRIP_SCALE): the maximum
              lateral velocity the tires can cancel per frame. Below it the car holds the road.
          drift_friction (float): Share of the speed lost per frame while the car is drifting.
          traction (float): Coefficient applied to accelerating and braking (1 = full traction).
          is_drifting (bool): True while the car is drifting.
          color (tuple): The RGB color of the car.
          sprite (pygame.Surface): The visual representation of the car.
 
      Methods:
          get_heading(): Returns the unit vector the car points to.
          get_speed(): Returns the signed speed along the car's orientation (negative when reversing).
          accelerate(): Pushes the car forward with an acceleration value.
          back_run(): Pushes the car backwards with an acceleration value (reverse).
          brake(): Slows the car down while moving forward, then reverses once stopped.
          steer(direction): Changes the steering angle (+1 left, -1 right, 0 recenter).
          apply_friction(): Slows the car down progressively (air friction).
          apply_terrain(terrain): Takes the grip, drift friction and traction of the terrain under the car.
          update_orientation(): Rotates the car according to its speed and steering angle.
          apply_grip(): Cancels the lateral velocity within the limit of the grip, and detects drifting.
          update_position(): Updates the car's orientation, velocity and position.
          keep_on_screen(): Prevents the car from leaving the map.
          build_sprite(): Creates and returns a pygame.Surface representing the car.
          get_rotated_sprite(): Returns the rotated sprite and its corresponding rectangle for rendering.
      '''
 
    def __init__(self, start_col: int, start_row: int, color: tuple = (255, 0, 0)): 
        '''Initializes a Car with the given starting column, row, and color.
        Parameters:
            start_col (int): The starting column index of the car in the grid.
            start_row (int): The starting row index of the car in the grid.
            color (tuple): The RGB color of the car. Default is red (255, 0, 0).
        Returns:
            None
        '''
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.angle: float = 0.0
        self.steering_angle: float = 0.0
        
        self.grip: float = ROAD_GRIP
        self.drift_friction: float = ROAD_DRIFT_FRICTION
        self.traction: float = ROAD_TRACTION
        self.is_drifting: bool = False
        self.color = color
        self.sprite = self.build_sprite()
 
    def get_heading(self) -> tuple[float, float]:
        '''Returns the unit vector the car points to.
        Returns:
            tuple[float, float]: The x and y components of the unit vector representing the car's heading.'''
        rad = math.radians(self.angle)
        return -math.sin(rad), -math.cos(rad)
 
    def get_speed(self) -> float:
        '''Returns the signed speed along the car's orientation (negative when reversing).
        Returns:
            float: The signed speed of the car along its orientation.'''
        hx, hy = self.get_heading()
        return self.vx * hx + self.vy * hy
 
    def accelerate(self) -> None:
        '''Pushes the car forward with an acceleration value.
        Returns:
            None
        '''
        hx, hy = self.get_heading()
        self.vx += hx * CAR_ACCELERATION * self.traction
        self.vy += hy * CAR_ACCELERATION * self.traction
 
    def back_run(self) -> None: ##marche arrière
        '''Pushes the car backwards with an acceleration value (reverse).
        Returns:
            None
        '''
        hx, hy = self.get_heading()
        self.vx -= hx * CAR_ACCELERATION * self.traction
        self.vy -= hy * CAR_ACCELERATION * self.traction
 
    def brake(self) -> None: #avec la touche qui fait la marche arriere : si en route bim ça freine, sinon back_run
        '''Slows the car down while moving forward, then reverses once stopped.
        Returns:
            None
        '''
        forward_speed = self.get_speed()
        if forward_speed > 0:
            # On retire de la vitesse vers l'avant, sans jamais dépasser zéro
            amount = min(forward_speed, CAR_BRAKE_FORCE * self.traction)
            hx, hy = self.get_heading()
            self.vx -= hx * amount
            self.vy -= hy * amount
        else:
            self.back_run()
 
    def steer(self, direction: int) -> None: #change l'angle de braquage si +1 -> gauche; si -1 -> droite sinon -> aucune commande (avec 0)
        '''Changes the steering angle (+1 left, -1 right, 0 recenter).
        Parameters:
            direction (int): The direction to steer. +1 for left, -1 for right, 0 for recentering.
        Returns:
            None
        '''
        if direction != 0:
            self.steering_angle += direction * CAR_STEERING_SPEED
        elif abs(self.steering_angle) <= CAR_STEERING_SPEED:
            self.steering_angle = 0.0
        else: #aucune commande donc 0 -> le volant revient progressivement vers le centre
            self.steering_angle -= math.copysign(CAR_STEERING_SPEED, self.steering_angle) # le volant ne peut pas tourner plus loin que l'angle max def dans le fichier csts
        self.steering_angle = max(-CAR_MAX_STEERING,
                                  min(CAR_MAX_STEERING, self.steering_angle))
 
    def update_orientation(self) -> None: #fait tourner la voiture
        '''Rotates the car according to its speed and steering angle.
        Returns:
            None
        '''
        turn_rate = self.get_speed() * math.tan(math.radians(self.steering_angle)) / CAR_WHEELBASE
        self.angle += math.degrees(turn_rate)
 
    def apply_friction(self) -> None: #freinage dû aux forces de frottements
        '''Slows the car down progressively (air friction).
        Returns:
            None
        '''
        self.vx *= 1 - CAR_AIR_FRICTION
        self.vy *= 1 - CAR_AIR_FRICTION
        if math.hypot(self.vx, self.vy) < 0.01:
            self.vx = 0.0
            self.vy = 0.0
 
    def apply_grip(self) -> None: #c'est ici que se joue le dérapage
        '''Cancels the lateral velocity within the limit of the grip, and detects drifting.
        Returns:
            None
        '''
        hx, hy = self.get_heading()
        forward_speed = self.vx * hx + self.vy * hy
        # Vitesse latérale = vitesse totale moins sa partie dans l'axe de la voiture
        lat_x = self.vx - forward_speed * hx
        lat_y = self.vy - forward_speed * hy
        lateral_speed = math.hypot(lat_x, lat_y)
        max_grip = self.grip * GRIP_SCALE
        if self.is_drifting:
            max_grip *= DRIFT_GRIP_RATIO   # pneus déjà en train de glisser : moins d'adhérence
 
        self.is_drifting = lateral_speed > max_grip
        if lateral_speed > 0:
            cancelled = min(lateral_speed, max_grip)
            ratio = cancelled / lateral_speed
            self.vx -= lat_x * ratio
            self.vy -= lat_y * ratio
        if self.is_drifting:
            self.vx *= 1 - self.drift_friction
            self.vy *= 1 - self.drift_friction
 
    def apply_terrain(self, terrain) -> None:
        '''Takes the grip, drift friction and traction of the terrain under the car.
        Parameters:
            terrain (RoadTile | IceTile | HerbeTile): The terrain tile under the car.
        Returns:
            None'''
        self.grip = terrain.grip
        self.drift_friction = terrain.drift_friction
        self.traction = terrain.traction
 
    def update_position(self) -> None:
        '''Updates the car's orientation, velocity and position.
        Returns:
            None
        '''
        self.apply_friction()
        self.update_orientation()
        self.apply_grip()
        self.x += self.vx
        self.y += self.vy
        self.keep_on_screen()
 
    def keep_on_screen(self) -> None: #pour que les voitures restent sur l'écran
        '''Prevents the car from leaving the map.
        Returns:
            None
        '''
        margin = CAR_HEIGHT / 2
        max_x = GRID_COLS * TILE_SIZE - margin
        max_y = GRID_ROWS * TILE_SIZE - margin
        if not (margin <= self.x <= max_x and margin <= self.y <= max_y):
            self.x = max(margin, min(max_x, self.x))
            self.y = max(margin, min(max_y, self.y))
            self.vx = 0.0
            self.vy = 0.0
 
    def build_sprite(self) -> pygame.Surface:
        '''Creates and returns a pygame.Surface representing the car.
        Returns:
            pygame.Surface: The surface representing the car's sprite.  '''
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        # Pare-brise : repère visuel pour reconnaître l'avant de la voiture
        pygame.draw.rect(surf, (255, 200, 200), (4, 4, CAR_WIDTH - 8, 12),
                         border_radius=3)
        return surf
 
    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:# pygame tourne dans le sens trigonométrique, comme self.angle
    
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect