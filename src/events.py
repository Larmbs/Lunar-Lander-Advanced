from typing import Callable, Union
import pygame as pg



CONDITION = Callable[[], bool]
KEY_ID = int
EVENT = Union[CONDITION, KEY_ID]
ACTION = Callable[[], None]

class Event:
    def __init__(self, condition:EVENT, action:ACTION, max_highs:int=-1):
        self.condition = condition
        self.action = action
        self.max_highs = max_highs if max_highs > 0 else -1
    
    #Returns bool determining to delete event
    def update(self, keys:pg.key.ScancodeWrapper) -> bool:
        if isinstance(self.condition, int):
            if  keys[self.condition]:
                self.action()
                self.max_highs -= 1
        elif self.condition():
            self.action()
            self.max_highs -= 1
            
        return self.max_highs == 0
            
        
class EventsChecker:
    def __init__(self) -> None:
        self.events_to_check:list[Event] = []
    
    def add_event(self, event:Event) -> None:
        self.events_to_check.append(event)
        
    def handle_events(self) -> None:
        keys_pressed = pg.key.get_pressed()

        for event in self.events_to_check:
            if event.update(keys_pressed):
                self.events_to_check.remove(event)
                
def create_timed_event(action:ACTION, ticks:int) -> Event:
    return Event(lambda:True, action, ticks)
    