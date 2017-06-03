## nueva logica
from pymongo import MongoClient
#from sshtunnel import SSHTunnelForwarder
import pprint

def get_corner(_id):
    global N
    head = col.find_one({'_id': _id})
    if head == None:
        return None
    
    moves = head['child'] # dictionary : _id: move

    d = dict((k,v) for k,v in moves.items() if (v == 0 or v == N-1 or v == N*(N-1) or v == N*N-1 ))
    if len(d) == 0:
        return None
    
    key, value =  d.popitem()
    return value

def get_value(_id):
    global col
    head = col.find_one({'_id': _id})
    if head == None:
        return 0
    return head['win'] * 2 + head['draw'] - head['lose']


def get_with_minimax(_id, depth = 4):
    global N
    head = col.find_one({'_id': _id})
    if head == None:
        return None

    moves = head['child'] # dictionary : _id: move

    if not any(moves):
        return None

    points = dict()
    for key in moves.keys():
        points[key] = mini_max(key, depth, -float('inf'), float('inf'), False )

    pprint.pprint(points)

    max_key = max(points, key=lambda k: points[k])
    return head['child'][max_key]
    
    
def mini_max(_id, depth, a, b, maximizingPlayer):
    
    head = col.find_one({'_id': _id})
    if head == None:
        return None

    # si no tiene un solo hijo guardado
    if not any(head['child']) or depth == 0:
        return head['win'] * 2 + head['draw'] - head['lose']

    if maximizingPlayer:
        v = -float('inf')
        for key in head['child'].keys():
            v = max(v, mini_max(key, depth -1, a, b, False))
            a = max(a, v)
            if b <= a:
                break
        return v
    else:
        v = float('inf')
        for key in head['child'].keys():
            v = min(v, mini_max(key, depth -1, a, b, True))
            b = min(b, v)
            if b <= a:
                break
            return v
    

    
    

def get_next_move(_id):
    """
    recibe el id de la partida actual
    retorna None o el proximo tiro considerado como array, no matriz
    """
    global col 

    head = col.find_one({'_id': _id})
    if head == None:
        return None
    
    head_children = head['child'].keys() # id's con los hijos de la cabeza

    children = col.find({'_id': {'$in': head_children}})
    if children.count() == 0: # si no tiene ni un solo hijo...
        return None

    def_weight = {'weight':-float('inf')}
    children_map = dict()
    for child in children: # calculo el minimo de cada juego siguiente mio
        choices = col.aggregate([
            { '$match': {
                '_id': {'$in': child['child'].keys()}
            }},
            { '$project': {
                '_id': 1,
                'weight':{
                    '$add':[
                        {'$multiply': ['$win', 1]},
                        {'$multiply': ['$lose', -1]},
                        {'$multiply': ['$draw', 0]},
                    ]
                }
            }
            },
            { '$sort': {'weight': 1} # orden ascendente
            },
            {'$limit': 1}
        ]) # ya tengo el de mayor valor
        
        children_map[child['_id']] = next(choices, def_weight)['weight']

    #print children_map

    #calculo el tabler con el maximo para mi siguiente tiro
    max_key = max(children_map, key=lambda k: children_map[k])
    
    #print max_key
    return head['child'][max_key]

    # seleccion del menor siguiente
    """
    choices = col.aggregate([
        { '$match': {
            '_id': {'$in': head['child'].keys()}
        }},
        { '$project': {
            '_id': 1,
            'weight':{
                '$add':[
                    {'$multiply': ['$win', 1]},
                    {'$multiply': ['$lose', -1]},
                    {'$multiply': ['$draw', 0]},
                ]
            }
        }
        },
        { '$sort': {'weight': 1}
        },
        {'$limit': 1}
    ])

    choice = choices.next()
    return head['child'][choice['_id']]
    """

client = MongoClient('localhost', 27017)
db = client['othello']
col = db['move']
N = 8

#print get_corner('8146ef43c53f35c34f7f10210e17265f')