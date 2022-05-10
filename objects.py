import os
import sys
import json
from random import randint

import pygame
import pygame_menu
from pygame.math import Vector2

from SETTINGS import (CELL_SIZE, CELL_AMOUNT, GREEN, GRASS_COLOR, TEXT_COLOR, PLAYER_SCORE_JSON_PATH)


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.color = (183, 111, 122)
        self.direction = Vector2(0, 0)

        # Add images pf all snake (body, head, tail) positions
        self.head_right = pygame.image.load("./static/images/head_right.png").convert_alpha()
        self.head_up = pygame.image.load("./static/images/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("./static/images/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("./static/images/head_left.png").convert_alpha()

        self.head_direction_images = {
            "x": {
                1: self.head_right,
                -1: self.head_left,
            },
            "y": {
                1: self.head_down,
                -1: self.head_up
            }
        }

        self.tail_up = pygame.image.load("./static/images/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("./static/images/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("./static/images/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("./static/images/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load("./static/images/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("./static/images/body_horizontal.png").convert_alpha()

        self.body_tr = pygame.image.load("./static/images/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("./static/images/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("./static/images/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("./static/images/body_bl.png").convert_alpha()

        # Head default direction
        self.head_image = self.head_right

        self.crunch_sound = pygame.mixer.Sound("./static/sounds/crunch.wav")

    def draw(self):
        self.__update_head_image()
        self.__update_tail_image()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            
            if index == 0:
                # draw head direction
                self.canvas.blit(self.head_image, block_rect)
                
            elif index == len(self.body) - 1:
                #draw tail direction
                self.canvas.blit(self.tail_image, block_rect)
            
            else:
                previous_block_pos = self.body[index + 1] - block
                next_block_pos = self.body[index - 1] - block
                if previous_block_pos.x == next_block_pos.x:
                    self.canvas.blit(self.body_vertical, block_rect)
                elif previous_block_pos.y == next_block_pos.y:
                    self.canvas.blit(self.body_horizontal, block_rect)
                else:
                    #draw a curved body
                    if (previous_block_pos.x == -1 and next_block_pos.y == -1) or (previous_block_pos.y == -1 and next_block_pos.x == -1)\
                        or ((previous_block_pos.x == (CELL_AMOUNT-1)) and (next_block_pos.y == -1) and (block.x == 0))\
                            or ((previous_block_pos.y == (CELL_AMOUNT-1)) and (next_block_pos.x == -1) and (block.y == 0))\
                                or ((previous_block_pos.x == -1) and (next_block_pos.y == (CELL_AMOUNT-1)) and (block.y == 0))\
                                    or ((previous_block_pos.y == -1) and (next_block_pos.x == (CELL_AMOUNT-1)) and (block.x == 0)):
                        self.canvas.blit(self.body_tl, block_rect)

                    elif (previous_block_pos.x == 1 and next_block_pos.y == -1) or (previous_block_pos.y == -1 and next_block_pos.x == 1)\
                        or ((previous_block_pos.x == -(CELL_AMOUNT-1) and next_block_pos.y == -1) and (block.x == (CELL_AMOUNT-1)))\
                            or ((previous_block_pos.y == (CELL_AMOUNT-1) and next_block_pos.x == 1) and (block.y == 0))\
                                or ((previous_block_pos.y == -1 and next_block_pos.x == -(CELL_AMOUNT-1)) and (block.x == (CELL_AMOUNT-1)))\
                                    or ((previous_block_pos.x == 1 and next_block_pos.y == (CELL_AMOUNT-1)) and (block.y == 0)):
                        self.canvas.blit(self.body_tr, block_rect)

                    elif (previous_block_pos.x == -1 and next_block_pos.y == 1) or (previous_block_pos.y == 1 and next_block_pos.x == -1)\
                        or ((previous_block_pos.y == -(CELL_AMOUNT-1) and next_block_pos.x == -1) and (block.y == (CELL_AMOUNT-1)))\
                            or ((previous_block_pos.x == (CELL_AMOUNT-1) and next_block_pos.y == 1) and (block.x == 0))\
                                or ((previous_block_pos.x == -1 and next_block_pos.y == -(CELL_AMOUNT-1)) and (block.y == (CELL_AMOUNT-1)))\
                                    or ((previous_block_pos.y == 1 and next_block_pos.x == (CELL_AMOUNT-1)) and (block.x == 0)):
                        self.canvas.blit(self.body_bl, block_rect)

                    elif (previous_block_pos.x == 1 and next_block_pos.y == 1) or (previous_block_pos.y == 1 and next_block_pos.x == 1)\
                        or ((previous_block_pos.y == -(CELL_AMOUNT-1) and next_block_pos.x == 1) and (block.y == (CELL_AMOUNT-1)))\
                            or ((previous_block_pos.x == -(CELL_AMOUNT-1) and next_block_pos.y == 1) and (block.x == (CELL_AMOUNT-1)))\
                                or ((previous_block_pos.x == 1 and next_block_pos.y == -(CELL_AMOUNT-1)) and (block.y == (CELL_AMOUNT-1)))\
                                    or ((previous_block_pos.y == 1 and next_block_pos.x == -(CELL_AMOUNT-1)) and (block.x == (CELL_AMOUNT-1))):
                        self.canvas.blit(self.body_br, block_rect)
    
    def __update_head_image(self):
        if self.direction.x:
            self.head_image = self.head_direction_images["x"][self.direction.x]
        elif self.direction.y:
            self.head_image = self.head_direction_images["y"][self.direction.y]
    
    def __update_tail_image(self):
        tail_direction = self.body[-2] - self.body[-1]
        if tail_direction == Vector2(1, 0): self.tail_image = self.tail_left
        elif tail_direction == Vector2(-1, 0): self.tail_image = self.tail_right
        elif tail_direction == Vector2(0, 1): self.tail_image = self.tail_up
        elif tail_direction == Vector2(0, -1): self.tail_image = self.tail_down

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

        self.check_border_collision()
    
    def check_border_collision(self):
        if self.body[0].x < 0:
            self.body[0].x = CELL_AMOUNT-1
        elif self.body[0].x > CELL_AMOUNT-1:
            self.body[0].x = 0
        elif self.body[0].y < 0:
            self.body[0].y = CELL_AMOUNT-1
        elif self.body[0].y > CELL_AMOUNT-1:
            self.body[0].y = 0
    
    def increase_length(self):
        self.body.insert(0, self.body[0] + self.direction)
    
    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.head_image = self.head_right

class Fruit:
    def __init__(self, canvas, fruit_image):
        self.canvas = canvas
        self.fruit_image = fruit_image

        self.randomize()
    
    def draw(self):
        fruit_rect = pygame.Rect(int(self.pos.x*CELL_SIZE), int(self.pos.y*CELL_SIZE), CELL_SIZE, CELL_SIZE)
        self.canvas.blit(self.fruit_image, fruit_rect)
 
    def randomize(self):
        #initialize the fruit position on the canvas
        self.x = randint(0, CELL_AMOUNT - 1)
        self.y = randint(0, CELL_AMOUNT - 1)
        self.pos = Vector2(self.x, self.y)

class Wall:
    def __init__(self, canvas):
        self.canvas = canvas
        self.wall_image = pygame.image.load("./static/images/wall.png").convert_alpha()
        self.walls_amount = 5
        self.walls = []

        self.randomize()
    
    def draw(self):
        for wall in self.walls:
            for block in wall:
                x_pos = int(block.x * CELL_SIZE)
                y_pos = int(block.y * CELL_SIZE)
                wall_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
                self.canvas.blit(self.wall_image, wall_rect)

    def reset(self):
            self.walls = []
            self.randomize()

    def randomize(self):
        for wall_block in range(self.walls_amount):
            wall = []
            #initialize the wall position on the canvas
            x = randint(0, CELL_AMOUNT - 1)
            y = randint(0, CELL_AMOUNT - 1)
            pos = Vector2(x, y)

            wall_length = randint(3, 5)

            # fill array with vectors
            for i in range(wall_length):
                wall.append(pos)

            # make a random shaped wall
            for i in range(1, wall_length):
                increase_x = randint(0, 1)
                if increase_x:
                    wall[i] = wall[i-1] + Vector2(1, 0)
                else:
                    wall[i] = wall[i-1] + Vector2(0, 1)

            self.walls.append(wall)

            need_to_reset = False
            # check the wall surroundings
            for index_wall in range(len(self.walls)-1):
                for block in self.walls[index_wall]:
                    for i in range(index_wall+1, len(self.walls)):
                        for j in range(len(self.walls[i])):
                            if (block == self.walls[i][j]) or (block + Vector2(1, 1) == self.walls[i][j]) or (block + Vector2(-1, 1) == self.walls[i][j])\
                                or (block + Vector2(1, -1) == self.walls[i][j]) or (block + Vector2(-1, -1) == self.walls[i][j]):
                                need_to_reset = True

            if need_to_reset:
                need_to_reset = False
                self.reset()

class Game: 
    @staticmethod
    def get_sorted_list_of_players_records() -> list:
        if os.stat(PLAYER_SCORE_JSON_PATH).st_size:
            with open(PLAYER_SCORE_JSON_PATH, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)
                players_records = sorted(data, key=lambda x: x[list(x.keys())[0]], reverse=True)
        else:
            players_records = []
        
        return players_records

    def __init__(self, canvas, clock):
        self.canvas = canvas
        self.clock = clock

        self.apple_image = pygame.image.load("./static/images/apple.png").convert_alpha()

        self.score = 0
        self.snake = Snake(self.canvas)
        self.fruit = Fruit(self.canvas, self.apple_image)
        self.wall = Wall(self.canvas)

        self.poetsen_one_font = pygame.font.Font("./static/fonts/PoetsenOne-Regular.ttf", 25)
        self.tektur_font = pygame.font.Font("./static/fonts/Tektur-Regular.ttf", 30)
        self.game_sound = pygame.mixer.Sound("./static/sounds/game_sound.mp3")
        self.menu_sound = pygame.mixer.Sound("./static/sounds/menu_sound.mp3")
        self.game_sound.set_volume(0.4)

    def update(self):
        if self.snake.direction != pygame.Vector2(0, 0):
            self.snake.move()
        self.check_fruit_collision()
        self.check_death_collision() 
        self.check_wall_collision()
              

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw()
        self.snake.draw()
        self.draw_score()
        self.wall.draw()

    def check_fruit_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.increase_length()
            self.snake.play_crunch_sound()
            self.score += 1
        
        # Prevent appearing a fruit under the snake body
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
        
        # Prevent appearing a fruit under the score table
        if self.fruit.pos == Vector2(17, 18) or self.fruit.pos == Vector2(18, 18):
            self.fruit.randomize()
        
        # Prevent appearing a fruit under the wall
        for wall in self.wall.walls:
                for block in wall:
                    if self.fruit.pos == block:
                        self.fruit.randomize()

    def check_wall_collision(self):
        # Prevent appearing a wall under the score table
        for wall in self.wall.walls:
                for block in wall:
                    if block == Vector2(17, 18) or block == Vector2(18, 18):
                        self.wall.reset()
        
        # Prevent appearing a wall in the snake
        for wall in self.wall.walls:
                for block in wall:
                    for snake_block in self.snake.body:
                        if block == snake_block:
                            self.wall.reset()
     
    def check_death_collision(self):
        #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]: 
                self.game_over()
        
        #check if snake hits the wall
        for wall in self.wall.walls:
                for block in wall:
                    if self.snake.body[0] == block:
                        self.game_over()
    
    def game_over(self):
        self.__write_score_to_json()

        end_loop = True

        while end_loop:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        end_loop = False
                    if event.key == pygame.K_ESCAPE:
                        self.game_sound.stop()
                        self.menu_sound.play()
                        self.go_to_menu = True
                        end_loop = False
                    
            self.draw_death_score()
            pygame.display.update()
            self.clock.tick(15)
                

        self.snake.reset()
        self.wall.reset()
        self.score = 0

    
    def draw_grass(self):

        for row in range(CELL_AMOUNT):
            for cell in range(CELL_AMOUNT):
                if cell % 2 == 0 and row % 2 == 0:
                    grass_rect = pygame.Rect(cell*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.canvas, GRASS_COLOR, grass_rect)
                elif cell % 2 == 1 and row % 2 == 1:
                    grass_rect = pygame.Rect(cell*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.canvas, GRASS_COLOR, grass_rect)
    
    def draw_score(self):
        score_text = f"{self.score}"
        score_surface = self.poetsen_one_font.render(score_text, True, TEXT_COLOR)
        score_x = int(CELL_SIZE*CELL_AMOUNT - 60)
        score_y = int(CELL_SIZE*CELL_AMOUNT - 60)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = self.apple_image.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 7, apple_rect.height)

        pygame.draw.rect(self.canvas, GRASS_COLOR, bg_rect)
        pygame.draw.rect(self.canvas, TEXT_COLOR, bg_rect, 2)
        self.canvas.blit(score_surface, score_rect)
        self.canvas.blit(self.apple_image, apple_rect)
    
    def draw_death_score(self):
        message_text = "Ваш счёт:"
        message_surface = self.tektur_font.render(message_text, True, TEXT_COLOR)
        message_x = int(CELL_SIZE*CELL_AMOUNT - 450)
        message_y = int(CELL_SIZE*CELL_AMOUNT - 400)
        message_rect = message_surface.get_rect(center = (message_x, message_y))

        score_text = f"{self.score}"
        score_surface = self.poetsen_one_font.render(score_text, True, TEXT_COLOR)
        score_x = int(CELL_SIZE*CELL_AMOUNT - 430)
        score_y = int(CELL_SIZE*CELL_AMOUNT - 350)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = self.apple_image.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(message_rect.left - 20, message_rect.top, apple_rect.width + message_rect.width + score_rect.width, apple_rect.height + message_rect.height + 20)

        pygame.draw.rect(self.canvas, GRASS_COLOR, bg_rect)
        pygame.draw.rect(self.canvas, TEXT_COLOR, bg_rect, 2)
        self.canvas.blit(message_surface, message_rect)
        self.canvas.blit(score_surface, score_rect)
        self.canvas.blit(self.apple_image, apple_rect)

        self.draw_back_to_menu()
    
    def draw_back_to_menu(self):
        message_text = "Назад в Меню 'Esc'"
        message_surface = self.tektur_font.render(message_text, True, TEXT_COLOR)
        message_x = int(CELL_SIZE*CELL_AMOUNT - 160)
        message_y = int(CELL_SIZE*CELL_AMOUNT - 770)
        message_rect = message_surface.get_rect(center = (message_x, message_y))
        self.canvas.blit(message_surface, message_rect)
    
    def __write_score_to_json(self):
        if os.stat(PLAYER_SCORE_JSON_PATH).st_size:
            with open(PLAYER_SCORE_JSON_PATH, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)
                for num, dict in enumerate(data):
                    if next(iter(dict)) == self.player_name:
                        if (int(dict[next(iter(dict))]) < self.score):
                            data.pop(num)
                            data.append({self.player_name: self.score})
                        break
                else:
                    data.append({self.player_name: self.score})
        else:
            data = []
            data.append({self.player_name: self.score})
            
        with open(PLAYER_SCORE_JSON_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    def paused(self):
        pause_text = "Нажмите 'Пробел', чтобы продолжить"
        pause_surface = self.tektur_font.render(pause_text, True, TEXT_COLOR)
        pause_x = int(CELL_SIZE*CELL_AMOUNT - 400)
        pause_y = int(CELL_SIZE*CELL_AMOUNT - 300)
        pause_rect = pause_surface.get_rect(center = (pause_x, pause_y))
        bg_rect = pygame.Rect(pause_rect.left - 20, pause_rect.top, pause_rect.width + 40, pause_rect.height + 20)

        pygame.draw.rect(self.canvas, GRASS_COLOR, bg_rect)
        pygame.draw.rect(self.canvas, TEXT_COLOR, bg_rect, 2)
        self.canvas.blit(pause_surface, pause_rect)
    
        pause = True

        while pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                        pause = False
                    
            pygame.display.update()
            self.clock.tick(15)

    def game_loop(self, player_name: str, difficulty_settings: dict):
        self
        self.player_name = player_name
        self.go_to_menu = False
        CANVAS_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(CANVAS_UPDATE, difficulty_settings["snake_update_time"])
        self.menu_sound.stop()
        self.game_sound.play()
        while not self.go_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == CANVAS_UPDATE:
                    self.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                        self.paused()
                    if event.key == pygame.K_UP and self.snake.direction.y != 1:
                        self.snake.direction = pygame.Vector2(0, -1)
                    if event.key == pygame.K_DOWN and self.snake.direction.y != -1:
                        self.snake.direction = pygame.Vector2(0, 1)
                    if event.key == pygame.K_RIGHT and self.snake.direction.x != -1:
                        self.snake.direction = pygame.Vector2(1, 0)
                    if event.key == pygame.K_LEFT and self.snake.direction.x != 1 and self.snake.direction != pygame.Vector2(0, 0):
                        self.snake.direction = pygame.Vector2(-1, 0)

            self.canvas.fill(GREEN)
            self.draw_elements()

            pygame.display.update()
            self.clock.tick(60)

class GameMenu:
    def __init__(self, canvas, game: Game):
        self.width = 600
        self.height = 400
        self.canvas = canvas

        self.player_name = "Игрок1"
        self.difficulty = 1
        self.difficulty_settings = {"snake_update_time": 150}

        self.menu_sound = pygame.mixer.Sound("./static/sounds/menu_sound.mp3")
        self.menu_sound.set_volume(0.7)

        self.game = game

    def call(self):
        self.menu = pygame_menu.Menu('Добро пожаловать!', self.width, self.height,
                        theme=pygame_menu.themes.THEME_BLUE)

        self.menu.add.text_input('Имя персонажа: ', default=self.player_name, maxchar=12, onchange=self.set_player_name)
        self.menu.add.selector('Уровень сложности: ', [('Легко', 1), ('Сложно', 2)], onchange=self.set_difficulty)
        self.menu.add.button('Играть', self.start_the_game)
        self.menu.add.button('Рекорды', self.call_record_menu)
        self.menu.add.button('Выход', pygame_menu.events.EXIT)

        self.menu_sound.play()

        self.menu.mainloop(self.canvas)
    
    def set_player_name(self, player_name: str):
        self.player_name = player_name

    def set_difficulty(self, value, difficulty: int):
        if difficulty == 1:
            self.difficulty_settings["snake_update_time"] = 150
        elif difficulty == 2:
            self.difficulty_settings["snake_update_time"] = 90

    def start_the_game(self):
        self.menu_sound.stop()
        self.game.game_loop(self.player_name, self.difficulty_settings)

    def call_record_menu(self):
        players_records: list = Game.get_sorted_list_of_players_records()[:5]
        records_title = ""

        if len(players_records) > 0:
            for num, record in enumerate(players_records):
                for player_name, score in record.items():
                    records_title += f"{num+1}.) {player_name} - {score}\n"
            
            record_menu = pygame_menu.Menu('Рекорды:', self.width, self.height,
                        theme=pygame_menu.themes.THEME_BLUE)

            record_menu.add.label(title=records_title)
            record_menu.add.button("Назад", record_menu.disable)

            record_menu.mainloop(self.canvas)
