from typing import Union
from pydantic import BaseModel, ValidationError
import json


VALUE= Union[int, float]
POINT = tuple[VALUE, VALUE]
ColorValue = tuple[int, int, int]

class MapJSON(BaseModel):
    Name:str
    Heights:list[int]
    Vertical_Stretch:int
    Horizontal_Stretch:int
    POIS:list[POINT]
    
def get_maps(json_file:str) -> list[MapJSON]:
    with open(json_file, "r") as f:
        data = json.load(fp=f)
        
    result:list[MapJSON] = []
    if not isinstance(data, list):
        data = [data]
        
    for model in data:
        try:
            result.append(MapJSON.model_validate(model))
        except ValidationError as e:
            raise e
    
    return result
