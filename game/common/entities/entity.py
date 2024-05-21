import threading
from os import path
from time import sleep

import pygame

from game.common.bomberman_game import BombermanGame


class Entity:

    def __init__(self, bomberman_game: BombermanGame, x: int, y: int,
                 folder_path: str = "../../../sprites/entities/monster"):

        self.x = x
        self.y = y
        self.game = bomberman_game
        self.folder_path = folder_path
        self.files = {"up": f"{folder_path}/up_", "down": f"{folder_path}/down_",
                      "left": f"{folder_path}/left_", "right": f"{folder_path}/right_"}

        self.position = "down"
        self.position_state = "1"
        self.entity_moving = False

    """ Return the position of the entity """

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    """ All functions below return True if the movement is possible, False otherwise """

    def move_up(self) -> bool:

        if self._is_possible_position(self.x, self.y - 64):
            threading.Thread(target=self.move, args=(0, -1, "up")).start()
            return True
        self.position = "up"
        return False

    def move_down(self) -> bool:
        if self._is_possible_position(self.x, self.y + 64):
            threading.Thread(target=self.move, args=(0, 1, "down")).start()
            return True
        self.position = "down"
        return False

    def move_left(self) -> bool:
        if self._is_possible_position(self.x - 64, self.y):
            threading.Thread(target=self.move, args=(-1, 0, "left")).start()
            return True
        self.position = "left"
        return False

    def move_right(self) -> bool:
        if self._is_possible_position(self.x + 64, self.y):
            threading.Thread(target=self.move, args=(1, 0, "right")).start()
            return True
        self.position = "right"
        return False

    def move(self, x_modifier: int, y_modifier: int, position: str):

        """ Move the entity """

        self.position = position
        self.entity_moving = True

        sleep(0.13)
        self.kill(self.x, self.y)
        self.x += x_modifier * 21
        self.y += y_modifier * 21
        self.position_state = 2

        sleep(0.13)
        self.kill(self.x, self.y)
        self.x += x_modifier * 21
        self.y += y_modifier * 21
        self.position_state = 3

        sleep(0.13)
        self.kill(self.x, self.y)
        self.x += x_modifier * 22
        self.y += y_modifier * 22
        self.position_state = 1

        # 21 + 21 + 22 = 64 (the size of the block)

        self.entity_moving = False

    def kill(self, x, y):
        """ Kill the player """

        if self.__class__ == self.game.player.__class__:  # If the entity is the player
            for player in self.game.players:
                if any(player.get_x() == enemy.get_x() and player.get_y() == enemy.get_y() for enemy in self.game.enemies):
                    player.die()
            return  # The player can't kill himself after

        for player in self.game.players: # If the entity is an enemy
            if (player.get_x(), player.get_y()) == (x, y):
                player.die()

    def has_movement(self) -> bool:
        return self.entity_moving

    def _is_possible_position(self, x, y):
        """ Check if the position is possible to move """

        # Detect if bomb is in the same position as the entity (Not possible to move)
        for bomb in self.game.bombs:
            if (bomb.x, bomb.y) == (x, y):
                return False

        return self.game.get_block_type(x, y) == self.game.BlockType.GRASS

    def display(self):

        """ Display the entity on the screen """

        enemyPath = self.files.get(self.position) + str(self.position_state) + ".png"

        if path.exists(enemyPath):
            self.game.screen.blit(pygame.image.load(enemyPath), (self.x, self.y))
            return

        self.game.screen.blit(pygame.image.load(self.folder_path + "/default_1.png"), (self.x, self.y))
