import json
import pymongo
from bson import json_util
from repositories.articulo_repository import buscar_uno
import uuid
import datetime


client = pymongo.MongoClient(
    'mongodb+srv://StockUser:ZttZr9vG86O7oSeH@clusterstock.yqskleb.mongodb.net/?retryWrites=true&w=majority')

db = client['restock_db']

collec_articulo = db['articulo']

collec_orden = db['orden_restock']

CREATED = 'pendiente'
CANCELED = 'cancelada'
ENDED = 'finalizada'


def parse_json(data: dict):
    return json.loads(json_util.dumps(data))


def buscar_uno(id: str):
    orden = collec_orden.find_one({
        'id': id
    })
    return parse_json(orden)


def buscar_muchos(condiciones: dict):
    orden = collec_orden.find(
        parse_json(condiciones)
    )
    return parse_json(orden)


def crear(orden_vacia: dict):
    orden_nueva = {
        'id': str(uuid.uuid1()),
        'fechaEmision': datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S'),
        'estado': CREATED,
        'idArticulo': orden_vacia['idArticulo'],
        'cantidad': orden_vacia['cantidad']
    }
    collec_orden.insert_one(parse_json(orden_nueva))
    return orden_nueva


def modificar(id: str, modificaciones: dict):
    collec_orden.update_one({
        'id': id
    },
        {
        '$set': parse_json(modificaciones)
    })
    print(modificaciones)
    print(buscar_uno(id))
    return buscar_uno(id)


# def buscar_ordenes(condiciones: dict):
#     orden = collec_orden.find(condiciones)
#     return parse_json(condiciones)

# def buscar_ordenes_pendintes():
#     orden = collec_orden.find({
#         'estado': CREATED
#     })
#     return parse_json(orden)


# def buscar_ordenes_por_articulo(id: str):
#     articulo = buscar_uno(id)
#     orden = collec_orden.find({
#         'idArticulo': id
#     })
#     articulo['ordenes'] = orden
#     return parse_json(articulo)


# def cancelar_orden(id: str):
#     collec_orden.update_one({
#         'id': id
#     },
#         {
#         '$set': {
#             'estado': CANCELED
#         }
#     })
#     return buscar_una_orden(id)
#
#
# def finalizar_orden(id: str):
#     collec_orden.update_one({
#         'id': id
#     },
#         {
#         '$set': {
#             'estado': ENDED
#         }
#     })
#     return buscar_una_orden(id)
