import os
import sys

import pygame as pg

from config import CONFIG, AppConfig
from game import Game


BASE_PATH = os.getcwd()

class App:
    def __init__(self, config:AppConfig):
        self.config = config
        
        self.RES = config.Window.SizeX, config.Window.SizeY

        pg.init()

        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.game = Game(config, self.clock)

    def update(self):
        self.game.update()

    def render(self):
        self.game.render()

    def run(self):
        while True:
            self.update()

            [self.exit() for event in pg.event.get() if event.type == pg.QUIT]

            self.render()
            self.screen.blit(self.game.get_screen(), (0, 0))

            self.clock.tick(self.config.Window.FrameRate)

            pg.display.flip()

    def exit(self):
        pg.quit()
        sys.exit()


def main():
    app = App(CONFIG)
    app.run()


if __name__ == "__main__":
    main()
