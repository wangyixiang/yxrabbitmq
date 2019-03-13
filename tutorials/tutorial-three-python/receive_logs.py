import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.50.209',
                              credentials=pika.PlainCredentials('root', 'root')))
channel = connection.channel()

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)


def callback(ch, method, properties, body):
    print(" [x] {}".format(body))


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
