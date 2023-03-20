import random
from modules import tools, controller


class QTable:
    def __init__(self):
        self.table = {}

    def get_value(self, state, action):
        if state not in self.table:
            self.table[state] = {}
        if action not in self.table[state]:
            self.table[state][action] = 0.0
        return self.table[state][action]

    def update_value(self, state, action, alpha=0.1, gamma=0.9):
        player = state[3]
        reward = 0
        old_value = self.get_value(state, action)
        if player == "white":
            board_pieces = controller.count_pieces(state[0])
            (red, white) = board_pieces
            reward = (white-red)+(len(self.get_actions(state))/97)
        else:
            board_pieces = controller.count_pieces(state[0])
            (red, white) = board_pieces
            reward = (red-white)+(len(self.get_actions(state))/97)
        new_value = (1 - alpha) * old_value + alpha * \
            (reward + gamma)
        self.table[state][action] = new_value

    def get_actions(self, state):
        board, player = state[0], state[3]
        actions = 0
        for row in range(board.get_length()):
            for col in range(board.get_length()):
                piece = board.get(row, col)
                if piece and piece.color() == player:
                    moves = tools.get_moves(board, row, col)
                    captures = tools.get_captures(board, row, col)
                    if captures:
                        moves = captures
                    actions += len(moves)
        return actions

    def get_best_action(self, state, epsilon=0.1):
        if random.random() < epsilon:
            return random.choice(self.get_actions(state))
        else:
            actions = self.get_actions(state)
            values = [self.get_value(state, a) for a in actions]
            max_value = max(values)
            best_actions = [a for a, v in zip(
                actions, values) if v == max_value]
            return random.choice(best_actions)
