import os
import sys

import arcade
from game_logic import GameLogic, GameState
from rendering import Renderer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

sound = arcade.load_sound("Sounds/3-track-3.mp3")

win_sound = arcade.load_sound("Sounds/8f1b691a4ba209b.mp3")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def save_result_to_file(store: int, outcome: str):
    # Здесь записываются результаты в txt файл (тк в критериях оценки есть "Хранение данных")
    try:
        os.makedirs("results", exist_ok=True)
        file_path = os.path.join("results", "game_results.txt")
        if outcome == "win":
            result_line = f"Последний результат: победа" \
                          f"счет: {store}\n"
        else:
            result_line = f"Последний результат: поражение" \
                          f"счет: {store}\n"
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(result_line)

    except Exception as e:
        print(e)


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_list = arcade.SpriteList()

        self.background = arcade.Sprite(
            "Sprites/MenuBackground.png")
        self.background.center_x = CENTER_X
        self.background.center_y = CENTER_Y
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
        self.background_list.append(self.background)

        self.button_list = arcade.SpriteList()

        self.play_button = arcade.Sprite(
            "Sprites/PlayButton.png")
        self.play_button.center_x = CENTER_X
        self.play_button.center_y = CENTER_Y - 75

        self.settings_button = arcade.Sprite(
            "Sprites/SettingButton.png")
        self.settings_button.center_x = CENTER_X
        self.settings_button.center_y = CENTER_Y - 125

        self.quit_button = arcade.Sprite(
            "Sprites/QuitButton.png")
        self.quit_button.center_x = CENTER_X
        self.quit_button.center_y = CENTER_Y - 175

        self.button_list.append(self.play_button)
        self.button_list.append(self.settings_button)
        self.button_list.append(self.quit_button)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.button_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.collides_with_point((x, y)):
            game_view = GameView()
            self.window.show_view(game_view)
        elif self.settings_button.collides_with_point((x, y)):
            settings_view = SettingsView()
            self.window.show_view(settings_view)
        elif self.quit_button.collides_with_point((x, y)):
            arcade.exit()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.play_sound(sound)
        self.logic = GameLogic()
        self.renderer = Renderer(self.logic)
        self.logic.setup()

    def on_draw(self):
        self.clear()
        self.renderer.draw()

        if self.logic.game_state == GameState.gameover:
            self.window.show_view(DeathView(score=self.logic.score))

        if self.logic.game_state == GameState.win:
            self.window.show_view(WinView(self.logic.score))

    def on_update(self, delta_time):
        if self.logic.game_state == GameState.playing:
            self.logic.update()

    def on_key_press(self, key, modifers):
        self.logic.on_key_press(key, modifers)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.logic.game_state == GameState.gameover:
            self.window.show_view(DeathView(score=self.logic.score))


class DeathView(arcade.View):
    def __init__(self, score: int):
        super().__init__()
        self.store = score  # количество монет
        arcade.play_sound(win_sound)

        save_result_to_file(self.store, "lose")

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)
        arcade.draw_text("GAME OVER", CENTER_X, CENTER_Y + 50, arcade.color.RED, 48, anchor_x="center")

        arcade.draw_text(f"Store: {self.store}", CENTER_X, CENTER_Y - 50, arcade.color.WHITE, 24, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # возврат в меню по клику в любом месте
        self.window.show_view(MainMenuView())


class WinView(arcade.View):
    def __init__(self, score: int):
        super().__init__()
        arcade.play_sound(win_sound)
        self.store = score

        save_result_to_file(self.store, "win")

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        arcade.draw_text("WIN!!!", CENTER_X, CENTER_Y + 50, arcade.color.GREEN, 48, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(MainMenuView())


ItHard = 0


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        global ItHard
        self.mode = ItHard

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        arcade.draw_text("Настройки сложности", 400, 500, arcade.color.WHITE, 30, anchor_x="center")

        normal_color = arcade.color.GREEN if self.mode == 0 else arcade.color.GRAY
        arcade.draw_text("[ОБЫЧНЫЙ]", 300, 300, normal_color, 30, anchor_x="center")

        hard_color = arcade.color.RED if self.mode == 1 else arcade.color.GRAY
        arcade.draw_text("[СЛОЖНЫЙ]", 600, 300, hard_color, 30, anchor_x="center")

        arcade.draw_text("<Назад в меню>", 400, 150, arcade.color.YELLOW, 24, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        global ItHard

        if 250 <= x <= 350 and 285 <= y <= 315:
            ItHard = 0
            self.mode = 0

        elif 450 <= x <= 550 and 285 <= y <= 315:
            ItHard = 1
            self.mode = 1

        elif 350 <= x <= 450 and 140 <= y <= 160:
            self.window.show_view(MainMenuView())


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Home")
    menu_view = MainMenuView()
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()
