from bson import json_util
from fastapi import FastAPI
from Entities import OrdenRestockCompleta
from Entities import OrdenRestockVacia
from Entities import ArticuloVacio
from Entities import ArticuloModificacion
from repositories.articulo_repository import crear_articulo, modificar_articulo, buscar_un_articulo, borrar_articulo
from repositories.orden_repository import crear_orden, finalizar_orden, cancelar_orden, buscar_ordenes_pendintes, buscar_ordenes_por_articulo
import pika
import json
from pika.exchange_type import ExchangeType

# python -m uvicorn server:app --port 9600 --reload

# ---------------------RABBITMQ---------------------

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='Restock', exchange_type=ExchangeType.topic)

# ---------------------API-SERVER---------------------

app = FastAPI()


def parse_json(data: dict):
    return json.loads(json_util.dumps(data))


@app.get('/{idOrdenRestock}/ordenRestock')
def load(idOrdenRestock: str):
    orden = finalizar_orden(idOrdenRestock)
    return orden


@app.get('/ordenesPendientes')
def load():
    ordenes = buscar_ordenes_pendintes()
    return ordenes


@app.get('/{idArticulo}/ordenesPorArticulo')
def load(idArticulo: str):
    articulo = buscar_ordenes_por_articulo(idArticulo)
    return articulo


@app.put('/{idOrdenRestock}/cancelarOrden')
def load(idOrdenRestock: str):
    orden_cancelada = cancelar_orden(idOrdenRestock)
    channel.basic_publish(exchange='Restock', routing_key='order.canceled', body=json.dumps(orden_cancelada))
    return orden_cancelada


@app.put('/{idOrdenRestock}/finalizarOrden')
def load(idOrdenRestock: str):
    orden_finalizada = finalizar_orden(idOrdenRestock)
    channel.basic_publish(exchange='Restock', routing_key='order.ended', body=json.dumps(orden_finalizada))
    return orden_finalizada


@app.post('/crearOrden')
def load(body: OrdenRestockVacia):
    orden_nueva = crear_orden(body.__dict__)
    modificar_articulo(orden_nueva['idArticulo'], {'ultimaOrden': orden_nueva['id']})
    channel.basic_publish(exchange='Restock', routing_key='order.created', body=json.dumps(orden_nueva))
    return orden_nueva


@app.post('/crearArticulo')
def load(body: ArticuloVacio):
    articulo_nuevo = crear_articulo(body.__dict__)
    return articulo_nuevo


@app.put('/{idArticulo}/modificarArticulo')
def load(idArticulo: str, body: ArticuloModificacion):
    articulo_modificado = modificar_articulo(idArticulo, body.__dict__)
    return articulo_modificado


@app.delete('/{idArticulo}/borrarArticulo')
def load(idArticulo: str):
    articulo_borrado = borrar_articulo(idArticulo)
    return articulo_borrado
