from .entity import Entity
from .physics import PhysicsBody
from .sprite import Sprite


class Basic(Entity):
    def __init__(self, physics:PhysicsBody, sprite:Sprite) -> None:
        super().__init__(physics, sprite)
    
    """Actions"""
    def move_up(self) -> None:
        self.active.y += 5
        
    def move_down(self) -> None:
        self.active.y -= 5
        
    def move_left(self) -> None:
        self.active.x += 5
        
    def move_right(self) -> None:
        self.active.x -= 5
        