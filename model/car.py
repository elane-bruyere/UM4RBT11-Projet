# Kart-Engine v2.3
import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_MAX_STEERING, CAR_STEERING_SPEED, CAR_WHEELBASE, GRID_COLS, GRID_ROWS, CAR_BRAKE_FORCE, CAR_AIR_FRICTION
)
 
 
class Car:
    '''
      Class representing a car in the game.
 
      Attributes:
          x (float): The x-coordinate of the car's position.
          y (float): The y-coordinate of the car's position.
          speed (float): The current speed of the car (pixels per frame).
          angle (float): The orientation of the car in degrees. 0 means the car
              points up, and a positive angle is a counter-clockwise rotation
              (the car turns left).
          steering_angle (float): The angle of the steering wheel in degrees.
              Positive means left, negative means right.
          color (tuple): The RGB color of the car.
          sprite (pygame.Surface): The visual representation of the car.
 
      Methods:
          accelerate(): Increases the car's speed by a fixed acceleration value.
          back_run(): Decreases the car's speed by a fixed acceleration value (reverse).
          brake(): Slows the car down while moving forward, then reverses once stopped.
          steer(direction): Changes the steering angle (+1 left, -1 right, 0 recenter).
          apply_friction(): Slows the car down progressively (air friction).
          update_orientation(): Rotates the car according to its speed and steering angle.
          update_position(): Updates the car's orientation and position.
          keep_on_screen(): Prevents the car from leaving the map.
          build_sprite(): Creates and returns a pygame.Surface representing the car.
          get_rotated_sprite(): Returns the rotated sprite and its corresponding rectangle for rendering.
      '''
 
    def __init__(self, start_col: int, start_row: int, color: tuple = (255, 0, 0)): #voiture rouge 
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.steering_angle: float = 0.0
        self.color = color
        self.sprite = self.build_sprite()
 
    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION
 
    def back_run(self) -> None: ##marche arrière 
        self.speed -= CAR_ACCELERATION
 
    def brake(self) -> None: #avec la touche qui fait la mar che arriere : si en route bim ça freine, sinon back_run 
        if self.speed > 0:
            self.speed = max(0.0, self.speed - CAR_BRAKE_FORCE)
        else:
            self.back_run()
 
 
    def steer(self, direction: int) -> None: #change l'angle de braquage si +1 -> gauche; si -1 -> droite sinon -> aucune commande (avec 0)
        if direction != 0:
            self.steering_angle += direction * CAR_STEERING_SPEED
        elif abs(self.steering_angle) <= CAR_STEERING_SPEED:
            self.steering_angle = 0.0
        else: #aucune commande donc 0 -> le volant revient progressivement vers le centre
            self.steering_angle -= math.copysign(CAR_STEERING_SPEED, self.steering_angle) # le volant ne peut pas tourner plus loin que l'angle max def dans le fichier csts
        self.steering_angle = max(-CAR_MAX_STEERING,
                                  min(CAR_MAX_STEERING, self.steering_angle))
 
    def update_orientation(self) -> None: #fait tourner la voiture 
 
        '''La vitesse de rotation est proportionnelle à la vitesse de la voiture :
        à l'arrêt elle ne tourne pas, et en marche arrière le sens s'inverse.
        '''
        turn_rate = self.speed * math.tan(math.radians(self.steering_angle)) / CAR_WHEELBASE
        self.angle += math.degrees(turn_rate)
 
    def apply_friction(self) -> None: #freinage dû aux forces de frottements
        '''Frottements de l'air : la voiture perd une petite part de sa vitesse à chaque image.'''
        self.speed *= 1 - CAR_AIR_FRICTION
        if abs(self.speed) < 0.01:
            self.speed = 0.0
 
    def update_position(self) -> None:
        self.apply_friction()
        self.update_orientation()
        rad = math.radians(self.angle)
        # L'axe y de l'écran pointe vers le bas, d'où les signes moins
        self.x += -math.sin(rad) * self.speed
        self.y += -math.cos(rad) * self.speed
        self.keep_on_screen()
 
    def keep_on_screen(self) -> None: #pour que les voitures restent sur l'écran 
        '''Bloque la voiture dans les limites de la carte et annule sa vitesse si elle touche un bord.'''
        margin = CAR_HEIGHT / 2
        max_x = GRID_COLS * TILE_SIZE - margin
        max_y = GRID_ROWS * TILE_SIZE - margin
        if not (margin <= self.x <= max_x and margin <= self.y <= max_y):
            self.x = max(margin, min(max_x, self.x))
            self.y = max(margin, min(max_y, self.y))
            self.speed = 0
 
    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        # Pare-brise : repère visuel pour reconnaître l'avant de la voiture
        pygame.draw.rect(surf, (255, 200, 200), (4, 4, CAR_WIDTH - 8, 12),
                         border_radius=3)
        return surf
 
    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        # pygame tourne dans le sens trigonométrique, comme self.angle
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
 