import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='Catalogo', exchange_type=ExchangeType.topic)

message = '{"idArticulo": "9d17622e-6e9e-11ed-9144-3ca82aabe788", "cantidad": 1}'

channel.basic_publish(exchange='Catalogo', routing_key='venta.articulo.cocina', body=message)

print(f"sent message: {message}")

connection.close()