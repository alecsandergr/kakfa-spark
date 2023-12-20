from __future__ import annotations

import logging

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(funcName)s: %(levelname)s: %(message)s"
)
logger = logging.getLogger("spark_structured_streaming")


def initialize_spark_session(app_name: str) -> SparkSession | None:
    """
    Initialize the Spark Session with provided configurations.

    Args:
        app_name (str): Name of the spark application.

    Returns:
        SparkSession | None: Spark session object or None if there's an error.
    """
    try:
        spark = SparkSession.builder.appName(app_name).getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")
        logger.info("Spark session created successfully")
        return spark

    except Exception as e:
        logger.error(f"Spark session initialization failed. Error: {e}")
        return None


def get_streaming_dataframe(
    spark: SparkSession, brokers: list, topic: str
) -> DataFrame | None:
    """
    Get a streaming dataframe from Kafka.

    Args:
        spark (SparkSession): Initialized Spark session.
        brokers (list): List of Kafka brokers.
        topic (str): Kafka topic to subscribe to.

    Returns:
        DataFrame | None: Dataframe object or None if there's an error.
    """
    try:
        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", ",".join(brokers))
            .option("subscribe", topic)
            .option("delimiter", ",")
            .option("startingOffsets", "earliest")
            .load()
        )
        logger.info("Streaming dataframe fetched successfully")
        return df

    except Exception as e:
        logger.warning(f"Failed to fetch streaming dataframe. Error: {e}")
        return None


def transform_streaming_data(df: DataFrame) -> DataFrame:
    """
    Transform the initial dataframe to get the final structure.

    Args:
        df (DataFrame): Initial dataframe with raw data.

    Returns:
        DataFrame: Transformed dataframe.
    """
    schema = StructType(
        [
            StructField("name", StringType(), False),
            StructField("gender", StringType(), False),
            StructField("address", StringType(), False),
            StructField("city", StringType(), False),
            StructField("nation", StringType(), False),
            StructField("zip", StringType(), False),
            StructField("latitude", StringType(), False),
            StructField("longitude", StringType(), False),
            StructField("email", StringType(), False),
        ]
    )

    transformed_df = (
        df.selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )

    return transformed_df


def initiate_streaming_to_console(df: DataFrame):
    """
    Start streaming the transformed data to the console.

    Args:
        df (DataFrame): Transformed dataframe.
    """
    logger.info("Initiating streaming process...")
    stream_query = df.writeStream.format("console").outputMode("append").start()
    stream_query.awaitTermination()


def main():
    app_name = "SparkStructuredStreamingToConsole"
    brokers = ["kafka:19092"]
    topic = "random_names"

    spark = initialize_spark_session(app_name)
    if spark:
        df = get_streaming_dataframe(spark, brokers, topic)
        if df:
            transformed_df = transform_streaming_data(df)
            initiate_streaming_to_console(transformed_df)


if __name__ == "__main__":
    main()
