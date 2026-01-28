import arcade

# константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()

        # создаем список для фона
        self.background_list = arcade.SpriteList()

        # создаем спрайт фона
        self.background = arcade.Sprite("Sprites/MenuBackground.png")
        self.background.center_x = CENTER_X
        self.background.center_y = CENTER_Y
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
        self.background_list.append(self.background)

        # создаем список спрайтов для кнопок
        self.button_list = arcade.SpriteList()

        # создаем кнопки
        self.play_button = arcade.Sprite("Sprites/PlayButton.png")
        self.play_button.center_x = CENTER_X
        self.play_button.center_y = CENTER_Y - 75

        self.settings_button = arcade.Sprite("Sprites/SettingButton.png")
        self.settings_button.center_x = CENTER_X
        self.settings_button.center_y = CENTER_Y - 125

        self.quit_button = arcade.Sprite("Sprites/QuitButton.png")
        self.quit_button.center_x = CENTER_X
        self.quit_button.center_y = CENTER_Y - 175

        # добавляем кнопки в список
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

        # список для кнопки
        self.button_list = arcade.SpriteList()

        # кнопка для перехода к экрану смерти
        self.die_button = arcade.Sprite("Sprites/PlayButton.png")
        self.die_button.center_x = CENTER_X
        self.die_button.center_y = CENTER_Y - 50

        self.button_list.append(self.die_button)

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        # рисуем текст
        arcade.draw_text(
            "Здесь будет основная игра",
            CENTER_X,
            CENTER_Y + 100,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        # рисуем кнопку
        self.button_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.die_button.collides_with_point((x, y)):
            death_view = DeathView()
            self.window.show_view(death_view)


class DeathView(arcade.View):
    def __init__(self):
        super().__init__()
        self.store = 0  # количество монет

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        # рисуем текст игры
        arcade.draw_text(
            "GAME OVER",
            CENTER_X,
            CENTER_Y + 50,
            arcade.color.RED,
            48,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Store: {self.store}",
            CENTER_X,
            CENTER_Y - 50,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # возврат в меню по клику в любом месте
        self.window.show_view(MainMenuView())


class SettingsView(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # текст окна настроек
        arcade.draw_text(
            "Окно настроек",
            CENTER_X,
            CENTER_Y,
            arcade.color.WHITE,
            36,
            anchor_x="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # возврат в меню по клику в любом месте
        self.window.show_view(MainMenuView())


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "TestMenu")

    # создаем и показываем главное меню
    menu_view = MainMenuView()
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()