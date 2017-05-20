##logic 1
import md5
from logic_1 import get_next_move

N = 8 # quemado el tamanio del tablero
empty = 0 # quemado el espacio disponible

def get_valid_position(board, color):
    _id = get_key(board, color)
    move = get_next_move(_id)
    if move != None:
        print 'eleccion'
        return move
    print _id
    print 'logica'

    n_board = []
    line = []
    for i in range(len(board)):
        if i%N == 0 and i !=0:
            n_board.append(line)
            line = []
        line.append(board[i]['color'])
    n_board.append(line)

    move = get_computer_move(n_board, color)

    print "move: "+str(move)
    if move[0] == -1:
        return -1

    return move[1]*N + move[0]

def to_string(board, color):
    s = str(color)
    for i in range(len(board)):
        s += str(board[i]['color'])
    return s

def get_key(board, color):
    m = md5.new()
    _id = to_string(board, color)
    m.update(_id)
    return m.hexdigest()


def get_computer_move(board, color):

    positions, change_tiles = get_valid_moves(board, color)

    #print "positions: "+str(positions)

    for i in range(len(positions)):
        if is_on_corner(positions[i][0], positions[i][1]):
            return positions[i]
        
    best_move = [-1,-1]

    best_score = -1
    for i in range(len(positions)): # para cada movimiento valido
        temp_board = board[:]
        change_tiles[i].append(positions[i])
        temp_board = make_moves(temp_board,change_tiles[i], color)
        score = get_score_board(temp_board)[color]
        if score > best_score:
            best_move = positions[i]
            best_score = score
    return best_move

def make_moves(board, positions, color):
    for position in positions:
        board[position[1]][position[0]] = color
    return board

def get_valid_moves(board, color):
    """
    recibe tablero 2d y color del turno actual
    retorna un array de posiciones [(i, j), ...]
    """
    positions = []
    change_tiles = []
    for j in range(N):
        for i in range(N):
            vals = is_valid_movement(board, color, i, j)
            #print "vals: "+str(vals)
            if vals != False:
                positions.append([i, j])
                change_tiles.append(vals)
    return positions, change_tiles

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