from src import EventsChecker, Event
from src import ACCEL_GRAVITY, ANGLE_GRAVITY, TERRAIN_SPACING, TERRAIN_THICKNESS
from src import Entity, MoveableObject, CircleSprite, Lander, TerrainSprite, StaticObject
import pygame as pg
import numpy as np
from src.data import MapJSON, get_maps, ValidationError, PolygonJSON, get_polygons
from src import DebugDisplay
from config import AppConfig
import os



POINT = list[float]

class Game:
    def __init__(self, config:AppConfig, clock:pg.time.Clock):
        self.config = config
        self.clock = clock
        
        self.WIDTH = config.Window.SizeX
        self.HEIGHT = config.Window.SizeY
        
        self.scroll:POINT = [0.0, 0.0]
        self.zoom = 0.2
        self.dt = 1/config.Window.FrameRate
        
        center_x = self.WIDTH//2
        center_y = self.HEIGHT//2

        self.surface = pg.Surface((self.WIDTH, self.HEIGHT))

        self.objs:list[Entity] = []
        
        maps:list[MapJSON] = get_maps(os.path.join(config.Assets.Folder, config.Assets.Maps))
        polygons:list[PolygonJSON] = get_polygons(os.path.join(config.Assets.Folder, config.Assets.Polygons))
    
        """OBJECTS"""
        sprite = CircleSprite("blue", 50)
        phys = MoveableObject(10, 20, 20, 20, 0, 0, 0)
        self.lander = Lander(phys, sprite, 3000)
        self.objs.append(self.lander)
        
        
        if isinstance(maps, list):
            mount = TerrainSprite("white", maps[0].Heights, maps[0].Vertical_Stretch, maps[0].Horizontal_Stretch, TERRAIN_THICKNESS)
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
        
        self.debug_display = DebugDisplay()
        self.debug_display.add_node(lambda:F"{self.config.Window.Title}", True)
        self.debug_display.add_node(lambda:F"FPS {int(self.clock.get_fps())}", True)
    
    def update(self):
        self.event_checker.handle_events()
            
        for obj in self.objs:
            obj.active.apply_accel(ACCEL_GRAVITY, ANGLE_GRAVITY, self.dt)
            obj.active.update(self.dt)
    
    def render(self):
        self.surface.fill(pg.Color(0, 0, 0, 0))
        for obj in self.objs:
            obj.draw(self.zoom, self.scroll, self.surface)
            
        self.debug_display.display_title()
        
    
    def get_screen(self):
        return self.surface
    