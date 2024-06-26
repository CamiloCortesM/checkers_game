import copy
from modules import tools, controller


def heuristics(state, qtable_value):
    """
    This heuristic function calculates the search metrics of the alpha beta algorithm according to the utility values for:
        a. Normalized utility values from the number of pawn and king pieces on the board.
        b. Normalized utility values from the number of captures that could be made by kings and pawns.
        c. Normalized utility values from the distances of pawns to become kings.
        d. Normalized utility values from the number of pieces in the safest places on the board.
    """
    board, player = state[0], state[3]
    length = board.get_length()
    r_pawn, w_pawn = 0, 0
    r_king, w_king = 0, 0
    r_captures, w_captures = 0, 0
    r_kingd, w_kingd = 0, 0
    r_safe, w_safe = 0.0, 0.0
    for row in range(length):
        for col in range(length):
            piece = board.get(row, col)
            if piece:
                r = row if row > (length - (row + 1)) else (length - (row + 1))
                c = col if col > (length - (col + 1)) else (length - (col + 1))
                d = int(((r ** 2.0 + c ** 2.0) ** 0.5) / 2.0)
                if piece.color() == 'red':
                    r_captures += sum([len(v) for v in
                                       tools.get_captures(board, row, col)])
                    if piece.is_king():
                        r_king += 1
                    else:
                        r_pawn += 1
                        r_kingd += row + 1
                        r_safe += d
                else:
                    w_captures += sum([len(v) for v in
                                       tools.get_captures(board, row, col)])
                    if piece.is_king():
                        w_king += 1
                    else:
                        w_pawn += 1
                        w_kingd += length - (row + 1)
                        w_safe += d
    if player == 'red':
        red_count_heuristics = 3.354 * (((r_pawn + r_king * 2.0) - (
            w_pawn + 1.0 + w_king * 2.0)) / 1.0 + ((r_pawn + r_king * 2.0) + (w_pawn + w_king * 2.0)))
        red_capture_heuristics = 1.7417 * \
            ((r_captures - w_captures)/(1.0 + r_captures + w_captures))
        red_kingdist_heuristics = 1.429 * \
            ((r_kingd - w_kingd)/(1.0 + r_kingd + w_kingd))
        red_safe_heuristics = 5.263 * \
            ((r_safe - w_safe)/(1.0 + r_safe + w_safe))
        return red_count_heuristics + red_capture_heuristics + red_kingdist_heuristics + red_safe_heuristics+qtable_value
    else:
        white_count_heuristics = 3.354 * (((w_pawn + w_king * 2.0) - (
            r_pawn + 1.0 + r_king * 2.0)) / 1.0 + (((r_pawn + r_king * 2.0) + (w_pawn + w_king * 2.0))))
        white_capture_heuristics = 1.7416 * \
            ((w_captures - r_captures)/(1.0 + r_captures + w_captures))
        white_kingdist_heuristics = 1.428 * \
            ((w_kingd - r_kingd)/(1.0 + r_kingd + w_kingd))
        white_safe_heuristics = 5.263 * \
            ((w_safe - r_safe)/(1.0 + r_safe + w_safe))
        return white_count_heuristics + white_capture_heuristics + white_kingdist_heuristics + white_safe_heuristics+qtable_value


def utility(state, qtable_value):
    """
    This function calculates the utility of a node, if it is a terminal node.
    """
    return heuristics(state, qtable_value)


def is_terminal(state, maxdepth=None):
    """
    Determines if a tree node is a terminal or not.
    Returns boolean True/False.
    """
    board, turn, depth,player = state
    (moves, captures) = controller.get_hints(board, turn)
    if maxdepth is not None:
        return ((not moves) and (not captures)) or depth >= maxdepth
    else:
        return ((not moves) and (not captures))


def transition(state, action, ttype, qtable):
    """
    This is the transition function. Given a board state and action,
    it transitions to the next board state.
    """
    if type(action) == list:
        action = tuple(action)
        
    board = copy.deepcopy(state[0])
    turn = state[1]
    depth = state[2]

    if ttype == "move":
        controller.apply_move(board, action)
    elif ttype == "jump":
        row, col = action[1]
        if (controller.apply_capture(board, action)):
            if (tools.get_jumps(board, row, col)):
                capture = tools.get_jumps(board, row, col)
                if capture:
                    transition(state, [(row, col), capture[0]], "jump",qtable)
                    return (board, turn, depth,state[3])

    turn = 'white' if state[1] == 'red' else 'red'
    depth += 1
    
    qtable.update_value(state, action)

    return (board, turn, depth,state[3])


def maxvalue(state, maxdepth, qtable, action, alpha=None, beta=None):
    """
    The maxvalue function for the adversarial tree search.
    """
    board, turn = state[0], state[1]
    if is_terminal(state, maxdepth):
        if type(action) == list:
            action = tuple(action)
        return utility(state, qtable.get_value(state, action))
    else:
        v = float('-inf')
        (moves, captures) = controller.get_hints(board, turn)
        if captures:
            for a in captures:
                v = max(v, minvalue(transition(state, a, "jump", qtable),
                        maxdepth, qtable, a, alpha, beta,))
                if alpha is not None and beta is not None:
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v
        elif moves:
            for a in moves:
                v = max(v, minvalue(transition(state, a, "move", qtable),
                        maxdepth, qtable, a, alpha, beta,))
                if alpha is not None and beta is not None:
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v


def minvalue(state, maxdepth, qtable, action, alpha=None, beta=None,):
    """
    The minvalue function for the adversarial tree search.
    """
    board, turn = state[0], state[1]
    if is_terminal(state, maxdepth):
        if type(action) == list:
            action = tuple(action)
        return utility(state, qtable.get_value(state, action))
    else:
        v = float('inf')
        (moves, captures) = controller.get_hints(board, turn)
        if captures:
            for a in captures:
                v = min(v, maxvalue(transition(state, a, "jump", qtable),
                                    maxdepth, qtable, a, alpha, beta))
                if alpha is not None and beta is not None:
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v
        elif moves:
            for a in moves:
                v = min(v, maxvalue(transition(state, a, "move", qtable),
                                    maxdepth, qtable, a, alpha, beta))
                if alpha is not None and beta is not None:
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v


def minimax_search(state, maxdepth=None):
    """
    The depth limited minimax tree search.
    """
    board = state[0]
    turn = state[1]
    (moves, captures) = controller.get_hints(board, turn)
    if captures:
        return max([(a, minvalue(transition(state, a, "jump"), maxdepth))
                    for a in captures], key=lambda v: v[1])
    elif moves:
        return max([(a, minvalue(transition(state, a, "move"), maxdepth))
                    for a in moves], key=lambda v: v[1])
    else:
        return ("pass", -1)


def alphabeta_search(state, qtable, maxdepth=None):
    """
    Searching for alpha-beta trees of limited depth
    """

    board = state[0]
    turn = state[1]

    # my_immutable_list = [tuple(item) for item in board]
    # board_tuple = tuple(my_immutable_list)
    # new_state = (board_tuple,state[1],state[2])

    (moves, captures) = controller.get_hints(board, turn)
    alpha = float('-inf')
    beta = float('inf')
    if captures:
        return max([
            (a, minvalue(transition(state, a, "jump", qtable),
                         maxdepth, qtable, a, alpha, beta))
            for a in captures], key=lambda v: v[1])
    elif moves:
        return max([
            (a, minvalue(transition(state, a, "move", qtable),
                         maxdepth, qtable, a, alpha, beta))
            for a in moves], key=lambda v: v[1])
    else:
        return ("pass", -1)


def get_next_move(board, turn, qtable, maxdepth=4):
    """
    function to obtain the best play with alphabeta_search

    - tree with six levels is alphabeta_search(state, 6)
    """
    player = turn
    state = (board, turn, 0, player)
    print("Thinking ...")
    move = alphabeta_search(state, qtable, maxdepth)
    return move[0]
