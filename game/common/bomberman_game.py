import threading
from enum import Enum
from time import sleep

import pygame
import os


class BombermanGame:

    def __init__(self):

        super().__init__()

        self.blocs = []
        self.bombs = []  # Bombs
        self.explode = []
        self.enemies = []
        self.players = []

        # Create the Frame
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((0, 0))
        pygame.display.set_caption('Solo Bomberman')

        music_path = os.path.join("./sprites/sounds/Kirby_song.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        self.explosion_sound = pygame.mixer.Sound("./sprites/sounds/explosion.mp3")
        self.explosion_sound.set_volume(0.12)

    class BlockType(Enum):
        GRASS = 0
        WALL = 1
        STONE = 2
        ENEMY = 3
        BOMB = 4

    def get_block_type(self, x, y) -> BlockType:

        """ Return the type of the block at the position GamePos(x, y) """

        if (x == 0 or y == 0) or (x == 640 or y == 640):
            return self.BlockType.WALL

        if (x, y) in self.blocs:
            return self.BlockType.STONE

        if (x, y) in self.enemies:
            return self.BlockType.ENEMY

        if (x, y) in self.bombs:
            return self.BlockType.BOMB

        return self.BlockType.GRASS

    def get_game_block_at(self, x, y):

        """ Convert a position in the map (1, 2, 3) to position in the game(64, 128, 192) """

        x *= 64
        y *= 64
        return x, y, self.get_block_type(x, y)

    def show_bomb(self):

        """ Show the bombs on the screen """

        for bomb in self.bombs:

            if bomb.get_image() is not None:
                self.screen.blit(pygame.image.load(bomb.get_image()), (bomb.x, bomb.y))

            if bomb.has_explosed():
                locations = self.explode_bomb(bomb)
                bomb.kill_entities(locations)
                self.bombs.remove(bomb)

    def show_explode(self, image):

        """ Show the explosion on the screen """

        image = pygame.image.load(image)

        for locations in self.explode:
            for location in locations:

                for enemy in self.enemies:
                    if (enemy.x, enemy.y) == (location[0], location[1]):
                        self.enemies.remove(enemy)

                for player in self.players:
                    if (player.get_x(), player.get_y()) == (location[0], location[1]):
                        player.die()

                self.screen.blit(image, (location[0], location[1]))

    def _remove_bomb(self, locations):
        sleep(1)
        self.explode.remove(locations)

    def explode_bomb(self, bomb):

        """ Explode all bomb """

        if not bomb.has_explosed():
            return []

        remove_enemies = []
        remove_blocs = []

        x, y = bomb.x, bomb.y
        directions = [(64, 0), (0, 64), (-64, 0), (0, -64)]
        approved_directions = [True, True, True, True]

        for i in range(3):

            for index_x, (dx, dy) in enumerate(directions):

                if not approved_directions[index_x]:
                    continue

                x_location = x + dx * i
                y_location = y + dy * i

                if self.get_block_type(x_location, y_location) != self.BlockType.GRASS:
                    approved_directions[index_x] = False

                if 0 < x_location < 640 and 0 < y_location < 640:
                    remove_enemies.append((x_location, y_location, bomb.get_image()))
                    remove_blocs.append((x_location, y_location))
                    self.screen.blit(pygame.image.load(bomb.get_image()), (x_location, y_location))

        self.explode.append(remove_enemies)

        for enemy in self.enemies:
            if (enemy.x, enemy.y) in remove_enemies:
                self.enemies.remove(enemy)

        for bloc in remove_blocs:
            if bloc in self.blocs:
                self.blocs.remove(bloc)

        self.explosion_sound.play()

        threading.Thread(target=self._remove_bomb, args=(remove_enemies,)).start()

        return remove_enemies
