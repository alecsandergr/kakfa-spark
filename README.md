# Apache Kafka and Spark <!-- omit in toc -->

Author: Alecsander Guimarães Rodrigues 

[Github](http://github.com/alecsandergr)

[LinkedIn](http://linkedin.com/in/alecsandergr)

## Table of Contents <!-- omit in toc -->

- [Summary](#summary)
- [Creating the containers](#creating-the-containers)
- [Creating the virtual environment](#creating-the-virtual-environment)
- [Using Kafka](#using-kafka)
- [Using Spark](#using-spark)

## Summary

This repository contains examples of how to use Kafka, such as creating a topic, a producer, and a consumer. Furthermore, it includes a Spark job that uses the data stored in Kafka and prints it to the console. To run these examples, you must have Docker installed. If Docker is not installed yet, please check the [website](https://docs.docker.com/get-docker/) for installation instructions.

If you want to learn more about Kafka, you can check out this [repository](https://github.com/confluentinc/confluent-kafka-python) or the [Introduction to Python for Apache Kafka](https://developer.confluent.io/courses/kafka-python/intro/). 

## Creating the containers

You can check the docker-compose file [here](docker-compose.yml), but all you need to do, once you have installed the Docker, is to replicate the commands below.

```sh
# Run the commands to start the container
docker-compose -f docker-compose.yml up -d
# Stop the container when finished
docker-compose -f docker-compose.yml down -v
```

## Creating the virtual environment

For this project, if you have poetry installed, follow the instructions below:

```sh
# Install Poetry using the official installer
curl -sSL https://install.python-poetry.org | python3 -
# Navigate to your project's directory
cd your_project_directory
# Install the dependencies
poetry install
# Activate the virtual environment
poetry shell
```

You can also check the official documentation [here](https://python-poetry.org/docs/), if you would like to install it.

If you don't have, you can use venv:
```sh
# if you use macOS/Unix
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
# if you use Windows
py -m venv .venv
.venv\bin\Activate.bat
py -m pip install -r requirements.txt
```

## Using Kafka

Below are some examples of how you can use Kafka.

- [Creating a topic](topic.py) 
- [Consumer](consumer.py)
- [Producer](producer.py)

## Using Spark

To run the Spark job, you need to start the container containing Spark. For this example, follow these steps:

```sh
# Start the container
docker exec -it {your-directory}-spark-1 /bin/bash
# Change to the folder where the spark job is located
cd /src/streaming
# Give the shell script the permissions necessary
chmod +x run.sh
# Run the spark job
./run.sh
```

Below there are all the code:
- [Spark Job](src/streaming/spark_process.py)
- [Shell Script](src/streaming/run.py)