import arcade
from game_logic import GameLogic, GameState
from rendering import Renderer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_list = arcade.SpriteList()

        self.background = arcade.Sprite("Sprites/MenuBackground.png")
        self.background.center_x = CENTER_X
        self.background.center_y = CENTER_Y
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
        self.background_list.append(self.background)

        self.button_list = arcade.SpriteList()

        self.play_button = arcade.Sprite("Sprites/PlayButton.png")
        self.play_button.center_x = CENTER_X
        self.play_button.center_y = CENTER_Y - 75

        self.settings_button = arcade.Sprite("Sprites/SettingButton.png")
        self.settings_button.center_x = CENTER_X
        self.settings_button.center_y = CENTER_Y - 125

        self.quit_button = arcade.Sprite("Sprites/QuitButton.png")
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

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        arcade.draw_text("WIN!!!", CENTER_X, CENTER_Y + 50, arcade.color.GREEN, 48, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(MainMenuView())


class SettingsView(arcade.View):
    # TODO: Надо сделать экран настроек :)
    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # текст окна настроек
        arcade.draw_text("Окно настроек", CENTER_X, CENTER_Y, arcade.color.WHITE, 36, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # возврат в меню по клику в любом месте
        self.window.show_view(MainMenuView())


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Home")
    menu_view = MainMenuView()
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()
