from confluent_kafka import Producer
import socket

def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced to: {msg.topic()} [{msg.partition()}]")

def send_message(bootstrap_server, topic):
    conf = {"bootstrap.servers": bootstrap_server, "client.id": socket.gethostname()}
    producer = Producer(conf)

    message_key = b"Hello"

    for i in range(10):
        message_value = f"some_message_byte {i}".encode("utf-8")
        producer.produce(topic, key=message_key, value=message_value, callback=acked)
        producer.poll(1)

    producer.flush()

if __name__ == "__main__":
    bootstrap_server = "localhost:9094"
    topic = "vuthekiet_topic1"
    send_message(bootstrap_server, topic)
