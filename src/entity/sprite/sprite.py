from typing import Tuple, Union
import pygame as pg
from numpy import sin, cos
from .const import ColorValue, Clear
from abc import ABC, abstractmethod


VALUE = Union[int, float]
POINT = Tuple[VALUE, VALUE]

class Sprite(ABC):
    @abstractmethod
    def __init__(self) -> None:
        ...
    
    @abstractmethod
    def draw(self, pos:POINT, rot:float, zoom:float, scroll:POINT, surface:pg.Surface) -> None:
        ...
    
    """Just Draws a Line to help see direction"""
    def rotation_arrow(self, pos:POINT, rot:float, surface:pg.Surface):
        pg.draw.line(surface, "white", pos, (pos[0] + 50 * cos(rot), pos[1] + -50 * sin(rot)))
        
    def world_to_screen_cords(self, pos:POINT, zoom:float, scroll:POINT, surface:pg.Surface) -> POINT:
        center_x = surface.get_width()//2
        center_y = surface.get_height()//2
        return int((pos[0] - scroll[0]) * zoom) + center_x, -int((pos[1] - scroll[1]) * zoom) + center_y
    
    def __repr__(self) -> str:
        return "Sprite"


class CircleSprite(Sprite):
    def __init__(self, color:ColorValue, radius:int) -> None:
        self.color = color
        self.radius = radius
    
    def draw(self, pos:POINT, rot:float, zoom:float, scroll:POINT, surface:pg.Surface) -> None:
        screen_pos = self.world_to_screen_cords(pos, zoom, scroll, surface)
        
        #Drawing To Screen
        pg.draw.circle(surface, self.color, screen_pos, self.radius*zoom)
        self.rotation_arrow(screen_pos, rot, surface)
        
            
class TerrainSprite(Sprite):
    def __init__(self, color:ColorValue, heights:list[int], max_height:int, spacing:int, thickness:int=1):
        self.color = color
        
        self.heights = heights
        self.max_height = max_height
        self.spacing = spacing
        
        self.thickness = thickness
        
        """Total Width Of Terrain"""
        self.width = len(heights) * spacing
        
    def get_points(self) -> list[POINT]:
        result:list[POINT] = []
        
        for i, height in enumerate(self.heights):
            result.append((i*self.spacing, height*self.max_height))
            
        return result
    
    def transform_points(self, points:list[POINT], zoom:float, scroll:POINT, surface:pg.Surface) -> list[POINT]:
        result = []
        for point in points:
            result.append(self.world_to_screen_cords(point, zoom, scroll, surface))
        return result
    
    def scrolled_points(self, points:list[POINT], offset:int, world_width:int) -> list[POINT]:
        result:list[POINT] = []
        
        chunks:int = world_width // self.width + 2
        half_chunks = chunks//2
        
        for i in range(-half_chunks, half_chunks + 1):
            for point in points:
                result.append((point[0] + (offset+i) * self.width, point[1]))
        
        return result
    
    def draw(self, pos:POINT, rot:float, zoom:float, scroll:POINT, surface:pg.Surface) -> None:
        offset = int(scroll[0] // self.width)
        world_width = int(surface.get_width() / zoom)
        world_points = self.scrolled_points(self.get_points(), offset, world_width)
        points = self.transform_points(world_points, zoom, scroll, surface)
        pg.draw.lines(surface, self.color, False, points, self.thickness)
                
        
class PolygonSprite(Sprite):
    def __init__(self, color:ColorValue, points:list[POINT]) -> None:
        self.color = color
        self.points = points
        self.surface = pg.Surface((200,200))
       
    def draw(self, pos:POINT, rot:float, zoom:float, scroll:POINT, surface:pg.Surface) -> None:
        self.surface.fill(Clear)
        pg.draw.polygon(self.surface, self.color, self.points)
        s = pg.transform.rotate(self.surface, rot)
        surface.blit(s, pos)
        