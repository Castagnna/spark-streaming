from pyspark.sql import SparkSession
from config import HOST, PORT

spark = SparkSession.builder.appName("Spark Streaming").getOrCreate()

lines = (
    spark.readStream
    .format("socket")
    .option("host", HOST)
    .option("port", PORT)
    .load()
)

query = lines.writeStream.outputMode("append").format("console").start()

query.awaitTermination()