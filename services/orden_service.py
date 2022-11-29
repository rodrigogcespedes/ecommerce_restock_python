import json
import pika
from bson import json_util
from pika.exchange_type import ExchangeType
from Entities import dtoArticuloCatalogo
from repositories.orden_repository import crear, modificar, buscar_uno, buscar_muchos
from services.articulo_service import buscar_un_articulo, modificar_articulo

# ---------------------RABBITMQ---------------------

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# ---------------------EXCHANGES---------------------
channel.exchange_declare(exchange='Restock', exchange_type=ExchangeType.topic)

CREATED = 'pendiente'
CANCELED = 'cancelada'
ENDED = 'finalizada'


def parse_json(data: dict):
    return json.loads(json_util.dumps(data))


def crear_orden_automatica(ch, method, properties, body):
    flag = False
    dto = json.loads(body)
    articulo = buscar_un_articulo(dto['idArticulo'])
    if (dto['cantidad'] <= articulo['umbral'] * (2 if articulo['altaDemanda'] else 1)) and not articulo['noReponer']:
        if articulo['ultimaOrden'] != '0':
            orden = buscar_una_orden(articulo['ultimaOrden'])
            if orden['estado'] != CREATED:
                flag = True
        else:
            flag = True
    if flag:
        dictio = {
            'idArticulo': articulo['id'],
            'cantidad': articulo['cantidadRestock']
        }
        crear_orden(dictio)


def buscar_una_orden(idOrdenRestock: str):
    orden = buscar_uno(idOrdenRestock)
    del orden['_id']
    return orden


def buscar_ordenes_pendintes():
    condicion = {'estado': CREATED}
    ordenes = buscar_muchos(condicion)
    for orden in ordenes:
        del orden['_id']
    return ordenes


def buscar_ordenes_por_articulo(idArticulo: str):
    condicion = {'idArticulo': idArticulo}
    ordenes = buscar_muchos(condicion)
    for orden in ordenes:
        del orden['_id']
    articulo = buscar_un_articulo(idArticulo)
    articulo['ordenes'] = ordenes
    return articulo


def cancelar_orden(idOrdenRestock: str):
    modificacion = {'estado': CANCELED}
    orden_cancelada = modificar(idOrdenRestock, modificacion)
    channel.basic_publish(exchange='Restock', routing_key='order.canceled', body=json.dumps(orden_cancelada))
    return orden_cancelada


def finalizar_orden(idOrdenRestock: str):
    modificacion = {'estado': ENDED}
    orden_finalizada = modificar(idOrdenRestock, modificacion)
    channel.basic_publish(exchange='Restock', routing_key='order.ended', body=json.dumps(orden_finalizada))
    return orden_finalizada


def crear_orden(body: dict):
    orden_nueva = crear(body)
    modificar_articulo(orden_nueva['idArticulo'], {'ultimaOrden': orden_nueva['id']})
    #channel.basic_publish(exchange='Restock', routing_key='order.created', body=json.dumps(orden_nueva))
    return orden_nueva
