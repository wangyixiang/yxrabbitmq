import pika

rabbitmq_host = "192.168.50.209"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host,
        credentials=pika.PlainCredentials("root", "root")
    )
)
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def fib(n):
    if 0 == n:
        return 0
    if 1 == n:
        return 1
    return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)
    print("fib({})".format(n))
    response = fib(n)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')
channel.start_consuming()
