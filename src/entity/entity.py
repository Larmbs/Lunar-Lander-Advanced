from .physics import PhysicsBody
from .sprite import Sprite
import pygame as pg


POINT = list[float]
class Entity:
    def __init__(self, physics:PhysicsBody, sprite:Sprite):
        self.active = physics
        self.sprite = sprite
        
    def get_physics(self) -> PhysicsBody:
        return self.active
    
    def get_sprite(self) -> Sprite:
        return self.sprite
        
    def draw(self, zoom:float, scroll:POINT, surface:pg.Surface) -> None:
        self.sprite.draw(self.active.get_pos(), self.active.rot, zoom, (int(scroll[0]), int(scroll[1])), surface)
