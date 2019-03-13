import pika
import sys

rabbitmq_host = "192.168.50.209"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host,
        credentials=pika.PlainCredentials("root", "root")
    )
)

channel = connection.channel()
exchange_name = "direct_logs"

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# info warning error
severities = sys.argv[1:] if len(sys.argv) > 1 else ['info']

for severity in severities:
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=severity)


def callback(ch, method, prop, body):
    print(" [x] {}:{}".format(method.routing_key, body))


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
