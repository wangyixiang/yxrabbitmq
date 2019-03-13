import pika
import sys
import time

rabbitmq_host = "192.168.50.209"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host,
        credentials=pika.PlainCredentials("root", "root")
    )
)

channel = connection.channel()
exchange_name = "direct_logs"
channel.exchange_declare(exchange=exchange_name,
                         exchange_type="direct")

severity = sys.argv[1] if len(sys.argv) > 1 else "info"
message = ' '.join(sys.argv[2]) if len(sys.argv) > 2 else "Hello World!"

try:
    for i in range(int(1e6)):
        sent_message = ' '.join([str(i), message])
        channel.basic_publish(exchange=exchange_name,
                              routing_key=severity,
                              body=sent_message)
        print("[x] Sent {}:{}".format(severity, sent_message))
        time.sleep(1)
except KeyboardInterrupt:
    pass

connection.close()