import pika
from pika.exchange_type import ExchangeType


def on_message_received(ch, method, properties, body):
    print(f"Received new message: {body}")


connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='Restock', exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='', exclusive=True)

queue_name = queue.method.queue

channel.queue_bind(exchange='Restock', queue=queue_name, routing_key='order.*')

channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=on_message_received)

print("Starting Consuming")

channel.start_consuming()
