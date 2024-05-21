import threading
import random
from time import sleep

from game.common.bomberman_game import BombermanGame
from game.common.entities.entity import Entity


class Ghost(Entity):

    def __init__(self, bomberman_game: BombermanGame, x: int, y: int):
        super().__init__(bomberman_game, x, y, "./sprites/entities/monster/")
        threading.Thread(target=self.displace).start()

    def displace(self):

        sleep(1)

        random_number = random.randint(0, 3)

        if random_number == 0:
            self.move_up()
        elif random_number == 1:
            self.move_down()
        elif random_number == 2:
            self.move_left()
        elif random_number == 3:
            self.move_right()

        self.displace()
