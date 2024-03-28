from pydantic import BaseModel
import json


class WindowConfig(BaseModel):
    Title: str
    DisplayFPS: bool
    SizeX: int
    SizeY: int
    FrameRate: int

class AssetsConfig(BaseModel):
    Folder: str
    Maps: str
    Polygons: str

class AppConfig(BaseModel):
    Window: WindowConfig
    Assets: AssetsConfig
    
with open("config.json", "r") as f:
    data =  json.load(f)
    
CONFIG = AppConfig.model_validate(obj=data)

if __name__ == "__main__":
    print(CONFIG)
