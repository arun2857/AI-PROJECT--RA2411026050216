import time

def create_board():
    return ['' for _ in range(9)]

def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == '']

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in wins:
        if board[combo[0]] and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]], combo
    return None, None

def is_draw(board):
    return all(cell != '' for cell in board) and check_winner(board)[0] is None

def minimax(board, depth, is_maximizing, alpha, beta, nodes_count):
    nodes_count[0] += 1
    winner, _ = check_winner(board)
    if winner == 'O': return 10 - depth
    if winner == 'X': return depth - 10
    if is_draw(board): return 0

    moves = get_available_moves(board)
    if is_maximizing:
        best = -float('inf')
        for move in moves:
            board[move] = 'O'
            val = minimax(board, depth + 1, False, alpha, beta, nodes_count)
            board[move] = ''
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for move in moves:
            board[move] = 'X'
            val = minimax(board, depth + 1, True, alpha, beta, nodes_count)
            board[move] = ''
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def get_best_move(board):
    nodes_count = [0]
    best_val = -float('inf')
    best_move = -1
    start = time.perf_counter()

    for move in get_available_moves(board):
        board[move] = 'O'
        move_val = minimax(board, 0, False, -float('inf'), float('inf'), nodes_count)
        board[move] = ''
        if move_val > best_val:
            best_val = move_val
            best_move = move

    elapsed = (time.perf_counter() - start) * 1000
    return best_move, nodes_count[0], elapsed
