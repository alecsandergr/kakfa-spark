#!/bin/bash
# Script: run.sh
# Description: A script to submit a Spark job with a provided argument.
# Usage: ./run.sh <your_spark_scripts>

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

script=$1

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /src/streaming/"$script"