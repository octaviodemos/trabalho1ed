# Delta

## Papel do Delta no experimento

No projeto, Delta Lake e a implementacao usada para comparar mutabilidade e auditoria contra Iceberg, sempre com o mesmo dataset e o mesmo motor Spark.

## Implementacao no repositorio

O fluxo esta em `notebooks/delta-lake.ipynb` e usa:

- leitura do arquivo `data/raw/statcast_data.csv`;
- schema e limpeza vindos de `src/ingestao.py`;
- escrita da tabela em `data/delta_statcast`.

O notebook tambem utiliza a API `DeltaTable` para executar alteracoes pontuais sem recarga completa da base.

Sessao Spark com extensões e *catalog* Delta (detalhes e demais passos em [Exemplos de código](exemplos_codigo.md)):

```python
from pyspark.sql import SparkSession

DELTA_PACKAGES = "io.delta:delta-spark_2.12:3.2.0"

spark = (
    SparkSession.builder.appName("DeltaLake_SATC")
    .config("spark.jars.packages", DELTA_PACKAGES)
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", "data/warehouse")
    .getOrCreate()
)
```

## Cenarios executados no notebook

### 1) Carga inicial da tabela

Persistencia do dataset de arremessadores no formato Delta para criar a linha de base do experimento.

### 2) UPDATE de `velocidade_media`

Simulacao de correcao de telemetria para um jogador especifico, validando alteracao parcial de linha.

### 3) DELETE de jogador

Remocao de registro para reproduzir cenario de saneamento/sancao, mantendo historico da operacao.

## Evidencia de historico transacional

O notebook consulta `history()` da tabela Delta ao final. Isso registra cada operacao executada no experimento e serve como evidencia de auditoria para o relatorio.

```python
from delta.tables import DeltaTable

tabela_delta = DeltaTable.forPath(spark, CAMINHO_DELTA)
tabela_delta.history().select(
    "version", "timestamp", "operation", "operationParameters"
).show(truncate=False)

spark.read.format("delta").option("versionAsOf", 0).load(CAMINHO_DELTA)
```

## O que observamos com Delta

Dentro do escopo deste trabalho:

- API `DeltaTable` deixa update/delete diretos no PySpark;
- log transacional facilita rastreabilidade das mudancas;
- o fluxo ficou simples de reproduzir localmente em notebook.
