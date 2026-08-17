import pygame
from turtle import Turtle, Screen
import tkinter as tk


def music_player(sound):
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(-1)



class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

    def go_up(self):
        self.goto(self.xcor(), self.ycor() + 25)

    def go_down(self):
        self.goto(self.xcor(), self.ycor() - 25)

    def move_right(self):
        self.setheading(0)
        self.forward(30)

    def move_left(self):
        self.setheading(180)
        self.forward(30)

    def image(self, path):
        screen = Screen()
        screen.addshape(path)
        self.shape(path)




class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.x = 0
        self.y = 0
        self.move_speed = 10


    def move(self):
        self.x = self.xcor() + self.x_move
        self.y  = self.ycor() + self.y_move
        self.goto(self.x, self.y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, 0)
        self.bounce_x()

    def image(self, path):
        screen = Screen()
        screen.addshape(path)
        self.shape(path)




class Win:
    def __init__(self, title="GameGuy", mode="mainloop"):
        self.screen = Screen()
        self.screen.title(title)

        root = self.screen._root
        img = tk.PhotoImage(file="C:/Users/Arnav/Desktop/Coding/Files/Professional(Day 82 to 100)/Bomberman/images/bomberman.gif")
        root.iconphoto(False, img)


        if mode == "mainloop":
            self.screen.mainloop()
        else:
            self.screen.exitonclick()



class Scoreboard(Turtle):
    def __init__(self, position:tuple):
        super().__init__()
        self.goto(position)
        self.hideturtle()

        self.font = ("Arial", 25, "bold")

        self.lives = 3
        self.score = 0
        self.time = None

    def update_score(self, num):
        self.score += num

    def update_lives(self, to_do="down"):
        if to_do == "up":
            self.lives += 1
        else:
            self.lives -= 1


