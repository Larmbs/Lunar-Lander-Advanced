from numpy import sin, cos, arctan2
from typing import Tuple


PI = 3.141

class StaticObject:
    def __init__(self, m:int, x:float, y:float, rot:float) -> None:
        self.mass = m
        
        self.x = x
        self.y = y
        self.rot = rot
    
    def get_pos(self) -> Tuple[float, float]:
        return self.x, self.y
        
    def set_pos(self, x:float=0.0, y:float=0.0) -> None:
        self.x = x
        self.y = y
        
    def set_rotation(self, rot:float=0.0) -> None:
        self.rot = rot
        
    def update(self, dt:float) -> None:
        pass
    
    def apply_accel(self, mag:float, angle:float, dt:float) -> None:
        pass
    
    def __repr__(self) -> str:
        return "Physics"
    
    
class MoveableObject(StaticObject):
    def __init__(self, m:int, x:float, y:float, rot:float, vx:float, vy:float, vr:float) -> None:
        super().__init__(m, x, y, rot)
        
        self.vx = vx
        self.vy = vy
        self.vr = vr
        
    def update(self, dt:float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rot += self.vr * dt
        
    def get_heading(self) -> float:
        return arctan2(self.vx, self.vy)
        
    def apply_accel(self, mag:float, angle:float, dt:float) -> None:
        self.vx += cos(angle) * mag * dt
        self.vy += sin(angle) * mag * dt

    def apply_force(self, mag:float, angle:float, dt:float) -> None:
        self.vx += cos(angle) * mag / self.mass * dt
        self.vy += sin(angle) * mag / self.mass * dt

    def apply_rotational_accel(self, mag:float, dt:float) -> None:
        self.vr += mag * dt
        
    def apply_frictional_force(self, friction_coefficient:float, normal_force:float, dt:float, normal_direction:float|None=None) -> None:
        if not normal_direction:
            normal_direction = self.get_heading() + PI
        magnitude = normal_force * friction_coefficient * dt
        direction = normal_direction + PI/2
        self.apply_accel(magnitude, direction, dt)
    