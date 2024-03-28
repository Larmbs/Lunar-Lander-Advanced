import os
import sys

import pygame as pg

from config import Config
from src.game import Game

BASE_PATH = os.getcwd()


class App:
    def __init__(self, WIDTH:int=1000, HEIGHT:int=600):
        self.RES = WIDTH, HEIGHT

        pg.init()

        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.tick_rate = 120

        self.game = Game(WIDTH, HEIGHT, 1 / self.tick_rate)

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

            self.clock.tick(self.tick_rate)

            pg.display.flip()

    def exit(self):
        pg.quit()
        sys.exit()


def main():
    config = Config()  # noqa: F841
    app = App()
    app.run()


if __name__ == "__main__":
    main()
