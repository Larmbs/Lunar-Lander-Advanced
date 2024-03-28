from dataclasses import dataclass
import ast


INDEX = int
MULTIPLIER = int

@dataclass
class Map:
    name:str
    heights:list[int]
    max_height:int
    POI:list[tuple[INDEX, MULTIPLIER]]
    
    def __repr__(self) -> str:
        return f"{self.name} | {self.max_height} | {self.POI} | {self.heights}"
    

class UnexpectedInput(Exception):
    pass
    
def load_maps(file_dir:str) -> list[Map]|UnexpectedInput:
    result:list[Map] = []
    
    try:
        with open(file_dir, "r") as f:
            raw_lines:list[str] = f.readlines()
            striped:list[str] = list(map(str.strip, raw_lines))
            
        #Single White Space Between Lines
        for i in reversed(range(1, len(striped))):
            if striped[i] == "" and striped[i - 1] == "":
                striped.pop(i)
                            
        #Creates Map Objects
        while len(striped) > 0:
            result.append(Map(
                striped.pop(0).split(":")[-1],                  #Name
                ast.literal_eval(striped.pop(0).split(":")[-1]),#Heights
                int(striped.pop(0).split(":")[-1]),             #Max Height
                ast.literal_eval(striped.pop(0).split(":")[-1]) #POI
            ))
            if striped:
                striped.pop(0)
    except Exception as e:
        return UnexpectedInput(e)
    
    return result
