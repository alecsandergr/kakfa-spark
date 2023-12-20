from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


def topic_exists(admin_client: KafkaAdminClient, topic_name: str):
    topic_metadata = admin_client.list_topics()
    return topic_name in topic_metadata.topics if topic_metadata else False


def create_topic(
    admin_client: KafkaAdminClient,
    topic_name: str,
    num_partitions: int,
    replication_factor: int,
):
    new_topic = NewTopic(
        name=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )

    try:
        admin_client.create_topics(new_topics=[new_topic], validate_only=False)
        print(f'Topic "{topic_name}" created successfully.')
    except TopicAlreadyExistsError:
        print(f'Topic "{topic_name}" already exists.')


bootstrap_servers = "localhost:9092"

admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

topic_name = "bulhufas"
partitions = 3
replication_factor = 1

if not topic_exists(admin_client, topic_name):
    create_topic(admin_client, topic_name, partitions, replication_factor)
