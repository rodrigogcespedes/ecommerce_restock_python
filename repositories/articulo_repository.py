import json
import pymongo
from bson import json_util
import uuid

client = pymongo.MongoClient(
    'mongodb+srv://StockUser:ZttZr9vG86O7oSeH@clusterstock.yqskleb.mongodb.net/?retryWrites=true&w=majority')

db = client['restock_db']

collec_articulo = db['articulo']

collec_orden = db['orden_restock']


def parse_json(data: dict):
    return json.loads(json_util.dumps(data))


def buscar_un_articulo(id: str):
    articulo = collec_articulo.find_one({
        'id': id
    })
    return parse_json(articulo)


def crear_articulo(articulo_vacio : dict):
    articulo_nuevo = {
        'id': str(uuid.uuid1()),
        'idArticulo': articulo_vacio['idArticulo'],
        'umbral': articulo_vacio['umbral'],
        'cantidadRestock': articulo_vacio['cantidadRestock'],
        'altaDemanda': articulo_vacio['altaDemanda'],
        'noReponer': articulo_vacio['noReponer'],
        'ultimaOrden': '0'
    }
    collec_articulo.insert_one(parse_json(articulo_nuevo))
    return articulo_nuevo


def modificar_articulo(id: str, articulo_modificado : dict):
    collec_articulo.update_one({
        'id': id
    },
        {
        '$set': parse_json(articulo_modificado)
    })
    return buscar_un_articulo(id)


def borrar_articulo(id:str):
    collec_articulo.update_one({
        'id': id
    },
        {
        '$set': {
            'noReponer': True
        }
    })
    return {'deleted': id}
