
import os
import sys


from confluent_kafka import Consumer, KafkaError, KafkaException

from receipt.examples.image2text.easyocr_test import result
from workers.expense_actor import ExpenseAnalyticsActor

# engine = create_engine(postgres_async_config.SYNC_POSTGRES_URL, echo=True)
# SessionFactory = sessionmaker(bind=engine)


kafka_brokers = os.getenv("KAFKA_BROKERS", "localhost:9092")

conf = {
    'bootstrap.servers': kafka_brokers,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
topics = ['expense_analytics']
consumer.subscribe(topics)

class KafkaReciever:
    def __init__(self):
        self.actors = {
            'expense_analytics': ExpenseAnalyticsActor
        }


    def __call__(self, message, topic):
        actor = self.actors.get(topic)
        if not actor:
            raise Exception(f'No actor for topic {topic}')
        try:
            actor = actor(message)
        except Exception as ex:
            print("Could not create actor: " + str(ex))
        result = actor.process(message)

        if result:
            actor.output()
        return


running = True


def shutdown():
    running = False


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        kafka_receiver = KafkaReciever()
        print("Start consuming")

        while running:
            msg = consumer.poll(timeout=1.0)
            print('msg: ', msg)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    continue
                elif msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))

                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                kafka_receiver(msg.value().decode('utf-8'), msg.topic())
    finally:
        consumer.close()


if __name__ == '__main__':
    basic_consume_loop(consumer, ['video'])