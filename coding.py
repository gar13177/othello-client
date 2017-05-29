# coding
import md5

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

# primer tablero: 307c955dffaccfedbdd831ec85ac51da