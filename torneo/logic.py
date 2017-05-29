## 
from random import shuffle

N = 8 # quemado el tamanio del tablero
empty = 0 # quemado el espacio disponible


def get_valid_position(board, color):
    
    n_board = []
    line = []
    for i in range(len(board)):
        if i%N == 0 and i !=0:
            n_board.append(line)
            line = []
        line.append(board[i]['color'])
    n_board.append(line)

    positions = []
    for j in range(N):
        for i in range(N):
            if is_valid_movement(n_board, color, i, j):
                positions.append(j*N+i)

    if len(positions) > 0:
        shuffle(positions)
        return positions[0]

    print 'error'
    return -1

def is_valid_movement(board, color, i,j):
    """
    # # #
    # o #
    # # #
    """
    if board[j][i] != empty: return False

    # arriba a la izquierda
    temp_i = i-1
    temp_j = j-1
    while temp_i >= 0 and temp_j >= 0:
        if board[temp_j][temp_i] == empty: break
        elif board[temp_j][temp_i] == color and i-temp_i == 1: break
        elif board[temp_j][temp_i] == color and i-temp_i > 1:
            return True
        temp_i -= 1
        temp_j -= 1

    # arriba
    temp_j = j-1
    while temp_j >= 0:
        if board[temp_j][i] == empty: break
        elif board[temp_j][i] == color and j-temp_j == 1: break
        elif board[temp_j][i] == color and j-temp_j > 1:
            return True
        temp_j -= 1

    # arriba a la derecha
    temp_i = i+1
    temp_j = j-1
    while temp_i < N and temp_j >= 0:
        if board[temp_j][temp_i] == empty: break
        elif board[temp_j][temp_i] == color and j-temp_j == 1: break
        elif board[temp_j][temp_i] == color and j-temp_j > 1:
            return True
        temp_i += 1
        temp_j -= 1

    # a la izquierda
    temp_i = i-1
    while temp_i >= 0:
        if board[j][temp_i] == empty: break
        elif board[j][temp_i] == color and i-temp_i == 1: break
        elif board[j][temp_i] == color and i-temp_i > 1:
            return True
        temp_i -= 1

    # a la derecha
    temp_i = i+1
    while temp_i < N:
        if board[j][temp_i] == empty: break
        elif board[j][temp_i] == color and temp_i-i == 1: break
        elif board[j][temp_i] == color and temp_i-i > 1:
            return True
        temp_i += 1

    # abajo a la izquierda
    temp_i = i-1
    temp_j = j+1
    while temp_i >= 0 and temp_j < N:
        if board[temp_j][temp_i] == empty: break
        elif board[temp_j][temp_i] == color and i-temp_i == 1: break
        elif board[temp_j][temp_i] == color and i-temp_i > 1:
            return True
        temp_i -= 1
        temp_j += 1

    # abajo
    temp_j = j+1
    while temp_j < N:
        if board[temp_j][i] == empty: break
        elif board[temp_j][i] == color and temp_j-j == 1: break
        elif board[temp_j][i] == color and temp_j-j > 1:
            return True
        temp_j += 1
    
    # abajo a la derecha
    temp_i = i+1
    temp_j = j+1
    while temp_i < N and temp_j < N:
        if board[temp_j][temp_i] == empty: break
        elif board[temp_j][temp_i] == color and temp_j-j == 1: break
        elif board[temp_j][temp_i] == color and temp_j-j > 1:
            return True
        temp_i += 1
        temp_j += 1

    return False