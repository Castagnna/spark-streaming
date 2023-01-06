from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from config import HOST, PORT

spark = SparkSession.builder.appName("Spark Streaming").getOrCreate()

lines = (
    spark.readStream
    .format("socket")
    .option("host", HOST)
    .option("port", PORT)
    .load()
)

words = lines.select(F.explode(F.split(F.col("value"), " ")).alias("word"))
word_count = (
    words
    .groupBy("word")
    .agg(F.count("*").alias("cnt"))
    .orderBy(F.col("cnt").desc())
    .limit(20)
)
query = word_count.writeStream.outputMode("complete").format("console").start()

# Append Mode - Somente as novas linhas anexadas na Tabela de Resultados
# desde o último acionador serão gravadas no armazenamento externo.
# Isso é aplicável apenas nas consultas em que não se espera
# que as linhas existentes na Tabela de Resultados sejam alteradas.
# query = lines.writeStream.outputMode("append").format("console").start()

query.awaitTermination()