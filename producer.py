# Importing necessary libraries and modules
import hashlib
import json
import time
from typing import Optional

import requests
from confluent_kafka import Producer

from config import config

# Constants and configuration
API_ENDPOINT = "https://randomuser.me/api/?results=1"
KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
KAFKA_TOPIC = "random_names"
PAUSE_INTERVAL = 10
STREAMING_DURATION = 120


def retrieve_user_data(url: str = API_ENDPOINT) -> dict:
    """
    Fetches random user data from the provided API endpoint.

    Args:
        url (str, optional): the url from the API. Defaults to API_ENDPOINT.

    Returns:
        dict: a json containing the random data.
    """
    response = requests.get(url)
    return response.json()["results"][0]


def encrypt_zip(zip_code: str) -> int:
    """
    Hashes the zip code using MD5 and returns its integer representation.

    Args:
        zip_code (str): the zip code.

    Returns:
        int: the encoded integer representation from the zip code.
    """
    zip_str = str(zip_code)
    return int(hashlib.md5(zip_str.encode()).hexdigest(), 16)


def transform_user_data(data: dict) -> dict:
    """
    Formats the fetched user data for Kafka streaming.

    Args:
        data (dict): a json containing the random data.

    Returns:
        dict: the formatted user data.
    """
    return {
        "name": f"{data['name']['title']}. {data['name']['first']} {data['name']['last']}",
        "gender": data["gender"],
        "address": f"{data['location']['street']['number']}, {data['location']['street']['name']}",
        "city": data["location"]["city"],
        "nation": data["location"]["country"],
        "zip": encrypt_zip(data["location"]["postcode"]),
        "latitude": float(data["location"]["coordinates"]["latitude"]),
        "longitude": float(data["location"]["coordinates"]["longitude"]),
        "email": data["email"],
    }


def configure_kafka(servers: Optional[list] = None):
    """Creates and returns a Kafka producer instance."""

    if servers:
        config["bootstrap.servers"] = ",".join(servers)
    config["client.id"] = "producer_instance"
    return Producer(config)


def delivery_status(err, msg):
    """Reports the delivery status of the message to Kafka."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [Partition: {msg.partition()}]")


def publish_to_kafka(producer, topic, data):
    """Sends data to a Kafka topic."""
    producer.produce(
        topic, value=json.dumps(data).encode("utf-8"), callback=delivery_status
    )
    producer.flush()


def initiate_stream():
    """Initiates the process to stream user data to Kafka."""
    kafka_producer = configure_kafka(KAFKA_BOOTSTRAP_SERVERS)
    for _ in range(STREAMING_DURATION // PAUSE_INTERVAL):
        raw_data = retrieve_user_data()
        kafka_formatted_data = transform_user_data(raw_data)
        publish_to_kafka(kafka_producer, KAFKA_TOPIC, kafka_formatted_data)
        time.sleep(PAUSE_INTERVAL)


if __name__ == "__main__":
    initiate_stream()
