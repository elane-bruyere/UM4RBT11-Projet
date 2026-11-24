import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_MAX_STEERING, CAR_STEERING_SPEED, CAR_WHEELBASE, GRID_COLS, GRID_ROWS, CAR_BRAKE_FORCE, CAR_AIR_FRICTION,
    ROAD_GRIP, ROAD_DRIFT_FRICTION, ROAD_TRACTION, DRIFT_GRIP_RATIO, GRIP_SCALE
)



class Car:
    '''Class representing a car in the game.
    Attributes:
        x (float): The x-coordinate of the car's position in pixels.
        y (float): The y-coordinate of the car's position in pixels.
        vx (float): The x-component of the car's velocity in pixels per frame.
        vy (float): The y-component of the car's velocity in pixels per frame.
        angle (float): The orientation of the car in degrees.
        steering_angle (float): The current steering angle of the car in degrees.
        grip (float): The grip coefficient of the car, affecting its ability to maintain traction.
        drift_friction (float): The friction coefficient applied when the car is drifting.
        traction (float): The traction coefficient of the car, affecting its acceleration and braking.
        is_drifting (bool): Indicates whether the car is currently drifting.
        color (tuple): The RGB color of the car.
    Methods:
        get_heading() -> tuple[float, float]: Returns the unit vector representing the car's heading direction.
        get_speed() -> float: Returns the signed speed of the car along its heading direction.
        accelerate() -> None: Increases the car's velocity in the direction of its heading.
        back_run() -> None: Decreases the car's velocity in the opposite direction of its heading.
        brake() -> None: Applies braking force to the car, reducing its forward speed or initiating reverse movement.
        steer(direction: int) -> None: Adjusts the car's steering angle based on the input direction.
        update_orientation() -> None: Updates the car's orientation based on its speed and steering angle.
        apply_friction() -> None: Applies air friction to the car, reducing its velocity over time.
        apply_grip() -> None: Applies grip mechanics to the car, affecting its lateral movement and drifting behavior.
        apply_terrain(terrain) -> None: Adopts the properties of the terrain the car is currently on, affecting its grip, drift friction, and traction.
        update_position() -> None: Updates the car's position based on its velocity and applies friction, orientation, and grip mechanics.
        keep_on_screen() -> None: Ensures the car remains within the bounds of the game screen, stopping it if it reaches the edges.
        build_sprite() -> pygame.Surface: Creates and returns a Pygame surface representing the car's visual appearance.
        get_rotated_sprite() -> tuple[pygame.Surface, pygame.Rect]: Returns the rotated sprite of the car and its corresponding rectangle for rendering.
    '''

    def __init__(self, start_col: int, start_row: int, color: tuple = (255, 0, 0)): #voiture rouge
        '''Initializes a Car with the specified starting column, row, and color.
        Parameters:
            start_col (int): The starting column index of the car in the grid.
            start_row (int): The starting row index of the car in the grid.
            color (tuple): The RGB color of the car. Default is red (255, 0, 0).
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
        '''Returns the unit vector representing the car's heading direction.
        Returns:
            tuple[float, float]: A tuple containing the x and y components of the heading unit vector.
        '''
        rad = math.radians(self.angle)
        return -math.sin(rad), -math.cos(rad)

    def get_speed(self) -> float:
        '''Returns the signed speed of the car along its heading direction.
        Returns:
            float: The signed speed of the car along its heading direction.
        '''
        hx, hy = self.get_heading()
        return self.vx * hx + self.vy * hy

    def accelerate(self) -> None:
        '''Increases the car's velocity in the direction of its heading.
        Returns:
            None
        '''
        hx, hy = self.get_heading()
        self.vx += hx * CAR_ACCELERATION * self.traction
        self.vy += hy * CAR_ACCELERATION * self.traction

    def back_run(self) -> None: ##marche arrière
        '''Decreases the car's velocity in the opposite direction of its heading.
        Returns:
            None
        '''
        hx, hy = self.get_heading()
        self.vx -= hx * CAR_ACCELERATION * self.traction
        self.vy -= hy * CAR_ACCELERATION * self.traction

    def brake(self) -> None: #avec la touche qui fait la marche arriere : si en route bim ça freine, sinon back_run
        '''Applies braking force to the car, reducing its forward speed or initiating reverse movement.
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
        '''Adjusts the car's steering angle based on the input direction.
        Parameters:
            direction (int): The direction of steering input (-1 for right, 1 for left, 0 for no input).
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
        '''Updates the car's orientation based on its speed and steering angle.
        Returns:
            None
        '''
        turn_rate = self.get_speed() * math.tan(math.radians(self.steering_angle)) / CAR_WHEELBASE
        self.angle += math.degrees(turn_rate)

    def apply_friction(self) -> None: #freinage dû aux forces de frottements
        '''Applies air friction to the car, reducing its velocity over time.
        Returns:
            None
        '''
        self.vx *= 1 - CAR_AIR_FRICTION
        self.vy *= 1 - CAR_AIR_FRICTION
        if math.hypot(self.vx, self.vy) < 0.01:
            self.vx = 0.0
            self.vy = 0.0

    def apply_grip(self) -> None: #c'est ici que se joue le dérapage
        '''Applies grip mechanics to the car, affecting its lateral movement and drifting behavior.
        Returns:
            None
        '''
        hx, hy = self.get_heading()
        forward_speed = self.vx * hx + self.vy * hy
        lat_x = self.vx - forward_speed * hx
        lat_y = self.vy - forward_speed * hy
        lateral_speed = math.hypot(lat_x, lat_y)
        max_grip = self.grip * GRIP_SCALE
        if self.is_drifting:
            max_grip *= DRIFT_GRIP_RATIO   # pneus déjà en train de glisser donc ça grippe moins

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
        '''Adopts the properties of the terrain the car is currently on, affecting its grip, drift friction, and traction.
        Parameters:
            terrain: The terrain object that provides grip, drift friction, and traction properties.
        Returns:
            None
        '''
        self.grip = terrain.grip
        self.drift_friction = terrain.drift_friction
        self.traction = terrain.traction

    def update_position(self) -> None:
        '''Updates the car's position based on its velocity and applies friction, orientation, and grip mechanics.
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
        '''Ensures the car remains within the bounds of the game screen, stopping it if it reaches the edges.
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
        '''Creates and returns a Pygame surface representing the car's visual appearance.
        Returns:
            pygame.Surface: The visual representation of the car.
        '''
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
       
        pygame.draw.rect(surf, (39, 214, 245), (4, 4, CAR_WIDTH - 8, 12),
                         border_radius=3)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        '''Returns the rotated sprite of the car and its corresponding rectangle for rendering.
        Returns:
            tuple[pygame.Surface, pygame.Rect]: A tuple containing the rotated sprite and its rectangle.
        '''
       
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
