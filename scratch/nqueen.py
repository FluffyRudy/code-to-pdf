# title: 8
# aim: Program to implement N-Queens Problem using Python.


class NQueens:
    def __init__(self, n):
        self.N = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]

    def print_solution(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print()

    def is_safe(self, row, col):
        for i in range(col):
            if self.board[row][i] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        for i, j in zip(range(row, self.N, 1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        return True

    def solve_util(self, col):
        if col >= self.N:
            return True

        for i in range(self.N):
            if self.is_safe(i, col):
                self.board[i][col] = 1

                if self.solve_util(col + 1):
                    return True

                self.board[i][col] = 0

        return False

    def solve(self):
        if not self.solve_util(0):
            print("Solution does not exist")
            return False

        self.print_solution()
        return True


n_queens = NQueens(4)
n_queens.solve()
