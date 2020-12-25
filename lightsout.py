from sense_hat import SenseHat
from random import randrange

sense = SenseHat()

class Game():
    ON = [255, 0, 0] # red
    OFF = [0, 0, 0]  # blank
    CURSOR_ON = [192, 64, 64] # purple
    CURSOR_OFF = [0, 64, 64]  # aqua

    def __init__(self, height=8, width=8):
        self.width = width
        self.height = height
        self.board = []
        for _ in range(self.height):
            self.board.append([self.OFF] * self.width)
        for _ in range(6):
            y = randrange(0, self.height)
            x = randrange(0, self.width)
            self.flips(y, x)
        self.x = 0
        self.y = 0 
        self.show()
        self.play()

    def flip(self, y, x):
        if 0 <= y < self.height and 0 <= x < self.width:
            self.board[y][x] = self.OFF if self.board[y][x] == self.ON else self.ON

    def flips(self, y, x):
        self.flip(y, x-1)
        self.flip(y, x)
        self.flip(y, x+1)
        self.flip(y-1, x)
        self.flip(y+1, x)

    def is_won(self):
        return all(c == self.OFF for row in self.board for c in row)

    def show(self):
        pixels = [c for row in self.board for c in row]
        pixels[self.y * self.height + self.x] = (
            self.CURSOR_ON 
            if self.board[self.y][self.x] == self.ON 
            else self.CURSOR_OFF)
        sense.set_pixels(pixels)
        
        print(self.board)
        print(sense.get_pixels())

    def play(self):
        while True:
            [_, dir, action] = sense.stick.wait_for_event()
            x = self.x
            y = self.y
            if action == "pressed":
                if dir == "left":
                    x += -1
                elif dir == "right":
                    x += 1
                elif dir == "up":
                    y += -1
                elif dir == "down":
                    y += 1
                else:
                    self.flips(y, x)

            if 0 <= y < self.height and 0 <= x < self.width:
                self.x = x
                self.y = y
                self.show()
                if self.is_won():
                    break
        sense.clear()
        sense.show_message("Yay!")
        sense.clear()

Game()