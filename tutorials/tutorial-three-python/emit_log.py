import pika
import sys
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.50.209',
                              credentials=pika.PlainCredentials('root', 'root')))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

try:
    for i in range(int(1e6)):
        sent_message = message + " " + str(i)
        channel.basic_publish(exchange="logs",
                              routing_key='',
                              body=sent_message
                              )
        print("[x] Sent {}".format(sent_message))
        time.sleep(1)
except KeyboardInterrupt:
    pass

print("[x] shutdown the producer.")
connection.close()
