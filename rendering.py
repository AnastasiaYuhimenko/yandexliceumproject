import arcade
from entities import Direction
from maze import MAZE, MAZE_HEIGHT, MAZE_WIDTH, TILE_SIZE


class Renderer:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.offset_x = 95
        self.offset_y = 75
        self.walls = arcade.SpriteList()
        self.wall_sprite = arcade.Sprite("Sprites/BrickWallSprite.png")
        self.walls.append(self.wall_sprite)

        self.player_sprites = {
            Direction.UP: arcade.Sprite("Sprites/PlayerSpriteUp.png", scale=0.7),
            Direction.DOWN: arcade.Sprite("Sprites/PlayerSpriteDown.png", scale=0.7),
            Direction.LEFT: arcade.Sprite("Sprites/PlayerSpriteLeft.png", scale=0.7),
            Direction.RIGHT: arcade.Sprite("Sprites/PlayerSpriteRight.png", scale=0.7),
        }
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprites[Direction.RIGHT])

        self.ghost_lists = {
            0: arcade.SpriteList(),
            1: arcade.SpriteList(),
        }

        self.ghost_lists[0].append(arcade.Sprite("Sprites/MonsterSprite02.png", scale=0.7))
        self.ghost_lists[1].append(arcade.Sprite("Sprites/MonsterSprite01.png", scale=0.7))

        self.dots = arcade.SpriteList()
        self.dot_sprite = arcade.Sprite("Sprites/CoinSprite.png")
        self.dots.append(self.dot_sprite)

    def draw(self):
        arcade.set_background_color(arcade.color.BLACK)
        self._draw_maze()
        self._draw_player()
        self._draw_ghosts()
        self._draw_dots()
        self._draw_score()

    def _draw_maze(self):
        wall = self.walls[0]
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if MAZE[y][x] == 1:
                    wall.center_x = x * TILE_SIZE + TILE_SIZE / 2 + self.offset_x
                    wall.center_y = y * TILE_SIZE + TILE_SIZE / 2 + self.offset_y
                    self.walls.draw()

    def _draw_player(self):
        x, y, direction = self.game_logic.get_pacman_pos

        sprite = self.player_sprites[direction]
        sprite.center_x = x + self.offset_x
        sprite.center_y = y + self.offset_y

        self.player_list[0] = sprite
        self.player_list.draw()

    def _draw_ghosts(self):
        for x, y, id in self.game_logic.get_ghosts_data:
            sprite = self.ghost_lists[id][0]
            sprite.center_x = x + self.offset_x
            sprite.center_y = y + self.offset_y
            self.ghost_lists[id].draw()

    def _draw_dots(self):
        dot = self.dots[0]
        for x, y in self.game_logic.get_dots_data:
            dot.center_x = x + self.offset_x
            dot.center_y = y + self.offset_y
            self.dots.draw()

    def _draw_score(self):
        arcade.draw_text(
            f"Score: {self.game_logic.get_score}",
            10,
            570,
            arcade.color.WHITE,
            20,
        )
