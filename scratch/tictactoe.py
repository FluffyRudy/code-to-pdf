# title: 3
# aim: Program to implement Tic-Tac-Toe game using Python.


import random


def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board):
    for row in board:
        if row.count(row[0]) == 3 and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None


def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    for turn in range(9):
        player = players[turn % 2]
        row, col = random.randint(0, 2), random.randint(0, 2)
        while board[row][col] != " ":
            row, col = random.randint(0, 2), random.randint(0, 2)
        board[row][col] = player
        print_board(board)
        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            return
    print("It's a draw!")


tic_tac_toe()
