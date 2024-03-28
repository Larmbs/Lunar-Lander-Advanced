from typing import Callable
import pygame as pg



pg.font.init()
DEBUG = Callable[[], str]
    
class DebugDisplay:
    font:pg.font.Font = pg.font.Font('freesansbold.ttf', 32)
    
    def __init__(self) -> None:            
        self.title_debugs:list[DEBUG] = []
        self.debugs:list[DEBUG] = []
            
    def add_node(self, node:DEBUG, is_title:bool=False) -> None:
        if is_title: 
            self.title_debugs.append(node)
        self.debugs.append(node)
        
    def get_text(self, nodes:list[DEBUG]) -> list[str]:
        result:list[str] = []
        for node in nodes:
            result.append(node())
        return result
    
    def display_heads_up(self, surface:pg.Surface):
        text = str.join("\n", self.get_text(self.debugs))
        text_obj = self.font.render(text, True, "white")
        textRect = text_obj.get_rect()
        surface.blit(text_obj, (0, 0), textRect)
    
    def display_title(self):
        text = str.join(" | ", self.get_text(self.title_debugs))
        pg.display.set_caption(text)
          