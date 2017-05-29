from socketIO_client import SocketIO, LoggingNamespace
from logic import get_valid_position as gvp
#from logic_0 import get_valid_position as gvp
import sys

ready = False
userName = None
winnerTurnID = None
boardTiles = []
tournamentID = -1
currentTurnID = None
currentGameID = None
gameFinished = None
socketIO = None

lastBoard = None

tiros = 0
tableros_iguales = 0


def transformBoard(board):
    result = []
    for i in range(len(board)):
        result.append({'id': i, 'color': board[i]})
    return result

def play(position):
    global ready, boardTiles, socketIO,tournamentID,currentTurnID,currentGameID, tiros, lastBoard, tableros_iguales
    if lastBoard == boardTiles:
        tableros_iguales = tableros_iguales + 1

    lastBoard = boardTiles[:]
    
    if (ready and boardTiles[position]['color'] == 0):
        print 'play'
        ready = True
        boardTiles[position]['color'] = 3

        variables = {}
        variables['tournament_id'] = tournamentID 
        variables['player_turn_id'] = currentTurnID 
        variables['game_id'] = currentGameID 
        variables['movement'] = position
        socketIO.emit('play', variables)
    tiros = tiros + 1
    print 'end play'

def on_connect():
    global socketIO, tournamentID, userName
    print 'connect'
    user = {}
    user['user_name'] = userName
    user['tournament_id'] = tournamentID
    user['user_role'] = 'player'

    socketIO.emit('signin', user)

def pretty_print(board):
    chars = ''
    for i in range(len(board)):
        if i%8 == 0 and i != 0:
            chars+= '\n'
        chars = chars + str(board[i]['color'])+ '  ' 
    print chars

def reset_board():
    global boardTiles, tiros, tableros_iguales
    tableros_iguales = 0
    tiros = 0
    board = []
    for i in range(8*8):
        board.append(0)
    boardTiles = transformBoard(board)

def on_ready(args):
    global ready, boardTiles, currentGameID,currentTurnID,gameFinished
    gameFinished = False
    currentGameID = args['game_id']
    currentTurnID = args['player_turn_id']
    boardTiles = transformBoard(args['board'])
    ready = True
    print 'ready'
    pretty_print(boardTiles)
    # position = input('ingrese posicion')
    #position = get_valid_position(boardTiles, currentTurnID)
    position = gvp(boardTiles, currentTurnID)
    play(position) 


def on_finish(args):
    global boardTiles,currentGameID,currentTurnID,gameFinished,socketIO,tournamentID, winnerTurnID
    currentGameID = args['game_id']
    currentTurnID = args['player_turn_id']
    boardTiles = transformBoard(args['board'])
    gameFinished = True
    print "tiros: "+str(tiros)
    print "juegos iguales: "+str(tableros_iguales)

    if (gameFinished):
        variables = {}
        variables['tournament_id'] = tournamentID
        variables['game_id'] = currentGameID
        variables['player_turn_id'] = currentTurnID
        socketIO.emit('player_ready', variables)

        gameFinished = False

        reset_board()    

if __name__ == '__main__':  
    print sys.argv  
    if len(sys.argv) > 4:
        #sys.argv[1] ip
        #sys.argv[2] port
        #sys.argv[3] tournament id 
        #sys.argv[4] username
        #global tournamentID, userName
        tournamentID = sys.argv[3]
        userName = sys.argv[4]
        socketIO = SocketIO(sys.argv[1],sys.argv[2])
        socketIO.on('connect',on_connect)
        socketIO.on('ready', on_ready)
        socketIO.on('finish', on_finish)
        socketIO.wait()
    else:
        print "Uso correcto: python "+str(sys.argv[0])+" <ip> <port> <tournament id> <user name>"
