# Exemplos de código

Esta página resume **como o projeto aplica** Spark, Delta Lake e Iceberg no mesmo cenário Statcast. Os trechos espelham `notebooks/delta-lake.ipynb`, `notebooks/iceberg.ipynb` e `src/ingestao.py`; execute sempre a partir da raiz do repositório com o kernel do `.venv`.

No fluxo Delta, crie o `SparkSession` abaixo, depois a ingestão comum e a gravação. Para Iceberg, use a sessão da seção Iceberg e volte à ingestão antes do `CREATE TABLE`.

## Delta Lake — sessão Spark

Pacote Maven alinhado ao `pyproject.toml` (`delta-spark==3.2.0` com Spark 3.5.x):

```python
import os
from pathlib import Path

os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")

from pyspark.sql import SparkSession

raiz_projeto = Path(".").resolve()
DELTA_PACKAGES = "io.delta:delta-spark_2.12:3.2.0"

spark = (
    SparkSession.builder.appName("DeltaLake_SATC")
    .config("spark.jars.packages", DELTA_PACKAGES)
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", str(raiz_projeto / "data" / "warehouse"))
    .getOrCreate()
)
```

## Ingestão comum (`src/ingestao.py`)

O CSV bruto usa nomes de colunas em inglês; `ler_e_limpar_dados` aplica *cast* ao esquema e renomeia para o modelo de arremessadores usado nas duas tabelas.

```python
import sys
from pathlib import Path

raiz_projeto = Path(".").resolve()
if str(raiz_projeto) not in sys.path:
    sys.path.insert(0, str(raiz_projeto))

from src.ingestao import obter_esquema_statcast, ler_e_limpar_dados

CAMINHO_CSV = str(raiz_projeto / "data" / "raw" / "statcast_data.csv")

esquema_statcast = obter_esquema_statcast()
df = ler_e_limpar_dados(spark, CAMINHO_CSV)
assert len(df.columns) == len(esquema_statcast.fields)
```

## Delta Lake — gravação inicial e mutações

```python
CAMINHO_DELTA = str(raiz_projeto / "data" / "delta_statcast")

df.write.format("delta").mode("overwrite").save(CAMINHO_DELTA)
```

```python
from delta.tables import DeltaTable
import pyspark.sql.functions as F

tabela_delta = DeltaTable.forPath(spark, CAMINHO_DELTA)

tabela_delta.update(
    condition="nome_jogador = 'Webb, Logan'",
    set={"velocidade_media": F.lit(89.2)},
)
```

```python
spark.sql(
    f"""
    INSERT INTO delta.`{CAMINHO_DELTA}`
    VALUES (
      'Pitcher, Teste',
      500,
      93.5,
      2400,
      0.210,
      110,
      10,
      30
    )
    """
)
```

```python
tabela_delta.delete(condition=F.expr("nome_jogador = 'Rodón, Carlos'"))
```

## Delta Lake — histórico e *time travel*

```python
tabela_delta.history().select(
    "version", "timestamp", "operation", "operationParameters"
).show(truncate=False)

df_versao_zero = (
    spark.read.format("delta")
    .option("versionAsOf", 0)
    .load(CAMINHO_DELTA)
)
```

## Iceberg — sessão Spark e catálogo `ice`

Para reproduzir o notebook Iceberg isoladamente, reinicie o kernel do Jupyter (outro conjunto de pacotes Maven no mesmo processo Spark costuma exigir sessão limpa).

```python
from pathlib import Path
from pyspark.sql import SparkSession

raiz_projeto = Path(".").resolve()
warehouse_path = str(raiz_projeto / "data" / "iceberg_warehouse")
ICEBERG_RUNTIME = "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2"

spark = (
    SparkSession.builder.appName("Iceberg_Statcast")
    .config("spark.jars.packages", ICEBERG_RUNTIME)
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.ice", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.ice.type", "hadoop")
    .config("spark.sql.catalog.ice.warehouse", warehouse_path)
    .config("spark.sql.defaultCatalog", "ice")
    .getOrCreate()
)
```

## Iceberg — tabela, carga e DML em SQL

```python
TABELA = "ice.baseball.statcast_arremessadores"

spark.sql("CREATE NAMESPACE IF NOT EXISTS ice.baseball")
spark.sql(f"DROP TABLE IF EXISTS {TABELA}")

df.createOrReplaceTempView("staging_statcast")

spark.sql(
    f"""
    CREATE TABLE {TABELA} (
      nome_jogador STRING,
      total_arremessos INT,
      velocidade_media FLOAT,
      taxa_giro INT,
      media_rebatidas_contra FLOAT,
      strikeouts INT,
      home_runs_cedidos INT,
      walks_cedidos INT
    ) USING iceberg
    """
)

spark.sql(
    f"""
    INSERT INTO {TABELA}
    SELECT * FROM staging_statcast
    """
)
```

```sql
UPDATE ice.baseball.statcast_arremessadores
SET velocidade_media = 89.2
WHERE nome_jogador = 'Webb, Logan';
```

```sql
DELETE FROM ice.baseball.statcast_arremessadores
WHERE nome_jogador = 'Rodón, Carlos';
```

## Iceberg — auditoria por metadados

```python
spark.sql(f"SELECT * FROM {TABELA}.snapshots ORDER BY committed_at DESC").show(truncate=False)
spark.sql(f"SELECT * FROM {TABELA}.history ORDER BY made_current_at DESC").show(truncate=False)
```

## Leitura cruzada

| Objetivo | Delta | Iceberg |
|----------|-------|---------|
| Carga tabular | `df.write.format("delta")` | `CREATE TABLE ... USING iceberg` + `INSERT` |
| Correção pontual | `DeltaTable.update` / SQL | `UPDATE ... WHERE` |
| Remoção | `DeltaTable.delete` / SQL | `DELETE ... WHERE` |
| Linha do tempo | `history()`, `versionAsOf` | `.snapshots`, `.history` |

Para o passo a passo completo com saídas e markdown explicativo, abra os notebooks em `notebooks/`.
