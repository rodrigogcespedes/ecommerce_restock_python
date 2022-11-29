import pika
from pika.exchange_type import ExchangeType
from services.orden_service import crear_orden_automatica


def on_message_received(ch, method, properties, body):
    print(f"Received new message: {body}")


connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='Catalogo', exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='', exclusive=True)

queue_name = queue.method.queue

channel.queue_bind(exchange='Catalogo', queue=queue_name, routing_key='venta.articulo.*')

channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=crear_orden_automatica)

print("Starting Consuming")

channel.start_consuming()