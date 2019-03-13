import pika
import sys
import time
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.50.209',
                              credentials=pika.PlainCredentials('root', 'root')))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
try:
    for i in range(int(1e6)):
        sent_message = str(i) + " " + message + "." * random.randint(0, 2)
        print("[x] Sent {}".format(sent_message))
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=sent_message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        time.sleep(1)
except KeyboardInterrupt:
    pass

connection.close()
