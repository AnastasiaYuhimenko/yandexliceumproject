import math
import random
from enum import StrEnum

from maze import MAZE, MAZE_HEIGHT, MAZE_WIDTH, TILE_SIZE


class Direction(StrEnum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"


class Player:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.speed = 3
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.radius = TILE_SIZE // 2 - 2

    def update(self):
        new_x, new_y = self._calculate_next_pos(self.next_direction, self.speed)
        if not self._collides(new_x, new_y):
            self.center_x, self.center_y = new_x, new_y
            self.direction = self.next_direction

        new_x, new_y = self._calculate_next_pos(self.direction, self.speed)
        if not self._collides(new_x, new_y):
            self.center_x, self.center_y = new_x, new_y

    def _calculate_next_pos(self, direction, speed):
        x, y = self.center_x, self.center_y
        if direction == Direction.RIGHT:
            x += speed
        elif direction == Direction.LEFT:
            x -= speed
        elif direction == Direction.UP:
            y += speed
        elif direction == Direction.DOWN:
            y -= speed
        return x, y

    def _collides(self, x, y):
        maze_x, maze_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
        return maze_x < 0 or maze_x >= MAZE_WIDTH or maze_y < 0 or maze_y >= MAZE_HEIGHT or MAZE[maze_y][maze_x] == 1


class Monster:
    def __init__(self, x: float, y: float, id: int):
        self.center_x = x
        self.center_y = y
        self.speed = 2
        self.id = id
        self.direction = random.choice([Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN])
        self.radius = TILE_SIZE // 2 - 2

    def update(self, player_here):
        self.to = player_here
        best_diriction = self._choose_best_direction()
        self.direction = best_diriction
        self._move()

    def _choose_best_direction(self):
        directions = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]

        opposite = {
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
        }

        best_dir = None
        min_dist = float("inf")

        for direction in directions:
            if direction == opposite[self.direction]:
                continue

            new_x, new_y = self._calculate_next_pos(direction, self.speed)
            if self._collides(new_x, new_y):
                continue

            dist = math.hypot(
                new_x - self.to[0],
                new_y - self.to[1],
            )

            if dist < min_dist:
                min_dist = dist
                best_dir = direction
        if best_dir is None:
            return opposite[self.direction]
        return best_dir

    def _move(self):
        new_x, new_y = self._calculate_next_pos(self.direction, self.speed)
        if not self._collides(new_x, new_y):
            self.center_x, self.center_y = new_x, new_y

    def _calculate_next_pos(self, direction, speed):
        x, y = self.center_x, self.center_y
        if direction == Direction.RIGHT:
            x += speed
        elif direction == Direction.LEFT:
            x -= speed
        elif direction == Direction.UP:
            y += speed
        elif direction == Direction.DOWN:
            y -= speed
        return x, y

    def _collides(self, x, y):
        maze_x, maze_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
        return maze_x < 0 or maze_x >= MAZE_WIDTH or maze_y < 0 or maze_y >= MAZE_HEIGHT or MAZE[maze_y][maze_x] == 1


class Dot:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.collected = False
