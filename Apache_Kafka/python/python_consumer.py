from confluent_kafka import KafkaError, KafkaException, Consumer


def process_message(msg):
    key = msg.key()
    value = msg.value()
    print(f"Received message with key {key.decode('utf-8')} and value {value.decode('utf-8')}")


def consumer_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"%% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                process_message(msg)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except KafkaException as e:
        print(f"Kafka error: {e}")
    finally:
        consumer.close()


if __name__ == "__main__":
    conf = {
        'bootstrap.servers': 'localhost:9094',
        'group.id': 'hello',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    topics = ['vuthekiet_topic1']

    consumer_loop(consumer, topics)
