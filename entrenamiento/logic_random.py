##logic 1
import random

N = 8 # quemado el tamanio del tablero
empty = 0 # quemado el espacio disponible

def get_valid_position(board, color):
    n_board = []
    line = []
    for i in range(len(board)):
        if i%N == 0 and i !=0:
            n_board.append(line)
            line = []
        line.append(board[i])
    n_board.append(line)

    return get_computer_move(n_board, color)


def get_computer_move(board, color):

    moves = get_valid_moves(board, color)

    if len(moves) == 0: return None

    random.shuffle(moves)
    return moves[0]

def make_moves(board, positions, color):
    for position in positions:
        board[position[1]][position[0]] = color
    return board

def get_valid_moves(board, color):
    """
    recibe tablero 2d y color del turno actual
    retorna un array de posiciones [(i, j), ...]
    """
    moves = []
    for j in range(N):
        for i in range(N):
            vals = is_valid_movement(board, color, i, j)
            #print "vals: "+str(vals)
            if vals != False:
                moves.append([[i,j], vals])
    return moves

def get_score_board(board):
    results = dict()
    for j in range(N):
        for i in range(N):
            if board[j][i] != empty:
                if results.has_key(board[j][i]):
                    results[board[j][i]] = results[board[j][i]] + 1
                else:
                    results[board[j][i]] = 1
    return results

def is_on_corner(i, j):
    return (i == 0 and j == 0) or (i == N and j == 0) or (i == 0 and j == N) or (i == N and j == N)

def is_valid_movement(board, color, i,j):
    """
    # # #
    # o #
    # # #
    retorna False o un array de posiciones que se deben cambiar
    """
    if board[j][i] != empty: return False

    tiles_to_flip = []

    # arriba a la izquierda
    temp_i = i-1
    temp_j = j-1
    temp_tiles = []
    is_correct = False
    while temp_i >= 0 and temp_j >= 0:
        if board[temp_j][temp_i] == empty: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and i-temp_i == 1: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and i-temp_i > 1:
            #temp_tiles.append([temp_i, temp_j])
            is_correct = True
            break
        else:
            temp_tiles.append([temp_i, temp_j])
        temp_i -= 1
        temp_j -= 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)

    # arriba
    temp_j = j-1
    temp_tiles = []
    is_correct = False
    while temp_j >= 0:
        if board[temp_j][i] == empty: 
            temp_tiles = []
            break
        elif board[temp_j][i] == color and j-temp_j == 1: 
            temp_tiles = []
            break
        elif board[temp_j][i] == color and j-temp_j > 1:
            #temp_tiles.append([i, temp_j])
            is_correct = True
            break
        else:
            temp_tiles.append([i, temp_j])
        temp_j -= 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)

    # arriba a la derecha
    temp_i = i+1
    temp_j = j-1
    temp_tiles = []
    is_correct = False
    while temp_i < N and temp_j >= 0:
        if board[temp_j][temp_i] == empty: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and j-temp_j == 1: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and j-temp_j > 1:
            #temp_tiles.append([temp_i, temp_j])
            is_correct = True
            break
        else:
            temp_tiles.append([temp_i, temp_j])
        temp_i += 1
        temp_j -= 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)

    # a la izquierda
    temp_i = i-1
    temp_tiles = []
    is_correct = False
    while temp_i >= 0:
        if board[j][temp_i] == empty: 
            temp_tiles = []
            break
        elif board[j][temp_i] == color and i-temp_i == 1: 
            temp_tiles = []
            break
        elif board[j][temp_i] == color and i-temp_i > 1:
            #temp_tiles.append([temp_i, j])
            is_correct = True
            break
        else:
            temp_tiles.append([temp_i, j])
        temp_i -= 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)

    # a la derecha
    temp_i = i+1
    temp_tiles = []
    is_correct = False
    while temp_i < N:
        if board[j][temp_i] == empty: 
            temp_tiles = []
            break
        elif board[j][temp_i] == color and temp_i-i == 1: 
            temp_tiles = []
            break
        elif board[j][temp_i] == color and temp_i-i > 1:
            #temp_tiles.append([temp_i, j])
            is_correct = True
            break
        else:
            temp_tiles.append([temp_i, j])
        temp_i += 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)

    # abajo a la izquierda
    temp_i = i-1
    temp_j = j+1
    temp_tiles = []
    is_correct = False
    while temp_i >= 0 and temp_j < N:
        if board[temp_j][temp_i] == empty: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and i-temp_i == 1: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and i-temp_i > 1:
            #temp_tiles.append([temp_i, temp_j])
            is_correct = True
            break
        else:
            temp_tiles.append([temp_i, temp_j])
        temp_i -= 1
        temp_j += 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)

    # abajo
    temp_j = j+1
    temp_tiles = []
    is_correct = False
    while temp_j < N:
        if board[temp_j][i] == empty: 
            temp_tiles = []
            break
        elif board[temp_j][i] == color and temp_j-j == 1: 
            temp_tiles = []
            break
        elif board[temp_j][i] == color and temp_j-j > 1:
            #temp_tiles.append([i, temp_j])
            is_correct = True
            break
        else:
            temp_tiles.append([i, temp_j])
        temp_j += 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)

    # abajo a la derecha
    temp_i = i+1
    temp_j = j+1
    temp_tiles = []
    is_correct = False
    while temp_i < N and temp_j < N:
        if board[temp_j][temp_i] == empty: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and temp_j-j == 1: 
            temp_tiles = []
            break
        elif board[temp_j][temp_i] == color and temp_j-j > 1:
            #temp_tiles.append([temp_i, temp_j])
            is_correct = True
            break
        else:
            temp_tiles.append([temp_i, temp_j])
        temp_i += 1
        temp_j += 1
    if is_correct:
        tiles_to_flip.extend(temp_tiles)
    if len(tiles_to_flip) == 0: return False
    return tiles_to_flip