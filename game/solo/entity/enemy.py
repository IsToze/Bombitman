from game.common.bomberman_game import BombermanGame
from game.common.entities.entity import Entity


class Enemy(Entity):

    def __init__(self, bomberman_game: BombermanGame, x: int, y: int):
        super().__init__(bomberman_game, x, y, "./sprites/entities/monster/ghost_1")

