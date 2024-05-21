from time import sleep

from game.common.bomberman_game import BombermanGame
from game.common.entities.player import Player


class Bomb:

    def __init__(self, game: BombermanGame, x: int, y: int, timer: int):
        """ Create a bomb """

        self.game = game
        self.x = x
        self.y = y
        self.timer = timer
        self.exploded = False
        self.bomb_image = "./sprites/entities/explosion/bomb_1.png"

    def ignite(self):
        """ Ignite the bomb """

        self.bomb_image = "./sprites/entities/explosion/bomb_1.png"
        sleep(self.timer / 3)

        self.bomb_image = "./sprites/entities/explosion/bomb_2.png"
        sleep(self.timer / 3)

        self.bomb_image = "./sprites/entities/explosion/bomb_3.png"
        sleep(self.timer / 3)

        self.exploded = True
        self.bomb_image = "./sprites/entities/explosion/explosion.png"
        sleep(2)

        self.bomb_image = None
        self.exploded = False

    def kill_entities(self, locations):

        """ Kill all entities and remove block and kill player in the given locations """

        self.game.blocs = [block for block in self.game.blocs if block not in locations]
        self.game.enemies = [enemy for enemy in self.game.enemies if (enemy.get_x(), enemy.get_y()) not in locations]

        for player in self.game.players:
            if (player.get_x(), player.get_y()) in locations:
                player.die()

    def _abs(self, value: int) -> int:
        """ Return the absolute value of the given value """

        return value if value > 0 else -value

    def get_image(self) -> str:
        """ Return the image of the bomb """

        return self.bomb_image

    def has_explosed(self) -> bool:
        """ Return True if the bomb has exploded, False otherwise """

        return self.exploded
