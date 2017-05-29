from logic_random import get_valid_position
from pymongo import MongoClient
from time import time
import md5, pprint, random, sys, signal

class GameConstants:
    PLAYER_1_TURN_ID = 1
    PLAYER_2_TURN_ID = 2
    N = 8

def ix(x, y):
    global N
    return x + y * N

def getStartingBoard():
    global N, EMPTY, WHITE, BLACK
    board = dict()
    for x in range(N):
        for y in range(N):
            board[ix(x,y)] = EMPTY

    x2 = N >> 1
    y2 = N >> 1
    
    board[ix(x2 - 1, y2 - 1)] = WHITE
    board[ix(x2 - 1, y2 - 0)] = BLACK
    board[ix(x2 - 0, y2 - 1)] = BLACK
    board[ix(x2 - 0, y2 - 0)] = WHITE
    return board

def pretty_print(board):
    global N
    p_board = ''
    for i in range(len(board)):
        if i % N == 0 and i != 0:
            p_board += '\n'
        p_board = p_board + str(board[i]) + '  '
    return p_board

def to_string(board, color):
    s = str(color)
    for i in range(len(board)):
        s += str(board[i])
    return s

def get_key(board, color):
    m = md5.new()
    _id = to_string(board, color)
    m.update(_id)
    return m.hexdigest()

def dict_to_str_key(dictionary):
    temp = dict()
    for i in range(len(dictionary)):
        temp[str(i)] = dictionary[i]
    return temp

def build_collection(board, color):
    collection = dict()
    collection["_id"] = get_key(board,color)
    collection["player"] = color
    collection["board"] = dict_to_str_key(board)
    collection["child"] = dict()
    collection["win"] = 0
    collection["lose"] = 0
    collection["draw"] = 0
    return collection

def set_db_initials():
    global col
    board = getStartingBoard()
    players = [BLACK, WHITE]

    for player in players:
        _id = get_key(board,player)
        #pprint.pprint(col.find_one({'_id':_id}))
        if col.find({'_id':_id}).count() == 0:#si no existe
            collection = build_collection(board, player)
            col.insert_one(collection)



def get_result(board, p1, p2):
    """
    board es un diccionario
    se retorna p1-p2
    """
    p1_s = sum(x == p1 for x in board.values())
    p2_s = sum(x == p2 for x in board.values())
    return p1_s-p2_s

def increment_variable(col_ids, field):
    global col
    col_ids = set(col_ids)
    for _id in col_ids:
        col.update_one(
                {
                    "_id": _id
                },{
                    '$inc' : {
                        field: 1
                    }
                },
                upsert=False
            )

def play():
    global col
    board = getStartingBoard()
    players = [BLACK, WHITE]
    #random.shuffle(players) # alternamos el inicio del juego

    boards = dict() # llaves que se tienen que actualizar con minimax
    boards[BLACK] = []
    boards[WHITE] = []
    turno = 0
    current_b = get_key(board,players[turno])
    boards[players[turno]].append(current_b) # agrego el primer tablero 

    while True:
        move = get_valid_position(board, players[turno])
        index = -1 # por default, si no tiene tiro, asumo que es -1
        if move == None:
            n_move = get_valid_position(board, players[(turno+1)%2])
            if n_move == None:
                #quiere decir que ya no hay movimientos validos
                break
            #print 'sin turno'
        else:
            index = ix(move[0][0], move[0][1])
            board[index] = players[turno]
            for position in move[1]:
                board[ix(position[0], position[1])] = players[turno]

        if index == 0 or index == N-1 or index == N*(N-1) or index == N*N-1:
            playing = False
            print current_b+', '+str(index)
        # el tablero hijo le pertenece al otro jugador
        _id = get_key(board,players[(turno+1)%2])
        if col.find({'_id':_id}).count() == 0:
            #si no existe, lo inserto
            collection = build_collection(board,players[(turno+1)%2])
            col.insert_one(collection)
        col.update_one(
            {
                "_id": current_b
            },{
                '$set' : {
                    'child.'+_id: index
                }
            },
            upsert=False
        )
        current_b = _id
        boards[players[(turno+1)%2]].append(current_b) # agrego el siguiente board
        turno = (turno + 1) % 2
            
        #print '\n'+pretty_print(board)

    result = get_result(board, BLACK, WHITE) # resultado como signo BLACK - WHITE
    if result == 0: # empate
        increment_variable(boards[BLACK],'draw')
        increment_variable(boards[WHITE],'draw')
    elif result < 0: # gana WHITE
        increment_variable(boards[BLACK],'lose')
        increment_variable(boards[WHITE],'win')
    elif result > 0: # gana BLACK
        increment_variable(boards[BLACK],'win')
        increment_variable(boards[WHITE],'lose')
    #print 'Finalizado'

def signal_handler(signal, frame):
    global playing
    print 'Esperando a ultima partida'
    playing = False

def stats(count, time_init, time_end):
    """
    time_init, time_end diferencia en segundos
    """
    avg_sec = count/float(time_end-time_init) # promedio de partidos por segundo
    avg_min = count/(float(time_end-time_init)/60) # promedio de partidos por minuto
    avg_hou = count/(float(time_end-time_init)/3600) # promedio de partidos por hora
    avg_day = count/(float(time_end-time_init)/86400) # promedio de partidos por dia
    
    print 'Partidas jugadas: '+str(count)
    print 'Partidas por segundo: '+str(avg_sec)
    print 'Partidas por minuto: '+str(avg_min)
    print 'Partidas por hora: '+str(avg_hou)
    print 'Partidas por dia: '+str(avg_day)



EMPTY = 0
BLACK = GameConstants.PLAYER_1_TURN_ID
WHITE = GameConstants.PLAYER_2_TURN_ID
N = GameConstants.N

client = MongoClient('localhost', 27017)
db = client['othello']
col = db['move']

playing = True

if __name__ == '__main__':  
    print sys.argv  
    if len(sys.argv) == 1:
        #count = int(sys.argv[1])
        count = 0
        set_db_initials()

        #se crea un evento para Ctrl+C para que termine el ultimo juego
        signal.signal(signal.SIGINT, signal_handler)
        time_init = time()
        while playing:
            play()
            count += 1
        print 'Finalizado'
        time_end = time()
        stats(count,time_init, time_end)
    else:
        print "Uso correcto: python "+str(sys.argv[0])

