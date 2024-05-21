import os
import random
import threading
from time import sleep

import pygame
import pyscroll
import pytmx

from game.common.bomb import Bomb
from game.common.bomberman_game import BombermanGame
from game.common.entities.entity import Entity
from game.common.entities.player import Player
from game.solo.entity.ghost import Ghost


class BombermanSolo(BombermanGame):
    """ Open a window for a solo bomberman's game """

    def __init__(self):

        # Load the game
        super().__init__()
        tmx_data = pytmx.util_pygame.load_pygame('map/solo_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Load map (grass, wall, stone)
        self.breakable_blocks = pygame.image.load('sprites/blocs/stone.png')
        self._load_breakable_blocks()
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

        # Load enemies
        self._load_enemies(3)

        # Load Player
        self.player = Player(self)
        self.players.append(self.player)
        self.clock = pygame.time.Clock()

    def _load_breakable_blocks(self):

        """ Load the breakable blocks on the map """

        for x in range(64, 640, 64):
            for y in range(64, 640, 64):
                if random.randint(1, 2) == 1:
                    self.blocs.append((x, y))

        # Remove 2 blocks to make sure the entities is not blocked

        coordinates_remove = [(64, 64), (128, 64), (64, 128), (576, 576)]
        for coord in coordinates_remove:
            if coord in self.blocs:
                self.blocs.remove(coord)

    def _load_enemies(self, enemies_amount):

        """Load the enemies on the map"""

        while len(self.enemies) < enemies_amount:

            coord_x = random.randint(3, 9)  # Pour éviter d'être sur le personnage
            coord_y = random.randint(4, 9)

            if coord_x < 5 and coord_y < 5:
                continue  # For the enemies not spawn on the entities, because he spawn in an area of 3x3

            coord_x *= 64
            coord_y *= 64

            if (coord_x, coord_y) in self.blocs:
                self.blocs.remove((coord_x, coord_y))  # Remove the blocs where the enemies spawn

            if (coord_x, coord_y - 64) in self.blocs:
                self.blocs.remove((coord_x, coord_y - 64))  # Remove the block above to have minimal movement

            if (coord_x, coord_y) in self.enemies:
                continue

            self.enemies.append(Ghost(self, coord_x, coord_y))

    def run(self):

        """Run the game in solo mode"""

        running = True

        while running:

            if self.player.is_die():

                font = pygame.font.SysFont(None, 74)

                if self.player.has_win():
                    green = (0, 255, 0)
                    text = font.render("Win !", True, green)
                    text_rect = text.get_rect()
                    text_rect.center = (320, 320)
                    self.screen.blit(text, text_rect)
                else:
                    red = (255, 0, 0)
                    text = font.render("Lost !", True, red)
                    text_rect = text.get_rect()
                    text_rect.center = (320, 320)
                    self.screen.blit(text, text_rect)

                pygame.display.flip()
                sleep(3)
                pygame.quit()

                return

            self.group.draw(self.screen)

            for bloc in self.blocs:
                self.screen.blit(self.breakable_blocks, bloc)

            self.screen.blit(pygame.image.load('sprites/blocs/door.png'), (320, 0))

            for enemy in self.enemies:
                if not isinstance(enemy, Player):
                    enemy.display()

            if(self.player.get_x(), self.player.get_y()) == (320, 64):
                if len(self.enemies) == 0 and self.player.position == "up":
                    print("You win !")
                    running = False

            self.show_bomb()
            self.show_explode("sprites/entities/explosion/explosion.png")

            # Movement of the player
            if not self.player.has_movement():

                keys = pygame.key.get_pressed()

                if keys[pygame.K_z]:
                    self.player.move_up()
                elif keys[pygame.K_s]:
                    self.player.move_down()
                elif keys[pygame.K_q]:
                    self.player.move_left()
                elif keys[pygame.K_d]:
                    self.player.move_right()
                elif keys[pygame.K_SPACE]:
                    self.spawn_bomb(self.player.get_x(), self.player.get_y())

            self.player.display()
            pygame.display.flip()

            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

    def open_game(self):
        self.run()

    def spawn_bomb(self, x: int, y: int):

        """ Spawn a bomb at the position (x, y) """

        if any(bomb.x == x and bomb.y == y for bomb in self.bombs):
            return

        bomb = Bomb(self, x, y, 2)
        self.bombs.append(bomb)
        threading.Thread(target=bomb.ignite).start()
