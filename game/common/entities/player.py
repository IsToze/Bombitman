import sys

import pygame

from game.common.bomberman_game import BombermanGame
from game.common.entities.entity import Entity


class Player(Entity):

    def __init__(self, bomberman_game: BombermanGame):
        super().__init__(bomberman_game, 64, 64, "./sprites/entities/player")
        self.winner = False
        self.game_over = False

    def die(self, winner=False):
        print("\n"*100, "You died")
        self.game.players.remove(self)
        self.game_over = True
        self.winner = winner

    def is_die(self):
        """ Return True if the player is dead, False otherwise """
        return self.game_over

    def has_win(self):
        """ Return True if the player has win, False otherwise """
        return self.winner
