import pyspark.sql.functions as F
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType, 
    StructField, 
    StringType, 
    FloatType, 
    IntegerType
)

def obter_esquema_statcast() -> StructType:
    
    return StructType([
        StructField("player_name", StringType(), True),
        StructField("pitches", IntegerType(), True),
        StructField("velocity", FloatType(), True),
        StructField("spin_rate", IntegerType(), True),
        StructField("ba", FloatType(), True),
        StructField("so", IntegerType(), True),
        StructField("hrs", IntegerType(), True),
        StructField("bb", IntegerType(), True)
    ])

def ler_e_limpar_dados(spark: SparkSession, caminho_arquivo: str) -> DataFrame:
    df_bruto = spark.read.csv(caminho_arquivo, header=True, inferSchema=False)
    
    esquema = obter_esquema_statcast()
    renomeacao = {
        "player_name": "nome_jogador",
        "pitches": "total_arremessos",
        "velocity": "velocidade_media",
        "spin_rate": "taxa_giro",
        "ba": "media_rebatidas_contra",
        "so": "strikeouts",
        "hrs": "home_runs_cedidos",
        "bb": "walks_cedidos"
    }
    
    colunas_selecionadas = []
    for campo in esquema.fields:
        col_name = campo.name
        col_type = campo.dataType
        novo_nome = renomeacao.get(col_name, col_name)
        
        colunas_selecionadas.append(
            F.col(col_name).cast(col_type).alias(novo_nome)
        )
        
    return df_bruto.select(*colunas_selecionadas)

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("IngestaoStatcastAgregado") \
        .getOrCreate()
        
    caminho_csv = "data/raw/statcast_data.csv"
    
    try:
        df_limpo = ler_e_limpar_dados(spark, caminho_csv)
        print("Schema do DataFrame Limpo:")
        df_limpo.printSchema()
        print("Amostra dos Dados:")
        df_limpo.show(1000, truncate=False)
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
