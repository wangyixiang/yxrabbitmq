import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.50.209', credentials=pika.credentials.PlainCredentials('root', 'root')))
channel = connection.channel()
channel.queue_declare(queue='helloq')


def callback(ch, method, properties, body):
    print(body)


channel.basic_consume(callback, queue='helloq', no_ack=True)

channel.start_consuming()