from .entity import Entity

from .physics import PhysicsBody, MoveableObject
from .sprite import Sprite

from pygame.math import clamp

class Lander(Entity):
    def __init__(self, physics:MoveableObject, sprite:Sprite, thrust_force:float) -> None:
        super().__init__(physics, sprite)
        
        self.thrust_force = thrust_force
        self.turn_inc = 0.1
        self.max_angle = 3.141
        self.min_angle = 0
    
    """Actions"""
    def thrust(self) -> None:
        self.get_physics().apply_force(self.thrust_force, self.active.rot, 1/60) # type: ignore
        
    def turn_left(self) -> None:
        self.active.rot += self.turn_inc
        self.clamp_angle()

    def turn_right(self) -> None:
        self.active.rot -= self.turn_inc
        self.clamp_angle()
        
    def clamp_angle(self) -> None:
        clamp(self.active.rot, self.min_angle, self.max_angle)

