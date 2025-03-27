import numpy as np
import Minimax
from client import ConnectFourClient


class Connect4:
    NUM_ROWS, NUM_COLS = 6, 7

    def __init__(self):
        self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS))
        self.running = True
        self.client = ConnectFourClient()
        self.client.connect()
        self.turn = int(self.client.client_socket.recv(1024).decode('utf-8'))
        print(f"You are player{self.turn}")
        self.player = self.turn
        print(self.turn)
        self.game_loop()

    def game_loop(self):
        while self.running:
            # if self.check_winner(1) or self.check_winner(2) or all(self.board[0, :]):
            #     self.client.close()
            #     break
            if self.turn == 1:  # AI tính toán nước đi và gửi lên server
                _, col = Minimax.Minimax(4, self.player, self.board).minimax(self.board, 4, -np.inf, np.inf, True)
                self.drop_piece(col)
                self.client.send_move(col)
            elif self.turn == 2:  # Người chơi nhận nước đi từ server
                col = self.client.get_move()
                if col == -1:
                    break
                if 0 <= col < self.NUM_COLS:
                    self.drop_piece(col)

    def reset(self):
        self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS))
        self.turn = 1
        self.running = True

    def check_winner(self, player):
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS):
                if self.board[row, col] == player:
                    if self.check_horizontal(row, col, player) or self.check_vertical(row, col,
                                                                                      player) or self.check_diagonal(
                            row, col, player):
                        return True

    def check_horizontal(self, row, col, player):
        return col + 3 < self.NUM_COLS and all(self.board[row, col + i] == player for i in range(4))

    def check_vertical(self, row, col, player):
        return row + 3 < self.NUM_ROWS and all(self.board[row + i, col] == player for i in range(4))

    def check_diagonal(self, row, col, player):
        return (row + 3 < self.NUM_ROWS and col + 3 < self.NUM_COLS and all(
            self.board[row + i, col + i] == player for i in range(4))) or \
            (row - 3 >= 0 and col + 3 < self.NUM_COLS and all(self.board[row - i, col + i] == player for i in range(4)))

    def drop_piece(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            if row is not None:
                self.board[row, col] = self.turn
                self.turn = 3 - self.turn

        if self.check_winner(self.player):
            print("You wins!")
            self.running = False
            self.reset()
        elif self.check_winner(3 - self.player):
            print('You lose!')
            self.running = False
            self.reset()
        elif all(self.board[0, :]):
            print("It's a tie!")
            self.running = False
            self.reset()

    def is_valid_location(self, col):
        return self.board[0, col] == 0

    def get_next_open_row(self, col):
        for row in range(self.NUM_ROWS - 1, -1, -1):
            if self.board[row, col] == 0:
                return row
        return None


if __name__ == "__main__":
    Connect4()