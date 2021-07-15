class TicTacToe:

    def __init__(self):
        self.board = []
        self.status = ''

    def board_display(self):
        print("---------")
        print("|", self.board[0] + " " + self.board[1] + " " + self.board[2], "|")
        print("|", self.board[3] + " " + self.board[4] + " " + self.board[5], "|")
        print("|", self.board[6] + " " + self.board[7] + " " + self.board[8], "|")
        print("---------")

    def get_status(self):
        return self.status

    def set_status(self, winner):
        self.status = winner

    def main(self):
        self.board = list("_________".replace("_", " "))
        self.status = "None"
        self.board_display()
        while True:
            if self.get_status() != "X wins" or self.get_status() != "O wins" or self.get_status() != "Draw":
                self.playGame("X")
                self.playGame("O")
                self.countBoard()
                continue
            else:
                break

    def playGame(self, piece):
        enter = input("Enter the coordinates: ").replace(" ", "")
        if enter[0] not in "1234567890" or enter[1] not in "1234567890":
            print("You should enter numbers!")
        elif enter[0] not in "123" or enter[1] not in "123" or len(enter) > 2:
            print("Coordinates should be from 1 to 3!")
        else:
            index = ((int(enter[0]) - 1) * 3) + ((int(enter[1]) + 2) - 3)
            if self.board[index] != " ":
                print("This cell is occupied! Choose another one!")
            else:
                self.board[index] = piece
                self.board_display()
                self.checkRow()
                self.checkCol()
                self.checkDiagonal()

    def checkRow(self):
        for i in range(0, 7, 3):  # horizontal
            if self.board[i] == self.board[i + 1] and self.board[i] == self.board[i + 2]:
                if self.board[i] == 'X':
                    self.set_status("X wins")
                    print(self.get_status())
                    exit()
                elif self.board[i] == 'O':
                    self.set_status("O wins")
                    print(self.get_status())
                    exit()

    def checkCol(self):
        for i in range(0, 3):
            if self.board[i] == self.board[i + 3] and self.board[i] == self.board[i + 6]:
                if self.board[i] == 'X':
                    self.set_status("X wins")
                    print(self.get_status())
                    exit()
                elif self.board[i] == 'O':
                    self.set_status("O wins")
                    print(self.get_status())
                    exit()

    def checkDiagonal(self):
        if self.board[0] == self.board[4] and self.board[0] == self.board[8]:
            if self.board[0] == 'X':
                self.set_status("X wins")
                print(self.get_status())
                exit()
            elif self.board[0] == 'O':
                self.set_status("O wins")
                print(self.get_status())
                exit()
        elif self.board[2] == self.board[4] and self.board[2] == self.board[6]:
            if self.board[2] == 'X':
                self.set_status("X wins")
                print(self.get_status())
                exit()
            elif self.board[2] == 'O':
                self.set_status("O wins")
                print(self.get_status())
                exit()

    def countBoard(self):
        counter_x = 0
        counter_o = 0
        counter_empty = 0
        for el in range(0, 9):
            if self.board[el] == 'X':
                counter_x += 1
            elif self.board[el] == 'O':
                counter_o += 1
            else:
                counter_empty += 1

        return self.checkDraw(counter_x, counter_o)  # taking out counter_empty

    def checkDraw(self, counter_x, counter_o):  # taking out counter_empty
        if abs(counter_o - counter_x) < 2 and counter_x + counter_o >= 9:
            self.set_status("Draw")
            print(self.get_status())
            exit()


board = TicTacToe()
board.main()
