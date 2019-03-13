import pika
import time
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.50.209', credentials=pika.credentials.PlainCredentials('root', 'root')))
channel = connection.channel()
channel.queue_declare(queue='helloq')

try:
    for i in range(int(1e6)):
        channel.basic_publish(exchange='', routing_key='helloq', body='Hello World!%d' % i)
        time.sleep(1)
except KeyboardInterrupt:
    pass
print("stop sending.")
connection.close()
