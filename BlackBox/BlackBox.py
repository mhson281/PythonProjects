from copy import deepcopy

class BlackBoxGame:
    """Represent a Black Box object"""

    def __init__(self, atoms):
        """Initialize the 10x10 board and score.  Accept atoms as a parameter and label atoms on board."""
        self._board = [['.' for _ in range(10)] for _ in range(10)]
        for atom in atoms:
            self._board[atom[0]][atom[1]] = 'a'
        self._score = 25
        self._atoms = len(atoms)
        self._disp = deepcopy(self._board)
        # a: atom
        # h: hit atom
        # r: wrong atom guess

        # x: already chosen enter/exit

    def is_border(self, row, col):
        """Set the border for the board, used by guessing player for shooting rays"""
        corners = [(0, 0), (0, 9), (9, 0), (9, 9)]
        return (row == 0 or row == 9 or col == 0 or col == 9) and ((row, col) not in corners)

    def is_atom(self, row, col):
        """Return position of the atom"""
        return self._board[row][col] in 'ah'

    def auto_increase(self, row, col):
        """Increase row and column to direct ray to exit and get exit square"""
        if row == 0:
            return 1, 0

        if row == 9:
            return -1, 0

        if col == 0:
            return 0, 1

        if col == 9:
            return 0, -1

    def check_reflection(self, row, col):
        """Check the next column row and column for an atom, return True if it exists, reflection
        condition is met """
        corners_inc = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for (i, j) in corners_inc:
            try:
                if self.is_atom(row + i, col + j):
                    return True
            except:
                pass

        return False

    def check_deflection(self, row, col, i, j):
        """Check the four side corners of the atoms to see if the ray is hitting it, return the exit ray as deflected
        90 degree """
        c1 = self.is_atom(row + 1, col + 1)
        c2 = self.is_atom(row - 1, col + 1)
        c3 = self.is_atom(row - 1, col - 1)
        c4 = self.is_atom(row + 1, col - 1)

        if (c1 and c2) or (c2 and c3) or (c3 and c4) or (
                c4 and c1):  # if top right, bottom right, top left, or bottom left squares are atoms
            return -i, -j

        if c1 or c3:  # if top left and bottom right corner squares are atoms
            return -j, -i

        if c2 or c4:  # if top right and bottom left corner squares are atoms
            return j, i

        return i, j

    def modify_score(self, row, col, penalty):
        """If the ray hits an atom, change the name of the atom to another letter to record a hit, else, subtract 5
        points from the total score """
        if penalty == 5:
            if self._board[row][col] in 'rh' or self.is_border(row, col):
                return

            self._board[row][col] = 'r'
        else:  # 'x' marks a square that has already been chosen
            if self._board[row][col] == 'x':
                return
            self._board[row][col] = 'x'

        self._score -= penalty

    def shoot_ray(self, row, col):
        """Only allow shooting rays from border squares. Check for reflection and deflection, redirect ray as needed"""
        if not self.is_border(row, col):  # return false if square is not in border squares
            return False

        self.modify_score(row, col, 1)
        if self.check_reflection(row, col):  # return tuples of exit border square
            return row, col
        i, j = self.auto_increase(row, col)
        row += i
        col += j

        while not self.is_border(row, col):
            self._disp[row][col] = ' '
            if self.is_atom(row, col):  # return none if no exit border square exists
                return None

            i, j = self.check_deflection(row, col, i, j)
            row += i
            col += j

        self.modify_score(row, col, 1)
        return row, col

    def guess_atom(self, row, col):
        """Take guessed input as row and column and record hit if the guess is correct. Subtract points for wrong
        guess """
        if self._board[row][col] == 'a':  # if guess is correct,mark square as h(hit)
            self._board[row][col] = 'h'
            self._atoms -= 1
            return True

        self.modify_score(row, col, 5)

        return False

    def get_score(self):
        """Return the score"""
        return self._score

    def atoms_left(self):
        """Return the remaining atoms"""
        return self._atoms

    def printBoard(self, stats):
        """Print out the board to track if methods are working properly"""
        if stats == 1:
            board = deepcopy(self._board)
        else:
            board = deepcopy(self._disp)
        board[0][0] = board[9][9] = board[0][9] = board[9][0] = ' '
        print("  0 1 2 3 4 5 6 7 8 9")
        for i in range(len(board)):
            print(i, end=' ')
            for j in range(len(board[0])):
                print(board[i][j], end='')
                if j == len(board[0]) - 1:
                    print(' ' + str(i), end='')
                print(end=' ')
            if i == len(board) - 1:
                print("\n  0 1 2 3 4 5 6 7 8 9")
            else:
                print()
        print()
        print()
        self._disp = deepcopy(self._board)

    def feedback(self, stats):
        """Return the board, get_score, and atom_left to provide feedback on progress"""
        self.printBoard(stats)
        print(f"Score: {self.get_score()}")
        print(f"Atoms Left: {self.atoms_left()}\n\n")
