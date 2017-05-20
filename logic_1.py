## nueva logica
from pymongo import MongoClient
import pprint

def get_next_move(_id):
    """
    recibe el id de la partida actual
    retorna None o el proximo tiro considerado como array, no matriz
    """
    global col 

    head = col.find_one({'_id': _id})
    if head == None:
        return None
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

client = MongoClient('localhost', 27017)
db = client['othello']
col = db['move']
