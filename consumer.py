import json
from typing import List, Optional

from confluent_kafka import Consumer, KafkaException, TopicPartition

from config import config


def set_consumer_configs(servers: Optional[list] = None):
    config["group.id"] = "bulhufas_group"
    # so that we can consume event that are already in our target topic.
    config["auto.offset.reset"] = "earliest"
    # so that we can control the committing of offsets for our consumer.
    config["enable.auto.offset.store"] = False
    if servers is not None:
        config["bootstrap.servers"] = ",".join(servers)


def assignment_callback(consumer: Consumer, partitions: TopicPartition):
    for p in partitions:
        print(f"Assigned to {p.topic}, partition {p.partition}")


if __name__ == "__main__":
    set_consumer_configs()
    c = Consumer(config)
    c.subscribe(["bulhufas"], on_assign=assignment_callback)
    data = []
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                val = msg.value().decode("utf8")
                partition = msg.partition()
                print(f"Received: {val} from partition {partition}")
                data.append(json.loads(val))
    except KeyboardInterrupt:
        print("Canceled by user.")
    finally:
        c.close()
