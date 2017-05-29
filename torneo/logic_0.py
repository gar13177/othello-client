##logic 1
import md5
from logic_1 import get_next_move, get_corner

N = 8 # quemado el tamanio del tablero
EMPTY = 0 # quemado el espacio disponible
BLACK = 1
WHITE = 2

WEIGHT = [
 [20, -3, 11, 8, 8, 11, -3, 20],
 [-3, -7, -4, 1, 1, -4, -7, -3],
 [11, -4,  2, 2, 2,  2, -4, 11],
 [ 8,  1,  2,-3,-3,  2,  1,  8],
 [ 8,  1,  2,-3,-3,  2,  1,  8],
 [11, -4,  2, 2, 2,  2, -4, 11],
 [-3, -7, -4, 1, 1, -4, -7, -3],
 [20, -3, 11, 8, 8, 11, -3, 20],
]

def get_valid_position(board, color):
    _id = get_key(board, color)

    # se le da prioridad a las esquinas
    move = get_corner(_id)
    if move != None:
        print 'esquina'
        return move

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

    
    # prioridad a las esquinas
    for i in range(len(positions)):
        if is_on_corner(positions[i][0], positions[i][1]):
            return positions[i]

    best_move = [-1,-1]

    best_score = -float('inf')
    for i_abs in range(len(positions)): # para cada movimiento valido
        temp_board = board[:]
        change_tiles[i_abs].append(positions[i_abs])

        # siguiente tablero
        temp_board = make_moves(temp_board,change_tiles[i_abs], color)

        piece_diff_raw = get_score_board(temp_board)
        piece_diff = 0

        # se cuenta la diferencia de piezas y se busca lo siguiente:
        # 100*B/(B+W) o 100*W/(B+W) siendo el de arriba el mayor
        # 0 si son iguales
        if piece_diff_raw[BLACK] > piece_diff_raw[WHITE]:
            piece_diff = 100 * float(piece_diff_raw[BLACK])/(piece_diff_raw[BLACK]+piece_diff_raw[WHITE])
            if color != BLACK: # si soy los negros, y hay mas blancos, lo multiplico por -1
                piece_diff = -1*piece_diff
        elif piece_diff_raw[BLACK] < piece_diff_raw[WHITE]:
            piece_diff = 100 * float(piece_diff_raw[WHITE])/(piece_diff_raw[BLACK]+piece_diff_raw[WHITE])
            if color != WHITE: # si soy los blancos, y hay mas negros, lo multiplico por -1
                piece_diff = -1*piece_diff
        
        # calculo de esquinas
        corners = {BLACK:0, WHITE:0}
        for j in (0,N-1):
            for i in (0,N-1):
                if temp_board[j][i] == BLACK:
                    corners[BLACK] = corners[BLACK] +1 
                elif temp_board[j][i] == WHITE:
                    corners[WHITE] = corners[WHITE] +1 

        corners_diff = 0.0
        if color == BLACK:
            corners_diff = float(25*corners[BLACK]-25*corners[WHITE])
        elif color == WHITE:
            corners_diff = float(25*corners[WHITE]-25*corners[BLACK])

        # calculo de cerca de esquinas
        corners_close = {BLACK:0, WHITE:0}
        for j in (0,N-1):
            for i in (0,N-1):
                if temp_board[j][i] == EMPTY:
                    if i == 0 and j == 0:
                        if temp_board[j+1][i] == BLACK:
                            corners_close[BLACK] = corners_close[BLACK] +1 
                        elif temp_board[j+1][i] == WHITE:
                            corners_close[WHITE] = corners_close[WHITE] +1 

                        if temp_board[j][i+1] == BLACK:
                            corners_close[BLACK] = corners_close[BLACK] +1 
                        elif temp_board[j][i+1] == WHITE:
                            corners_close[WHITE] = corners_close[WHITE] +1 

                        if temp_board[j+1][i+1] == BLACK:
                            corners_close[BLACK] = corners_close[BLACK] +1 
                        elif temp_board[j+1][i+1] == WHITE:
                            corners_close[WHITE] = corners_close[WHITE] +1 

                    elif i == N-1 and j==N-1:
                        if temp_board[j-1][i] == BLACK:
                            corners_close[BLACK] = corners_close[BLACK] +1 
                        elif temp_board[j-1][i] == WHITE:
                            corners_close[WHITE] = corners_close[WHITE] +1
                            
                        if temp_board[j][i-1] == BLACK:
                            corners_close[BLACK] = corners_close[BLACK] +1 
                        elif temp_board[j][i-1] == WHITE:
                            corners_close[WHITE] = corners_close[WHITE] +1 

                        if temp_board[j-1][i-1] == BLACK:
                            corners_close[BLACK] = corners_close[BLACK] +1 
                        elif temp_board[j-1][i-1] == WHITE:
                            corners_close[WHITE] = corners_close[WHITE] +1 
        
        corners_close_diff = 0.0
        if color == BLACK:
            corners_close_diff = float(-12.5*corners_close[BLACK]+12.5*corners_close[WHITE])
        elif color == WHITE:
            corners_close_diff = float(-12.5*corners_close[WHITE]+12.5*corners_close[BLACK])
        
        # posibles movimientos
        new_moves = {BLACK:0, WHITE:0}
        b_positions, change_tiles_t = get_valid_moves(temp_board, BLACK)
        new_moves[BLACK] = len(b_positions)
        b_positions, change_tiles_t = get_valid_moves(temp_board, WHITE)
        new_moves[WHITE] = len(b_positions)

        new_moves_diff = 0.0
        if new_moves[BLACK] > new_moves[WHITE]:
            new_moves_diff = 100 * float(new_moves[BLACK])/(new_moves[BLACK]+new_moves[WHITE])
            if color != BLACK: # si soy los negros, y hay mas blancos, lo multiplico por -1
                new_moves_diff = -1*new_moves_diff
        elif new_moves[BLACK] < new_moves[WHITE]:
            new_moves_diff = 100 * float(new_moves[WHITE])/(new_moves[BLACK]+new_moves[WHITE])
            if color != WHITE: # si soy los blancos, y hay mas negros, lo multiplico por -1
                new_moves_diff = -1*new_moves_diff

        # piezas adyacentes
        frontier = get_frontier_discs(temp_board)
        frontier_diff = 0.0
        if frontier[BLACK] > frontier[WHITE]:
            frontier_diff = 100 * float(frontier[BLACK])/(frontier[BLACK]+frontier[WHITE])
            if color != BLACK: # si soy los negros, y hay mas blancos, lo multiplico por -1
                frontier_diff = -1*frontier_diff
        elif frontier[BLACK] < frontier[WHITE]:
            frontier_diff = 100 * float(frontier[WHITE])/(frontier[BLACK]+frontier[WHITE])
            if color != WHITE: # si soy los blancos, y hay mas negros, lo multiplico por -1
                frontier_diff = -1*frontier_diff

        # valoracion del tablero con peso
        weight = get_disc_squares(temp_board)
        weight_diff = 0.0
        if color == BLACK:
            weight_diff = weight[BLACK]-weight[WHITE]
        elif color == WHITE:
            weight_diff = weight[WHITE]-weight[BLACK]

        score = 10.0*piece_diff + 801.724*corners_diff + 382.026*corners_close_diff + 78.922*new_moves_diff + 74.396*frontier_diff + 10*weight_diff
        if score > best_score:
            print 'index: '+str(i_abs)
            best_move = positions[i_abs]
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

def get_disc_squares(board):
    results = {BLACK:0, WHITE:0, EMPTY:0}

    for j in range(len(board)):
        for i in range(len(board[j])):
            results[board[j][i]] = results[board[j][i]] + WEIGHT[j][i]

    return results

def get_frontier_discs(board):
    results = {BLACK:0, WHITE:0}
    for j in range(N):
        for i in range(N):
            if board[j][i] != EMPTY:
                checked = False
                if j > 0:
                    if board[j-1][i] == EMPTY:
                        results[board[j][i]] = results[board[j][i]] + 1
                        checked = True
                if j < N-1 and not checked:
                    if board[j+1][i] == EMPTY:
                        results[board[j][i]] = results[board[j][i]] + 1
                        checked = True
                if i > 0 and not checked:
                    if board[j][i-1] == EMPTY:
                        results[board[j][i]] = results[board[j][i]] + 1
                        checked = True
                if i < N-1 and not checked:
                    if board[j][i+1] == EMPTY:
                        results[board[j][i]] = results[board[j][i]] + 1
                        checked = True
    return results

def get_score_board(board):
    results = {BLACK:0,WHITE:0,EMPTY:0}
    for j in range(N):
        for i in range(N):
            if board[j][i] != EMPTY:
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
    if board[j][i] != EMPTY: return False

    tiles_to_flip = []

    # arriba a la izquierda
    temp_i = i-1
    temp_j = j-1
    temp_tiles = []
    is_correct = False
    while temp_i >= 0 and temp_j >= 0:
        if board[temp_j][temp_i] == EMPTY: 
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
        if board[temp_j][i] == EMPTY: 
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
        if board[temp_j][temp_i] == EMPTY: 
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
        if board[j][temp_i] == EMPTY: 
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
        if board[j][temp_i] == EMPTY: 
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
        if board[temp_j][temp_i] == EMPTY: 
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
        if board[temp_j][i] == EMPTY: 
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
        if board[temp_j][temp_i] == EMPTY: 
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

