import shutil
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from config import HOST, PORT

for item in ["./checkpoint", "./csv"]:
    try:
        shutil.rmtree(item)
    except OSError as err:
        print(f"Aviso: {err.strerror}")

spark = SparkSession.builder.appName("Spark Streaming").getOrCreate()

tweets = (
    spark.readStream
    .format("socket")
    .option("host", HOST)
    .option("port", PORT)
    .load()
)

query = (
    tweets.writeStream
    .outputMode("append")
    .option("encoding", "utf-8")
    .format("csv")
    .option("path", "./csv")
    .option("checkpointLocation", "./checkpoint")
    .start()
)

# Append Mode - Somente as novas linhas anexadas na Tabela de Resultados
# desde o último acionador serão gravadas no armazenamento externo.
# Isso é aplicável apenas nas consultas em que não se espera
# que as linhas existentes na Tabela de Resultados sejam alteradas.
# query = lines.writeStream.outputMode("append").format("console").start()

query.awaitTermination()