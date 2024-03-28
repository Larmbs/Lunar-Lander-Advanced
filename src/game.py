from .events import EventsChecker, Event
from .const import ACCEL_GRAVITY, ANGLE_GRAVITY
from .entity import Entity, MoveableObject, CircleSprite, Lander, Terrain, StaticObject
import pygame as pg
import numpy as np



POINT = list[float]

class Game:
    def __init__(self, WIDTH:int, HEIGHT:int, dt:float):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        
        self.scroll:POINT = [0.0, 0.0]
        self.zoom = 0.06
        self.dt = dt
        
        center_x = WIDTH//2
        center_y = HEIGHT//2

        self.surface = pg.Surface((WIDTH, HEIGHT))

        self.objs:list[Entity] = []
    
        """OBJECTS"""
        sprite = CircleSprite("blue", 50)
        phys = MoveableObject(10, 20, 20, 20, 0, 0, 0)
        self.lander = Lander(phys, sprite, 3000)
        self.objs.append(self.lander)
        
        mount = Terrain("white", [1, 3, 4, 6, 20, 7, 1, -1, 4, 6, 7, 2, 3, 6, 7, 7, 20, 1], 50, 200)
        static = StaticObject(0, 0, 0, 0)
        terrain = Entity(static, mount)
        
        self.objs.append(terrain)
        
        """LISTENERS"""        
        self.event_checker = EventsChecker()
        self.event_checker.add_event(Event(pg.K_a, self.lander.turn_left))
        self.event_checker.add_event(Event(pg.K_d, self.lander.turn_right))
        self.event_checker.add_event(Event(pg.K_w, self.lander.thrust))
        
        #Screen Scroll Bounding Box
        padding = 50
        
        #X Scroll
        screen_range_x = range(-center_x + padding, center_x - padding)            
        def add_x_vel(): self.scroll[0] += phys.vx * self.dt
        def is_in_bounds_x() -> bool: 
            screen_x = int((self.lander.active.x - self.scroll[0]) * self.zoom)
            return screen_x not in screen_range_x and np.sign(screen_x) == np.sign(phys.vx) # type: ignore
                
        #Y Scroll
        screen_range_y = range(-center_y + padding, center_y - padding)
        def add_y_vel() -> None: self.scroll[1] += phys.vy * self.dt
        def is_in_bounds_y() -> bool:
            screen_y = int((self.lander.active.y - self.scroll[1]) * self.zoom)
            return screen_y not in screen_range_y and np.sign(screen_y) == np.sign(phys.vy)
        
        self.event_checker.add_event(Event(is_in_bounds_x, add_x_vel))
        self.event_checker.add_event(Event(is_in_bounds_y, add_y_vel))
        
        
    
    def update(self):
        self.event_checker.handle_events()
            
        for obj in self.objs:
            obj.active.apply_accel(ACCEL_GRAVITY, ANGLE_GRAVITY, self.dt)
            obj.active.update(self.dt)
    
    def render(self):
        self.surface.fill(pg.Color(0, 0, 0, 0))
        for obj in self.objs:
            obj.draw(self.zoom, self.scroll, self.surface)
        
    
    def get_screen(self):
        return self.surface
    