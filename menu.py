import pygame_menu


class GameMenu:
    def __init__(self, canvas):
        self.width = 300
        self.height = 100
        self.canvas = canvas

        self.menu = pygame_menu.Menu('Добро пожаловать!', self.width, self.heigh,
                        theme=pygame_menu.themes.THEME_BLUE)

        self.menu.add.text_input('Имя персонажа: ', default='Игрок1', maxchar=12, onchange=self.set_player_name)
        self.menu.add.selector('Уровень сложности: ', [('Легко', 1), ('Сложно', 2)], onchange=self.set_difficulty)
        self.menu.add.button('Играть', self.start_the_game)
        self.menu.add.button('Рекорды', self.call_record_menu)
        self.menu.add.button('Выход', pygame_menu.events.EXIT)

        self.menu.mainloop(self.canvas)