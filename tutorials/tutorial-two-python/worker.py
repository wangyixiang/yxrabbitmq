import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.50.209',
                              credentials=pika.PlainCredentials('root', 'root')))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print('[*] Waiting for messages')


def callback(ch, method, properties, body):
    print("[x] Recieved %s" % body)
    time.sleep(body.count(b"."))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

# worker将用round robin的方式来消费message
channel.start_consuming()
