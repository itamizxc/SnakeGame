from tkinter import *
import random
from pymongo import MongoClient

GRID_MULTIPLIER = int(input("Input grid multiplier(min=5, max=25): "))
SPACE_SIZE = 50
GAME_WIDTH = SPACE_SIZE * GRID_MULTIPLIER
GAME_HEIGHT = SPACE_SIZE * GRID_MULTIPLIER
SPEED = 300
BODY_PARTS = 3
SNAKE_COLOR = "LIME GREEN"
SNAKE_HEAD = "#cceb34"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#0c5404"

client = MongoClient("localhost", 27017)
db = client.SnakeUser

Users = db.Users



class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.direction = "down"

        self.initialize_snake()

    def initialize_snake(self):
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

    def move(self):
        x, y = self.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.squares.insert(0, square)

        return x, y

    def remove_tail(self):
        self.canvas.delete(self.squares[-1])
        del self.squares[-1]
        del self.coordinates[-1]

    def change_direction(self, new_direction):
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction


class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.coordinates = []
        self.initialize_food()

    def initialize_food(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

    def draw_food(self):
        x, y = self.coordinates
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


class Game:
    def __init__(self, window, canvas, User):
        self.window = window
        self.canvas = canvas
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.score = 0
        self.label = Label(text="Score:{}".format(self.score), font=("Arial", 30, "bold"))
        self.label.pack()
        self.window.bind('<Left>', lambda event: self.snake.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.snake.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.snake.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.snake.change_direction('down'))
        self.User = User

    def start(self):
        self.food.draw_food()
        self.next_turn()

    def next_turn(self):
        x, y = self.snake.move()

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text="Score:{}".format(self.score))
            self.canvas.delete("food")
            self.food = Food(self.canvas)
            self.food.draw_food()
        else:
            self.snake.remove_tail()

        if self.check_collision():
            self.game_over()
            self.User.update_highscore(self.score)
            Users.insert_one({"name": self.User.name, "highscore": self.User.highscore})
        else:
            self.window.after(SPEED, self.next_turn)

    def check_collision(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= GAME_WIDTH:
            return True
        elif y < 0 or y >= GAME_HEIGHT:
            return True

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=('Arial', 80), text="GAME OVER", fill="#000000")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 160, font=('Arial', 40),
                                text="Highcore:{}".format(self.score), fill="#000000")

class User:
    def __init__(self):
        self.name = "User1"
        self.highscore = 0

    def update_name(self):
        self.name = input("Enter your username: ")

    def update_highscore(self, score):
        if score > self.highscore:
            self.highscore = score


user = User()
user.update_name()

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

game = Game(window, canvas, user)
game.start()

window.mainloop()
