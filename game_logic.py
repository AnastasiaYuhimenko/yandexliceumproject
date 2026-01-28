import math
import random
from enum import StrEnum

import arcade
from entities import Direction, Dot, Monster, Player
from maze import GHOST_SPAWN_POINTS, MAZE, MAZE_HEIGHT, MAZE_WIDTH, TILE_SIZE


class GameState(StrEnum):
    playing = "playing"
    gameover = "game_over"
    win = "win"


class GameLogic:
    def __init__(self):
        self.player = None
        self.ghosts = []
        self.dots = []
        self.score = 0
        self.game_state = GameState.playing

    def setup(self):
        spawn_points = GHOST_SPAWN_POINTS.copy()
        random.shuffle(spawn_points)
        self.player = Player(TILE_SIZE * 1.5, TILE_SIZE * 1.5)
        self.ghosts = [
            Monster(*spawn_points.pop(), id=0),
            Monster(*spawn_points.pop(), id=1),
        ]
        self.dots = []
        self.score = 0
        self.game_state = GameState.playing

        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if MAZE[y][x] == 2:
                    self.dots.append(Dot(TILE_SIZE * x + TILE_SIZE // 2, TILE_SIZE * y + TILE_SIZE // 2))

    def update(self):
        if self.game_state != GameState.playing:
            return

        self.player.update()
        pacman_pos = (self.player.center_x, self.player.center_y)

        for ghost in self.ghosts:
            ghost.update(pacman_pos)

        self._check_dot_collisions()
        self._check_ghost_collisions()

    def _check_dot_collisions(self):
        for dot in self.dots[:]:
            dist = math.hypot(dot.center_x - self.player.center_x, dot.center_y - self.player.center_y)

            if dist <= TILE_SIZE // 2:
                self.dots.remove(dot)
                self.score += 10

        if not self.dots:
            self.game_state = GameState.win

    def _check_ghost_collisions(self):
        pacman_radius = self.player.radius
        for ghost in self.ghosts:
            dist = math.hypot(self.player.center_x - ghost.center_x, self.player.center_y - ghost.center_y)

            if dist < pacman_radius + ghost.radius:
                self.game_state = GameState.gameover
                break

    def on_key_press(self, key, modifers):
        if self.game_state != GameState.playing:
            if key == arcade.key.ENTER or key == arcade.key.RETURN:
                self.setup()
            return

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.next_direction = Direction.UP

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.next_direction = Direction.DOWN

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.next_direction = Direction.LEFT

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.next_direction = Direction.RIGHT

    @property
    def get_pacman_pos(self):
        return (self.player.center_x, self.player.center_y, self.player.direction)

    @property
    def get_ghosts_data(self):
        return [(g.center_x, g.center_y, g.id) for g in self.ghosts]

    @property
    def get_dots_data(self):
        return [(d.center_x, d.center_y) for d in self.dots]

    @property
    def get_game_state(self):
        return self.game_state

    @property
    def get_score(self):
        return self.score
